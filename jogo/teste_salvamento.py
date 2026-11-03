import os
import sys
import uuid

# Garante que as importações funcionem a partir de qualquer diretório
_pasta_atual = os.path.dirname(os.path.abspath(__file__))
if _pasta_atual not in sys.path:
    sys.path.insert(0, _pasta_atual)

from banco import salvar_partida


def testar_salvamento_e_duplicidade() -> bool:
    print("==================================================")
    print("TESTE: SALVAMENTO E PREVENÇÃO DE DUPLICIDADE (teste_salvamento.py)")
    print("==================================================")

    id_teste = str(uuid.uuid4())
    resultado_teste = {
        "id": id_teste,
        "apelido": "JogadorTesteQA",
        "acertos": 5,
        "valor_ganho": 50000,
        "tempo_segundos": 42.5,
        "motivo_encerramento": "erro"
    }

    try:
        # 1. Primeira tentativa de salvamento
        print(f"Enviando 1ª tentativa com ID: {id_teste}...")
        resposta_1 = salvar_partida(resultado_teste)
        print(f"[OK] Primeira tentativa concluída com sucesso! ID retornado: {resposta_1}")

        # 2. Segunda tentativa com o mesmo identificador (idempotência)
        print(f"\nEnviando 2ª tentativa com o MESMO ID: {id_teste}...")
        resposta_2 = salvar_partida(resultado_teste)
        print(f"[OK] Segunda tentativa concluída sem erro! ID retornado: {resposta_2}")

        if str(resposta_1) == str(resposta_2) == id_teste:
            print("\n[APROVADO] Prevenção de duplicidade confirmada!")
            print("O banco aceitou a repetição sem gerar registros duplicados ou erros.")
            return True
        else:
            print("\n[FALHA] Discrepância nos IDs retornados.")
            return False

    except Exception as erro:
        print("\n[FALHA / ERRO] Não foi possível salvar a partida no Supabase:")
        print(f"Detalhes: {erro}")
        return False


if __name__ == "__main__":
    sucesso = testar_salvamento_e_duplicidade()
    sys.exit(0 if sucesso else 1)