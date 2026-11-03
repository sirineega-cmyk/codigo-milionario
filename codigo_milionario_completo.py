"""========================================================================

CÓDIGO MILIONÁRIO — VERSÃO INTEGRADA EM ARQUIVO ÚNICO (.PY)
========================================================================
Este arquivo reúne todas as camadas do projeto (Banco de Dados Supabase,
Perguntas, Regras de Partida, Cronômetro e Menu Interativo) em um único
script Python auto-suficiente, ideal para entrega acadêmica e execução
direta sem dependência de módulos externos locais.

Tecnologias: Python 3.10+, Supabase, PostgreSQL.
========================================================================"""

import os
import sys
import time
import json
import uuid
import random

# Certificados seguros para evitar erros de SSL
try:
    import truststore
    truststore.inject_into_ssl()
except Exception:
    pass

# Tratamento de encoding UTF-8 no terminal Windows
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

# Importações de bibliotecas externas
try:
    from dotenv import load_dotenv
    from supabase import create_client, Client
except ImportError:
    print("Aviso: Bibliotecas 'supabase' ou 'python-dotenv' não encontradas.")
    print("Instale com: pip install supabase python-dotenv truststore")
    create_client = None
    Client = None
    load_dotenv = lambda *args, **kwargs: None


# ========================================================================
# 1. BASE DE PERGUNTAS OFICIAIS (15 PERGUNTAS — 5 POR DIFICULDADE)
# ========================================================================

PERGUNTAS_BASE = [
    # Fáceis (1 a 5)
    {
        "id": 1,
        "enunciado": "Qual função do Python é utilizada para exibir informações na tela?",
        "alternativa_a": "input()",
        "alternativa_b": "print()",
        "alternativa_c": "display()",
        "alternativa_d": "show()",
        "correta": "B",
        "dificuldade": "facil"
    },
    {
        "id": 2,
        "enunciado": "Qual tipo de dado representa um número inteiro em Python?",
        "alternativa_a": "str",
        "alternativa_b": "float",
        "alternativa_c": "int",
        "alternativa_d": "bool",
        "correta": "C",
        "dificuldade": "facil"
    },
    {
        "id": 3,
        "enunciado": "Qual comando é utilizado para criar uma condição em Python?",
        "alternativa_a": "if",
        "alternativa_b": "for",
        "alternativa_c": "def",
        "alternativa_d": "import",
        "correta": "A",
        "dificuldade": "facil"
    },
    {
        "id": 4,
        "enunciado": "Qual estrutura de dados permite armazenar vários elementos em uma sequência modificável?",
        "alternativa_a": "Tupla",
        "alternativa_b": "String",
        "alternativa_c": "Lista",
        "alternativa_d": "Inteiro",
        "correta": "C",
        "dificuldade": "facil"
    },
    {
        "id": 5,
        "enunciado": "O que significa a sigla IA?",
        "alternativa_a": "Internet Automatizada",
        "alternativa_b": "Inteligência Artificial",
        "alternativa_c": "Informação Avançada",
        "alternativa_d": "Interface Automática",
        "correta": "B",
        "dificuldade": "facil"
    },

    # Médias (6 a 10)
    {
        "id": 6,
        "enunciado": "Qual será o resultado do código: print(10 // 3)?",
        "alternativa_a": "3.33",
        "alternativa_b": "3",
        "alternativa_c": "1",
        "alternativa_d": "4",
        "correta": "B",
        "dificuldade": "media"
    },
    {
        "id": 7,
        "enunciado": "Qual método adiciona um elemento ao final de uma lista em Python?",
        "alternativa_a": "add()",
        "alternativa_b": "insert_end()",
        "alternativa_c": "append()",
        "alternativa_d": "extend_one()",
        "correta": "C",
        "dificuldade": "media"
    },
    {
        "id": 8,
        "enunciado": "Qual é a principal finalidade de uma chave primária em um banco de dados?",
        "alternativa_a": "Identificar exclusivamente cada registro",
        "alternativa_b": "Armazenar imagens",
        "alternativa_c": "Ordenar automaticamente todas as tabelas",
        "alternativa_d": "Impedir qualquer alteração nos dados",
        "correta": "A",
        "dificuldade": "media"
    },
    {
        "id": 9,
        "enunciado": "Qual estrutura de dados armazena informações em pares de chave e valor?",
        "alternativa_a": "Lista",
        "alternativa_b": "Tupla",
        "alternativa_c": "Conjunto",
        "alternativa_d": "Dicionário",
        "correta": "D",
        "dificuldade": "media"
    },
    {
        "id": 10,
        "enunciado": "No contexto de Machine Learning, o que é um conjunto de treinamento?",
        "alternativa_a": "Um conjunto de dados utilizado para ensinar o modelo",
        "alternativa_b": "Uma lista de comandos para desligar o computador",
        "alternativa_c": "Um banco de dados contendo apenas resultados finais",
        "alternativa_d": "Um programa responsável por instalar bibliotecas",
        "correta": "A",
        "dificuldade": "media"
    },

    # Difíceis (11 a 15)
    {
        "id": 11,
        "enunciado": "Qual será a saída do código Python: print([x**2 for x in range(4)])?",
        "alternativa_a": "[1, 4, 9, 16]",
        "alternativa_b": "[0, 1, 2, 3]",
        "alternativa_c": "[0, 1, 4, 9]",
        "alternativa_d": "[0, 2, 4, 6]",
        "correta": "C",
        "dificuldade": "dificil"
    },
    {
        "id": 12,
        "enunciado": "Qual é a principal diferença entre uma lista e uma tupla em Python?",
        "alternativa_a": "Listas armazenam apenas números",
        "alternativa_b": "Tuplas são imutáveis, enquanto listas são mutáveis",
        "alternativa_c": "Tuplas não permitem elementos repetidos",
        "alternativa_d": "Listas não permitem armazenar strings",
        "correta": "B",
        "dificuldade": "dificil"
    },
    {
        "id": 13,
        "enunciado": "O que caracteriza o overfitting em um modelo de Machine Learning?",
        "alternativa_a": "O modelo não consegue aprender nenhum padrão",
        "alternativa_b": "O modelo apresenta o mesmo desempenho em todos os conjuntos",
        "alternativa_c": "O modelo aprende apenas dados novos",
        "alternativa_d": "O modelo se ajusta excessivamente aos dados de treinamento e generaliza mal",
        "correta": "D",
        "dificuldade": "dificil"
    },
    {
        "id": 14,
        "enunciado": "Qual é a finalidade principal do comando JOIN em SQL?",
        "alternativa_a": "Excluir registros duplicados",
        "alternativa_b": "Combinar dados de duas ou mais tabelas relacionadas",
        "alternativa_c": "Criar uma nova senha para o banco",
        "alternativa_d": "Modificar o tipo de dado de uma coluna",
        "correta": "B",
        "dificuldade": "dificil"
    },
    {
        "id": 15,
        "enunciado": "Em Python, o que acontece quando uma função encontra o comando return?",
        "alternativa_a": "A função retorna um resultado e encerra sua execução",
        "alternativa_b": "O programa inteiro é encerrado obrigatoriamente",
        "alternativa_c": "A função reinicia automaticamente",
        "alternativa_d": "O comando imprime o resultado na tela",
        "correta": "A",
        "dificuldade": "dificil"
    }
]


