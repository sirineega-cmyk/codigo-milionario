import os
import sys
import json
import uuid

# Utiliza certificados confiáveis do sistema operacional quando disponível
try:
    import truststore
    truststore.inject_into_ssl()
except Exception:
    pass

from dotenv import load_dotenv
from supabase import create_client, Client

# ==========================================
# CONFIGURAÇÃO DE AMBIENTE E SUPABASE
# ==========================================

# Localiza o arquivo .env tanto na pasta atual quanto na raiz do projeto
_pasta_atual = os.path.dirname(os.path.abspath(__file__))
_pasta_raiz = os.path.dirname(_pasta_atual)
_caminho_env = os.path.join(_pasta_raiz, ".env")

if os.path.exists(_caminho_env):
    load_dotenv(_caminho_env)
else:
    load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

_cliente_supabase: Client | None = None


def obter_cliente() -> Client:
    """Retorna a instância do cliente Supabase ou inicializa caso ainda não exista.

    Lança ValueError com mensagem clara se as credenciais não estiverem
    configuradas.
    """
    global _cliente_supabase, SUPABASE_URL, SUPABASE_KEY

    if _cliente_supabase is not None:
        return _cliente_supabase

    # Atualiza as variáveis caso tenham sido carregadas posteriormente
    SUPABASE_URL = os.getenv("SUPABASE_URL")
    SUPABASE_KEY = os.getenv("SUPABASE_KEY")

    if (
        not SUPABASE_URL
        or not SUPABASE_KEY
        or "sua_url_aqui" in SUPABASE_URL
        or "sua_chave_aqui" in SUPABASE_KEY
    ):
        raise ValueError(
            "Credenciais do Supabase não encontradas ou inválidas!\n"
            "Preencha SUPABASE_URL e SUPABASE_KEY no arquivo .env."
        )

    try:
        _cliente_supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        return _cliente_supabase
    except Exception as erro:
        raise ConnectionError(
            f"Falha ao conectar ao Supabase: {erro}"
        ) from erro


# Inicialização segura para disponibilizar banco.supabase quando as credenciais existirem
supabase: Client | None = None
try:
    if (
        SUPABASE_URL
        and SUPABASE_KEY
        and "sua_url_aqui" not in SUPABASE_URL
        and "sua_chave_aqui" not in SUPABASE_KEY
    ):
        supabase = create_client(SUPABASE_URL, SUPABASE_KEY)
        _cliente_supabase = supabase
except Exception:
    supabase = None


# ==========================================
# FUNÇÕES DE COMUNICAÇÃO (RPC)
# ==========================================

def buscar_perguntas(dificuldade: str) -> list[dict]:
    """Busca no Supabase as perguntas da dificuldade informada, sem a resposta correta."""
    cliente = obter_cliente()
    try:
        resposta = cliente.rpc(
            "buscar_perguntas",
            {"p_dificuldade": dificuldade.lower().strip()}
        ).execute()
        return resposta.data or []
    except Exception as erro:
        raise ConnectionError(
            f"Erro ao buscar perguntas da dificuldade '{dificuldade}': {erro}"
        ) from erro


def validar_resposta(pergunta_id: int, resposta_jogador: str) -> bool:
    """Valida via RPC no Supabase se a resposta do jogador está correta."""
    cliente = obter_cliente()
    try:
        resposta = cliente.rpc(
            "validar_resposta",
            {
                "p_pergunta_id": int(pergunta_id),
                "p_resposta": resposta_jogador.upper().strip()
            }
        ).execute()
        return bool(resposta.data)
    except Exception as erro:
        raise ConnectionError(
            f"Erro ao validar resposta da pergunta {pergunta_id}: {erro}"
        ) from erro


