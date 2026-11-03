import os
import sys

# Garante compatibilidade de saída com Windows e UTF-8
if hasattr(sys.stdout, "reconfigure"):
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except Exception:
        pass

_pasta_atual = os.path.dirname(os.path.abspath(__file__))
if _pasta_atual not in sys.path:
    sys.path.insert(0, _pasta_atual)

from teste_perguntas import testar_perguntas_locais, testar_perguntas_supabase
from teste_partida import executar_testes_partida
from teste_salvamento import testar_salvamento_e_duplicidade
from teste_ranking import testar_consulta_ranking


def executar_todos_os_testes():
    print("=" * 65)
    print("  SUITE UNIFICADA DE TESTES AUTOMATIZADOS - CODIGO MILIONARIO")
    print("=" * 65)

    resultados = {}

    # 1. Perguntas Locais
    try:
        ok_perguntas_locais = testar_perguntas_locais()
        resultados["Perguntas Locais (15 cadastradas, 5/5/5, 4 alternativas)"] = "Aprovado" if ok_perguntas_locais else "Falha"
    except Exception as e:
        resultados["Perguntas Locais"] = f"Erro ({e})"

    # 2. Perguntas Supabase RPC
    try:
        ok_perguntas_supabase = testar_perguntas_supabase()
        resultados["Perguntas Supabase (RPC buscar_perguntas com seguranca)"] = "Aprovado" if ok_perguntas_supabase else "Falha"
    except Exception as e:
        resultados["Perguntas Supabase"] = f"Erro ({e})"

    # 3. Lógica da Partida
    try:
        ok_partida = executar_testes_partida()
        resultados["Logica da Partida (Premiacao, 9 perguntas, Sorteio sem repeticao)"] = "Aprovado" if ok_partida else "Falha"
    except Exception as e:
        resultados["Logica da Partida"] = f"Erro ({e})"

    # 4. Salvamento e Idempotência no Supabase
    try:
        ok_salvamento = testar_salvamento_e_duplicidade()
        resultados["Salvamento e Idempotencia (UUID unico, sem duplicidades)"] = "Aprovado" if ok_salvamento else "Falha"
    except Exception as e:
        resultados["Salvamento e Idempotencia"] = f"Erro ({e})"

    # 5. Consulta e Ordenação do Ranking
    try:
        ok_ranking = testar_consulta_ranking()
        resultados["Consulta ao Ranking (Top 10, desempate por tempo e data)"] = "Aprovado" if ok_ranking else "Falha"
    except Exception as e:
        resultados["Consulta ao Ranking"] = f"Erro ({e})"

    # Resumo Final
    print("\n" + "=" * 65)
    print("  RESUMO DOS TESTES EXECUTADOS")
    print("=" * 65)
    todos_aprovados = True
    for item, status in resultados.items():
        simbolo = "[OK]" if status == "Aprovado" else "[X]"
        print(f"{simbolo} {item}: {status}")
        if status != "Aprovado":
            todos_aprovados = False

    print("=" * 65)
    if todos_aprovados:
        print("RESULTADO GERAL: 100% DOS TESTES AUTOMATIZADOS APROVADOS!")
    else:
        print("RESULTADO GERAL: ALGUNS TESTES APRESENTARAM FALHAS OU PENDENCIAS.")
    print("=" * 65)

    return todos_aprovados


if __name__ == "__main__":
    sucesso = executar_todos_os_testes()
    sys.exit(0 if sucesso else 1)
