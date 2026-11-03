import os
import sys
import time
import uuid
import random

# Garante que as importações internas funcionem tanto a partir da raiz quanto de jogo/
_pasta_atual = os.path.dirname(os.path.abspath(__file__))
if _pasta_atual not in sys.path:
    sys.path.insert(0, _pasta_atual)

from banco import (
    buscar_perguntas,
    validar_resposta,
    salvar_partida,
    salvar_partida_localmente
)


# ==========================================
# CONFIGURAÇÕES DO JOGO
# ==========================================

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

DIFICULDADES = [
    "facil",
    "media",
    "dificil"
]


# ==========================================
# FORMATAÇÃO MONETÁRIA
# ==========================================

def formatar_dinheiro(valor: float | int) -> str:
    """Formata um valor numérico para o padrão de moeda brasileiro (R$ X.XXX,XX)."""
    valor_formatado = f"{valor:,.2f}"
    valor_formatado = (
        valor_formatado
        .replace(",", "X")
        .replace(".", ",")
        .replace("X", ".")
    )
    return f"R$ {valor_formatado}"


# ==========================================
# SORTEIO DE PERGUNTAS
# ==========================================

def sortear_perguntas() -> list[dict]:
    """Sorteia exatamente 9 perguntas do banco (3 fáceis, 3 médias e 3 difíceis, nessa ordem).

    Garante que não haja repetições durante a partida.
    """
    perguntas_sorteadas = []

    for dificuldade in DIFICULDADES:
        perguntas = buscar_perguntas(dificuldade)

        if perguntas is None or len(perguntas) < 3:
            raise ValueError(
                f"Não existem perguntas suficientes cadastradas para a dificuldade '{dificuldade}' (mínimo necessário: 3)."
            )

        # random.sample garante seleção sem repetição dentro da dificuldade
        sorteadas = random.sample(perguntas, 3)
        perguntas_sorteadas.extend(sorteadas)

    return perguntas_sorteadas


# ==========================================
# CÁLCULO DE PRÊMIO
# ==========================================

def calcular_premio(acertos: int) -> int:
    """Calcula o prêmio conquistado de acordo com a quantidade de acertos (0 a 9)."""
    if acertos <= 0:
        return 0
    if acertos > len(PREMIOS):
        return PREMIOS[-1]
    return PREMIOS[acertos - 1]


# ==========================================
# SALVAMENTO DO RESULTADO
# ==========================================

def salvar_resultado(resultado: dict) -> bool:
    """Salva o resultado da partida no Supabase.

    Permite novas tentativas em caso de erro e, se o salvamento online
    não for confirmado, salva o resultado localmente para que nenhuma pontuação seja perdida.
    """
    # Garante a existência do identificador único (UUID) para evitar duplicatas
    if "id" not in resultado or not resultado["id"]:
        resultado["id"] = str(uuid.uuid4())

    while True:
        try:
            salvar_partida(resultado)
            print("\nPartida salva no ranking com sucesso!")
            return True

        except Exception as erro:
            print("\nNão foi possível salvar a partida no Supabase.")
            print("Detalhes do erro:", erro)

            while True:
                opcao = input(
                    "\nDeseja tentar salvar novamente no Supabase? (S/N): "
                ).strip().upper()

                if opcao in ["S", "N"]:
                    break
                print("Opção inválida! Digite S para tentar novamente ou N para continuar.")

            if opcao == "N":
                # Salva localmente em arquivo JSON para sincronização futura
                salvou_local = salvar_partida_localmente(resultado)
                print("\nA partida não pôde ser enviada ao Supabase neste momento.")
                if salvou_local:
                    print("O resultado foi armazenado localmente em 'partidas_pendentes.json'")
                    print("e será enviado na próxima sincronização quando a conexão for reestabelecida.")
                print("Identificador da partida:", resultado["id"])
                return False


# ==========================================
# FLUXO DA PARTIDA
# ==========================================