# ========================================================================
# 2. CONFIGURAÇÕES, PREMIAÇÕES E BANCO DE DADOS
# ========================================================================

PREMIOS = [
    1000,
    5000,
    10000,
    25000,
    50000,
    100000,
    200000,
    500000,
    1000000
]

DIFICULDADES = ["facil", "media", "dificil"]

# Carrega .env
load_dotenv(os.path.join(os.path.dirname(os.path.abspath(__file__)), ".env"))
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")

_cliente = None


def obter_cliente_supabase():
    global _cliente
    if _cliente is not None:
        return _cliente

    url = os.getenv("SUPABASE_URL")
    key = os.getenv("SUPABASE_KEY")

    if not url or not key or "sua_url_aqui" in url or create_client is None:
        return None

    try:
        _cliente = create_client(url, key)
        return _cliente
    except Exception:
        return None


def formatar_dinheiro(valor: float | int) -> str:
    """Formata valor no padrão Real brasileiro (R$ X.XXX,XX)."""
    formatado = f"{valor:,.2f}"
    formatado = formatado.replace(",", "X").replace(".", ",").replace("X", ".")
    return f"R$ {formatado}"


def formatar_tempo(segundos: float | int) -> str:
    total = int(round(segundos))
    minutos = total // 60
    resto = total % 60
    if minutos > 0:
        return f"{minutos}min {resto:02d}s ({segundos:.2f}s)"
    return f"{segundos:.2f}s"


def calcular_premio(acertos: int) -> int:
    if acertos <= 0:
        return 0
    if acertos > len(PREMIOS):
        return PREMIOS[-1]
    return PREMIOS[acertos - 1]


# ========================================================================
# 3. COMUNICAÇÃO COM O SUPABASE (OU MODO LOCAL TRANSPARENTE)
# ========================================================================