def salvar_partida(resultado: dict) -> str:
    """Salva o resultado da partida no Supabase.

    Gera UUID na primeira tentativa e garante idempotência caso seja reenviado.
    """
    cliente = obter_cliente()

    # Gera um identificador único apenas na primeira tentativa
    if "id" not in resultado or not resultado["id"]:
        resultado["id"] = str(uuid.uuid4())

    try:
        resposta = cliente.rpc(
            "salvar_partida",
            {
                "p_id": resultado["id"],
                "p_apelido": resultado["apelido"],
                "p_valor_ganho": resultado["valor_ganho"],
                "p_tempo_segundos": resultado["tempo_segundos"],
                "p_acertos": resultado["acertos"],
                "p_motivo_encerramento": resultado["motivo_encerramento"]
            }
        ).execute()

        # O retorno é o próprio ID confirmado pelo banco
        return str(resposta.data) if resposta.data else resultado["id"]
    except Exception as erro:
        raise ConnectionError(
            f"Erro ao salvar partida no Supabase: {erro}"
        ) from erro


def buscar_ranking() -> list[dict]:
    """Consulta o ranking com os 10 melhores jogadores no Supabase."""
    cliente = obter_cliente()
    try:
        resposta = cliente.rpc("buscar_ranking").execute()
        return resposta.data or []
    except Exception as erro:
        raise ConnectionError(
            f"Erro ao consultar o ranking no Supabase: {erro}"
        ) from erro


# ==========================================
# GERENCIAMENTO DE PARTIDAS PENDENTES
# ==========================================

CAMINHO_PENDENTES = os.path.join(_pasta_atual, "partidas_pendentes.json")


def salvar_partida_localmente(resultado: dict) -> bool:
    """Salva localmente uma partida que não pôde ser enviada imediatamente ao Supabase."""
    try:
        pendentes = []
        if os.path.exists(CAMINHO_PENDENTES):
            try:
                with open(CAMINHO_PENDENTES, "r", encoding="utf-8") as f:
                    pendentes = json.load(f)
            except Exception:
                pendentes = []

        # Evita duplicatas locais baseado no id
        if not any(p.get("id") == resultado["id"] for p in pendentes):
            pendentes.append(resultado)

        with open(CAMINHO_PENDENTES, "w", encoding="utf-8") as f:
            json.dump(pendentes, f, indent=2, ensure_ascii=False)

        return True
    except Exception:
        return False


def sincronizar_partidas_pendentes() -> int:
    """Tenta enviar ao Supabase quaisquer partidas salvas localmente pendentes.

    Retorna a quantidade de partidas sincronizadas com sucesso.
    """
    if not os.path.exists(CAMINHO_PENDENTES):
        return 0

    try:
        with open(CAMINHO_PENDENTES, "r", encoding="utf-8") as f:
            pendentes = json.load(f)
    except Exception:
        return 0

    if not pendentes:
        return 0

    ainda_pendentes = []
    sincronizadas = 0

    for partida in pendentes:
        try:
            salvar_partida(partida)
            sincronizadas += 1
        except Exception:
            ainda_pendentes.append(partida)

    try:
        if ainda_pendentes:
            with open(CAMINHO_PENDENTES, "w", encoding="utf-8") as f:
                json.dump(ainda_pendentes, f, indent=2, ensure_ascii=False)
        else:
            os.remove(CAMINHO_PENDENTES)
    except Exception:
        pass

    return sincronizadas


# ==========================================
# TESTE DE FUNCIONAMENTO
# ==========================================

def testar_banco():
    print("CÓDIGO MILIONÁRIO — TESTE DE BANCO")
    print("==================================")

    try:
        perguntas = buscar_perguntas("facil")
        print(f"Perguntas fáceis encontradas: {len(perguntas)}")

        if perguntas:
            primeira = perguntas[0]
            print("\nExemplo:", primeira["enunciado"])
            print("A)", primeira["alternativa_a"])
            print("B)", primeira["alternativa_b"])
            print("C)", primeira["alternativa_c"])
            print("D)", primeira["alternativa_d"])

            teste_val = validar_resposta(primeira["id"], "B")
            print(f"\nTeste de validação (id={primeira['id']}, alt='B'): {teste_val}")

        ranking = buscar_ranking()
        print(f"\nTotal de registros no ranking: {len(ranking)}")

        print("\n==================================")
        print("Teste concluído com sucesso!")
    except Exception as erro:
        print("\nErro ao acessar o banco:", erro)


if __name__ == "__main__":
    testar_banco()