def iniciar_partida() -> dict | None:
    """Executa o ciclo completo de uma partida de Código Milionário.

    Regras atendidas:
    - Apelido não vazio (sem dados pessoais desnecessários).
    - 9 perguntas: 3 fáceis, 3 médias e 3 difíceis (sem repetição).
    - Cronômetro inicia na 1ª pergunta e desconsidera menus, conexão e salvamento.
    - Término ao errar, parar voluntariamente, entrada inválida ou concluir 9 perguntas.
    - Ao errar, encerra e garante o prêmio dos acertos anteriores.
    - Salvamento único do resultado.
    """
    print("\n===================================")
    print("       CÓDIGO MILIONÁRIO")
    print("===================================")

    # 1. Solicitação de apelido do jogador
    while True:
        apelido = input("\nDigite seu apelido: ").strip()
        if apelido:
            break
        print("O apelido não pode ficar vazio! Por favor, digite um nome ou apelido.")

    print(f"\nBoa sorte, {apelido}!")
    print("Responda corretamente a 9 perguntas para conquistar R$ 1.000.000,00!")

    # 2. Carregamento e sorteio das perguntas
    try:
        perguntas = sortear_perguntas()
    except Exception as erro:
        print("\nErro ao carregar as perguntas do banco de dados:")
        print(f"Detalhes: {erro}")
        print("Verifique a conexão com a internet e as credenciais do Supabase.")
        return None

    acertos = 0
    valor_ganho = 0
    motivo_encerramento = "concluida"
    tempo_total_jogador = 0.0

    # 3. Execução das 9 perguntas
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

        # O cronômetro mede com precisão o tempo ativo de resposta do jogador,
        # desconsiderando o tempo de conexão, menus e salvamento.
        t_inicio = time.perf_counter()
        resposta = input(
            "\nSua resposta (A, B, C, D) ou [S] para parar: "
        ).strip().upper()
        t_fim = time.perf_counter()
        tempo_total_jogador += (t_fim - t_inicio)

        # Regra: Entrada inválida encerra imediatamente a partida
        if resposta not in ["A", "B", "C", "D", "S"]:
            print("\nEntrada inválida!")
            print(f"Você digitou '{resposta}'. De acordo com as regras, a partida será encerrada.")
            motivo_encerramento = "entrada_invalida"
            break

        # Regra: Desistência voluntária
        if resposta == "S":
            print("\nVocê decidiu parar a partida e garantir seu prêmio!")
            motivo_encerramento = "desistencia"
            break

        # Validação da resposta no Supabase (com tratamento de falhas temporárias)
        correta = False
        while True:
            try:
                correta = validar_resposta(pergunta["id"], resposta)
                break
            except Exception as erro:
                print("\nFalha de comunicação com o servidor ao validar a resposta.")
                print(f"Detalhes: {erro}")
                tentar = input("Deseja tentar validar novamente? (S/N): ").strip().upper()
                if tentar != "S":
                    motivo_encerramento = "falha_conexao"
                    break

        if motivo_encerramento == "falha_conexao":
            print("\nPartida encerrada devido à falha de conexão.")
            break

        # Avaliação do acerto
        if correta:
            acertos += 1
            valor_ganho = calcular_premio(acertos)
            print("\n✔ RESPOSTA CORRETA!")
            print(f"Novo prêmio garantido: {formatar_dinheiro(valor_ganho)}")
        else:
            print("\n✖ RESPOSTA INCORRETA!")
            print("A partida terminou.")
            motivo_encerramento = "erro"
            # O jogador encerra a partida e mantém o prêmio dos acertos anteriores
            break

    # Mensagem de consagração se completou as 9 perguntas
    if acertos == 9:
        print("\n🎉 PARABÉNS! VOCÊ RESPONDEU CORRETAMENTE TODAS AS 9 PERGUNTAS!")
        print("🏆 VOCÊ É O NOVO CÓDIGO MILIONÁRIO!")

    # 4. Apresentação do resumo final da partida
    print("\n===================================")
    print("          FIM DE JOGO")
    print("===================================")
    print("Jogador:", apelido)
    print("Acertos:", f"{acertos}/9")
    print("Prêmio final:", formatar_dinheiro(valor_ganho))
    print(f"Tempo de jogo: {tempo_total_jogador:.2f} segundos")
    print("Motivo do encerramento:", motivo_encerramento)
    print("===================================")

    # 5. Estruturação dos dados e salvamento com proteção contra duplicidade
    resultado = {
        "id": str(uuid.uuid4()),
        "apelido": apelido,
        "acertos": acertos,
        "valor_ganho": valor_ganho,
        "tempo_segundos": round(tempo_total_jogador, 2),
        "motivo_encerramento": motivo_encerramento
    }

    salvar_resultado(resultado)

    return resultado