def buscar_perguntas_banco(dificuldade: str) -> list[dict]:
    cliente = obter_cliente_supabase()
    if cliente:
        try:
            res = cliente.rpc("buscar_perguntas", {"p_dificuldade": dificuldade}).execute()
            if res.data and len(res.data) >= 3:
                return res.data
        except Exception:
            pass

    # Fallback local transparente se não houver conexão com o banco
    filtradas = [
        {
            "id": p["id"],
            "enunciado": p["enunciado"],
            "alternativa_a": p["alternativa_a"],
            "alternativa_b": p["alternativa_b"],
            "alternativa_c": p["alternativa_c"],
            "alternativa_d": p["alternativa_d"],
            "dificuldade": p["dificuldade"]
        }
        for p in PERGUNTAS_BASE if p["dificuldade"] == dificuldade
    ]
    return filtradas


def validar_resposta_banco(pergunta_id: int, resposta: str) -> bool:
    cliente = obter_cliente_supabase()
    if cliente:
        try:
            res = cliente.rpc(
                "validar_resposta",
                {"p_pergunta_id": pergunta_id, "p_resposta": resposta.upper().strip()}
            ).execute()
            return bool(res.data)
        except Exception:
            pass

    # Validação local de fallback
    for p in PERGUNTAS_BASE:
        if p["id"] == pergunta_id:
            return p["correta"] == resposta.upper().strip()
    return False


