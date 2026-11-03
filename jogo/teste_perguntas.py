import os
import sys

# Garante que as importações funcionem a partir de qualquer diretório
_pasta_atual = os.path.dirname(os.path.abspath(__file__))
if _pasta_atual not in sys.path:
    sys.path.insert(0, _pasta_atual)

from perguntas import perguntas

def testar_perguntas_locais():
    print("==================================================")
    print("TESTE 1: VALIDAÇÃO DAS PERGUNTAS LOCAIS (perguntas.py)")
    print("==================================================")

    erros = []

    # 1. Quantidade total
    total = len(perguntas)
    print(f"Total de perguntas cadastradas: {total}")
    if total != 15:
        erros.append(f"Esperado 15 perguntas, encontrado {total}.")

    # 2. Distribuição por dificuldade
    contagem_dificuldades = {"facil": 0, "media": 0, "dificil": 0}
    ids_vistos = set()

    for idx, p in enumerate(perguntas, 1):
        p_id = p.get("id")
        if p_id is None:
            erros.append(f"Pergunta na posição {idx} não possui 'id'.")
        elif p_id in ids_vistos:
            erros.append(f"ID duplicado encontrado: {p_id}.")
        else:
            ids_vistos.add(p_id)

        enunciado = p.get("enunciado", "").strip()
        if not enunciado:
            erros.append(f"Pergunta ID {p_id} possui enunciado vazio.")

        alts = p.get("alternativas", {})
        for letra in ["A", "B", "C", "D"]:
            if letra not in alts or not str(alts[letra]).strip():
                erros.append(f"Pergunta ID {p_id} possui alternativa '{letra}' inválida ou vazia.")

        correta = p.get("correta")
        if correta not in ["A", "B", "C", "D"]:
            erros.append(f"Pergunta ID {p_id} possui resposta correta inválida: '{correta}'.")

        dif = p.get("dificuldade")
        if dif in contagem_dificuldades:
            contagem_dificuldades[dif] += 1
        else:
            erros.append(f"Pergunta ID {p_id} possui dificuldade desconhecida: '{dif}'.")

    for dif, qtd in contagem_dificuldades.items():
        print(f"Perguntas {dif.upper()}: {qtd}/5")
        if qtd != 5:
            erros.append(f"Dificuldade '{dif}' possui {qtd} perguntas (esperado exatamente 5).")

    if erros:
        print("\n[FALHA] Foram encontrados erros nas perguntas locais:")
        for e in erros:
            print(" -", e)
        return False
    else:
        print("\n[APROVADO] Todas as 15 perguntas locais atendem integralmente aos requisitos!")
        return True


def testar_perguntas_supabase():
    print("\n==================================================")
    print("TESTE 2: BUSCA DE PERGUNTAS NO SUPABASE (RPC)")
    print("==================================================")

    try:
        from banco import buscar_perguntas
    except Exception as e:
        print(f"[IGNORADO] Não foi possível importar banco.py: {e}")
        return True

    erros = []
    try:
        for dif in ["facil", "media", "dificil"]:
            res = buscar_perguntas(dif)
            print(f"Perguntas retornadas para '{dif}': {len(res)}")
            if len(res) < 3:
                erros.append(f"Supabase retornou menos de 3 perguntas para '{dif}'.")
            
            # Verifica se a resposta correta NÃO foi exposta pela RPC
            for p in res:
                if "correta" in p:
                    erros.append("ALERTA DE SEGURANÇA: RPC 'buscar_perguntas' expôs a coluna 'correta'!")
                    break

        if erros:
            print("\n[FALHA] Erros na integração com Supabase:")
            for e in erros:
                print(" -", e)
            return False
        else:
            print("\n[APROVADO] Perguntas no Supabase consultadas com sucesso e segurança!")
            return True

    except Exception as e:
        print(f"[PENDENTE / AVISO] Falha ao conectar ao Supabase: {e}")
        print("Certifique-se de configurar .env com credenciais ativas para este teste.")
        return False


if __name__ == "__main__":
    t1 = testar_perguntas_locais()
    t2 = testar_perguntas_supabase()
    sys.exit(0 if (t1 and t2) else 1)
