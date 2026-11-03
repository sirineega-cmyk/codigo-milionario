import os
import sys

# Garante que as importações internas funcionem tanto a partir da raiz quanto de jogo/
_pasta_atual = os.path.dirname(os.path.abspath(__file__))
if _pasta_atual not in sys.path:
    sys.path.insert(0, _pasta_atual)

from partida import iniciar_partida, formatar_dinheiro
from banco import buscar_ranking, sincronizar_partidas_pendentes


def formatar_tempo(segundos: float | int) -> str:
    """Formata segundos em formato 'Xmin YYs' ou 'Xs'."""
    total = int(round(segundos))
    minutos = total // 60
    resto = total % 60
    if minutos > 0:
        return f"{minutos}min {resto:02d}s ({segundos:.2f}s)"
    return f"{segundos:.2f}s"


def exibir_ranking():
    """Exibe o ranking dos 10 melhores jogadores obtido do Supabase."""
    print("\n=======================================================")
    print("           RANKING OFICIAL — CÓDIGO MILIONÁRIO")
    print("=======================================================")

    # Sincroniza partidas que possam ter ficado pendentes em falhas anteriores
    sincronizadas = sincronizar_partidas_pendentes()
    if sincronizadas > 0:
        print(f"[{sincronizadas} partida(s) pendente(s) sincronizada(s) com o Supabase]")

    try:
        ranking = buscar_ranking()

        if not ranking:
            print("\nAinda não existem partidas registradas no ranking.")
            print("Seja o primeiro a jogar e conquistar o prêmio!")
        else:
            print(f"\n{'POS':<5} | {'JOGADOR':<18} | {'PRÊMIO':<14} | {'ACERTOS':<8} | {'TEMPO'}")
            print("-" * 65)

            for jogador in ranking:
                posicao = f"{jogador.get('posicao', 0)}º"
                apelido = str(jogador.get("apelido", ""))[:18]
                premio = formatar_dinheiro(jogador.get("valor_ganho", 0))
                acertos = f"{jogador.get('acertos', 0)}/9"
                tempo = formatar_tempo(jogador.get("tempo_segundos", 0))

                print(f"{posicao:<5} | {apelido:<18} | {premio:<14} | {acertos:<8} | {tempo}")

        print("=======================================================")

    except Exception as erro:
        print("\nNão foi possível consultar o ranking.")
        print(f"Detalhes: {erro}")
        print("Verifique sua conexão e se o Supabase está configurado corretamente.")


def exibir_menu():
    """Exibe as opções do menu principal."""
    print("\n===================================")
    print("         CÓDIGO MILIONÁRIO")
    print("===================================")
    print("1 - Iniciar partida")
    print("2 - Consultar ranking")
    print("3 - Sair")
    print("===================================")


def executar_menu():
    """Loop principal de navegação do menu."""
    # Sincroniza partidas locais pendentes ao iniciar o jogo
    try:
        sincronizar_partidas_pendentes()
    except Exception:
        pass

    while True:
        exibir_menu()
        opcao = input("\nEscolha uma opção (1, 2 ou 3): ").strip()

        if opcao == "1":
            iniciar_partida()
        elif opcao == "2":
            exibir_ranking()
        elif opcao == "3":
            print("\nObrigado por jogar o Código Milionário! Até a próxima.")
            break
        else:
            print("\nOpção inválida! Por favor, digite 1, 2 ou 3.")


if __name__ == "__main__":
    executar_menu()