def salvar_partida_banco(resultado: dict) -> bool:
    if "id" not in resultado or not resultado["id"]:
        resultado["id"] = str(uuid.uuid4())

    cliente = obter_cliente_supabase()
    if cliente:
        try:
            cliente.rpc(
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
            print("\nPartida salva no ranking online do Supabase com sucesso!")
            return True
        except Exception as e:
            print("\nNão foi possível sincronizar imediatamente com o Supabase:", e)

    # Salva em arquivo local para não perder o resultado
    caminho_local = os.path.join(os.path.dirname(os.path.abspath(__file__)), "partidas_pendentes.json")
    try:
        partidas = []
        if os.path.exists(caminho_local):
            with open(caminho_local, "r", encoding="utf-8") as f:
                partidas = json.load(f)
        if not any(p.get("id") == resultado["id"] for p in partidas):
            partidas.append(resultado)
            with open(caminho_local, "w", encoding="utf-8") as f:
                json.dump(partidas, f, indent=2, ensure_ascii=False)
        print("Resultado salvo com segurança localmente em 'partidas_pendentes.json'.")
        return True
    except Exception:
        return False


def buscar_ranking_banco() -> list[dict]:
    cliente = obter_cliente_supabase()
    if cliente:
        try:
            res = cliente.rpc("buscar_ranking").execute()
            if res.data:
                return res.data
        except Exception:
            pass

    # Carrega partidas locais se houver
    caminho_local = os.path.join(os.path.dirname(os.path.abspath(__file__)), "partidas_pendentes.json")
    if os.path.exists(caminho_local):
        try:
            with open(caminho_local, "r", encoding="utf-8") as f:
                partidas = json.load(f)
            # Ordena por valor DESC, tempo ASC
            partidas.sort(key=lambda x: (-x.get("valor_ganho", 0), x.get("tempo_segundos", 9999)))
            for idx, p in enumerate(partidas[:10], 1):
                p["posicao"] = idx
            return partidas[:10]
        except Exception:
            pass
    return []


# ========================================================================
# 4. REGRAS DA PARTIDA E CRONÔMETRO
# ========================================================================

def sortear_perguntas() -> list[dict]:
    """Sorteia exatamente 9 perguntas: 3 fáceis, 3 médias e 3 difíceis (sem repetição)."""
    sorteadas = []
    for dif in DIFICULDADES:
        perguntas = buscar_perguntas_banco(dif)
        if len(perguntas) < 3:
            raise ValueError(f"Perguntas insuficientes para a dificuldade '{dif}'.")
        sorteadas.extend(random.sample(perguntas, 3))
    return sorteadas


def iniciar_partida():
    print("\n===================================")
    print("       CÓDIGO MILIONÁRIO")
    print("===================================")

    # 1. Solicitação do apelido
    while True:
        apelido = input("\nDigite seu apelido: ").strip()
        if apelido:
            break
        print("O apelido não pode ficar vazio! Por favor, informe um nome ou apelido.")

    print(f"\nBoa sorte, {apelido}!")
    print("Responda corretamente a 9 perguntas para conquistar R$ 1.000.000,00!")

    try:
        perguntas = sortear_perguntas()
    except Exception as e:
        print("\nErro ao carregar perguntas:", e)
        return None

    acertos = 0
    valor_ganho = 0
    motivo_encerramento = "concluida"
    tempo_total_jogador = 0.0

    # 2. Execução das 9 perguntas
    for indice, pergunta in enumerate(perguntas):
        numero = indice + 1
        premio_da_pergunta = PREMIOS[indice]

        print("\n===================================")
        print(f"PERGUNTA {numero}/9 ({pergunta.get('dificuldade', '').upper()})")
        print(f"VALOR DESTA PERGUNTA: {formatar_dinheiro(premio_da_pergunta)}")
        print(f"PRÊMIO ATUAL GARANTIDO: {formatar_dinheiro(valor_ganho)}")
        print("===================================")

        print(f"\n{pergunta['enunciado']}\n")
        print(f"A) {pergunta['alternativa_a']}")
        print(f"B) {pergunta['alternativa_b']}")
        print(f"C) {pergunta['alternativa_c']}")
        print(f"D) {pergunta['alternativa_d']}")

        # O cronômetro mede com precisão apenas o tempo de reflexão e resposta do jogador
        t_inicio = time.perf_counter()
        resposta = input("\nSua resposta (A, B, C, D) ou [S] para parar: ").strip().upper()
        t_fim = time.perf_counter()
        tempo_total_jogador += (t_fim - t_inicio)

        # Regra obrigatória: entrada inválida encerra imediatamente
        if resposta not in ["A", "B", "C", "D", "S"]:
            print(f"\nEntrada inválida ('{resposta}')! A partida foi encerrada conforme as regras.")
            motivo_encerramento = "entrada_invalida"
            break

        # Desistência voluntária
        if resposta == "S":
            print("\nVocê decidiu parar a partida e garantir seu prêmio!")
            motivo_encerramento = "desistencia"
            break

        # Validação da resposta
        correta = validar_resposta_banco(pergunta["id"], resposta)

        if correta:
            acertos += 1
            valor_ganho = calcular_premio(acertos)
            print("\n✔ RESPOSTA CORRETA!")
            print(f"Prêmio garantido atualizado: {formatar_dinheiro(valor_ganho)}")
        else:
            print("\n✖ RESPOSTA INCORRETA!")
            print("A partida terminou.")
            motivo_encerramento = "erro"
            # O jogador mantém o prêmio dos acertos anteriores
            break

    if acertos == 9:
        print("\n🎉 PARABÉNS! VOCÊ ACERTOU TODAS AS 9 PERGUNTAS!")
        print("🏆 VOCÊ É O NOVO CÓDIGO MILIONÁRIO!")

    # 3. Resumo da partida
    print("\n===================================")
    print("          FIM DE JOGO")
    print("===================================")
    print("Jogador:", apelido)
    print("Acertos:", f"{acertos}/9")
    print("Prêmio final:", formatar_dinheiro(valor_ganho))
    print(f"Tempo de jogo: {tempo_total_jogador:.2f} segundos")
    print("Motivo do encerramento:", motivo_encerramento)
    print("===================================")

    resultado = {
        "id": str(uuid.uuid4()),
        "apelido": apelido,
        "acertos": acertos,
        "valor_ganho": valor_ganho,
        "tempo_segundos": round(tempo_total_jogador, 2),
        "motivo_encerramento": motivo_encerramento
    }

    salvar_partida_banco(resultado)
    return resultado


# ========================================================================
# 5. MENU PRINCIPAL E RANKING
# ========================================================================

def exibir_ranking():
    print("\n=======================================================")
    print("           RANKING OFICIAL — CÓDIGO MILIONÁRIO")
    print("=======================================================")

    ranking = buscar_ranking_banco()

    if not ranking:
        print("\nAinda não existem partidas registradas no ranking.")
    else:
        print(f"\n{'POS':<5} | {'JOGADOR':<18} | {'PRÊMIO':<14} | {'ACERTOS':<8} | {'TEMPO'}")
        print("-" * 65)
        for j in ranking:
            pos = f"{j.get('posicao', 0)}º"
            apelido = str(j.get("apelido", ""))[:18]
            premio = formatar_dinheiro(j.get("valor_ganho", 0))
            acertos = f"{j.get('acertos', 0)}/9"
            tempo = formatar_tempo(j.get("tempo_segundos", 0))
            print(f"{pos:<5} | {apelido:<18} | {premio:<14} | {acertos:<8} | {tempo}")

    print("=======================================================")


def menu_principal():
    while True:
        print("\n===================================")
        print("         CÓDIGO MILIONÁRIO")
        print("===================================")
        print("1 - Iniciar partida")
        print("2 - Consultar ranking")
        print("3 - Sair")
        print("===================================")

        opcao = input("\nEscolha uma opção (1, 2 ou 3): ").strip()

        if opcao == "1":
            iniciar_partida()
        elif opcao == "2":
            exibir_ranking()
        elif opcao == "3":
            print("\nObrigado por jogar o Código Milionário! Até a próxima.")
            break
        else:
            print("\nOpção inválida! Escolha 1, 2 ou 3.")


if __name__ == "__main__":
    menu_principal()
