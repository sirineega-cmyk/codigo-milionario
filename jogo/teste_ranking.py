import os
import sys

# Garante que as importações funcionem a partir de qualquer diretório
_pasta_atual = os.path.dirname(os.path.abspath(__file__))
if _pasta_atual not in sys.path:
    sys.path.insert(0, _pasta_atual)

from banco import buscar_ranking


def testar_consulta_ranking() -> bool:
    print("==================================================")
    print("TESTE: CONSULTA E ESTRUTURA DO RANKING (teste_ranking.py)")
    print("==================================================")

    try:
        ranking = buscar_ranking()

        print(f"Total de registros retornados: {len(ranking)} (máximo esperado: 10)")

        if len(ranking) > 10:
            print("[FALHA] O ranking retornou mais de 10 registros.")
            return False

        if not ranking:
            print("[AVISO] O ranking está vazio no momento (nenhuma partida registrada).")
            print("[APROVADO] Consulta executada sem erros!")
            return True

        erros = []
        apelidos_vistos = set()
        campos_obrigatorios = ["posicao", "apelido", "valor_ganho", "tempo_segundos", "acertos", "data_hora"]

        for idx, jogador in enumerate(ranking):
            # Validação dos campos
            for campo in campos_obrigatorios:
                if campo not in jogador:
                    erros.append(f"Registro {idx + 1} não possui o campo obrigatório '{campo}'.")

            # Validação de unicidade de apelido (apenas a melhor partida de cada jogador)
            apelido = str(jogador.get("apelido", "")).strip().lower()
            if apelido in apelidos_vistos:
                erros.append(f"Apelido duplicado no ranking: '{jogador.get('apelido')}'. Deve constar apenas a melhor partida.")
            else:
                apelidos_vistos.add(apelido)

        # Validação de ordenação: maior prêmio -> menor tempo -> data mais antiga
        for i in range(len(ranking) - 1):
            atual = ranking[i]
            proximo = ranking[i + 1]

            premio_atual = float(atual.get("valor_ganho", 0))
            premio_proximo = float(proximo.get("valor_ganho", 0))

            if premio_atual < premio_proximo:
                erros.append(f"Ordenação incorreta de prêmio: {premio_atual} veio antes de {premio_proximo}.")
            elif premio_atual == premio_proximo:
                tempo_atual = float(atual.get("tempo_segundos", 0))
                tempo_proximo = float(proximo.get("tempo_segundos", 0))
                if tempo_atual > tempo_proximo:
                    erros.append(f"Desempate por tempo incorreto: {tempo_atual}s veio antes de {tempo_proximo}s.")

        # Exibição dos resultados formatados
        print("\nClassificação atual obtida:")
        for j in ranking:
            print(f" - {j.get('posicao')}º | {j.get('apelido')} | R$ {j.get('valor_ganho')} | {j.get('acertos')}/9 acertos | {j.get('tempo_segundos')}s")

        if erros:
            print("\n[FALHA] Foram encontrados erros na estrutura do ranking:")
            for e in erros:
                print(" -", e)
            return False
        else:
            print("\n[APROVADO] Ranking validado com sucesso:")
            print(" - Campos obrigatórios presentes")
            print(" - Apenas a melhor partida de cada jogador")
            print(" - Ordenação correta por prêmio e desempate por tempo")
            return True

    except Exception as erro:
        print("\n[FALHA / ERRO] Erro ao consultar o ranking no Supabase:")
        print(f"Detalhes: {erro}")
        return False


if __name__ == "__main__":
    sucesso = testar_consulta_ranking()
    sys.exit(0 if sucesso else 1)