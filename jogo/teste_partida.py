import os
import sys
import unittest

# Garante que as importações funcionem a partir de qualquer diretório
_pasta_atual = os.path.dirname(os.path.abspath(__file__))
if _pasta_atual not in sys.path:
    sys.path.insert(0, _pasta_atual)

from partida import (
    PREMIOS,
    DIFICULDADES,
    calcular_premio,
    formatar_dinheiro,
    sortear_perguntas,
    iniciar_partida
)


class TesteLogicaPartida(unittest.TestCase):
    """Bateria de testes automatizados da lógica de negócio da partida."""

    def test_tabela_premios(self):
        """Valida se a tabela de premiação possui exatamente 9 valores e confere cada nível."""
        self.assertEqual(len(PREMIOS), 9)
        self.assertEqual(calcular_premio(0), 0)
        self.assertEqual(calcular_premio(1), 1000)
        self.assertEqual(calcular_premio(2), 5000)
        self.assertEqual(calcular_premio(3), 10000)
        self.assertEqual(calcular_premio(4), 25000)
        self.assertEqual(calcular_premio(5), 50000)
        self.assertEqual(calcular_premio(6), 100000)
        self.assertEqual(calcular_premio(7), 200000)
        self.assertEqual(calcular_premio(8), 500000)
        self.assertEqual(calcular_premio(9), 1000000)

    def test_formatacao_dinheiro(self):
        """Testa a formatação em Real brasileiro."""
        self.assertEqual(formatar_dinheiro(0), "R$ 0,00")
        self.assertEqual(formatar_dinheiro(1000), "R$ 1.000,00")
        self.assertEqual(formatar_dinheiro(50000), "R$ 50.000,00")
        self.assertEqual(formatar_dinheiro(1000000), "R$ 1.000.000,00")

    def test_sorteio_perguntas(self):
        """Testa o sorteio de perguntas:

        - Exatamente 9 perguntas no total
        - 3 fáceis, 3 médias e 3 difíceis (nessa ordem)
        - Sem perguntas repetidas na partida
        """
        perguntas = sortear_perguntas()
        self.assertEqual(len(perguntas), 9, "A partida deve conter exatamente 9 perguntas.")

        # Verifica ordem e quantidade por dificuldade
        dificuldades_sorteadas = [p.get("dificuldade") for p in perguntas]
        self.assertEqual(dificuldades_sorteadas[0:3], ["facil", "facil", "facil"])
        self.assertEqual(dificuldades_sorteadas[3:6], ["media", "media", "media"])
        self.assertEqual(dificuldades_sorteadas[6:9], ["dificil", "dificil", "dificil"])

        # Verifica ausência de repetição
        ids = [p["id"] for p in perguntas]
        self.assertEqual(len(ids), len(set(ids)), "Não pode haver repetição de perguntas na partida.")

    def test_regras_encerramento_simuladas(self):
        """Testa as regras de negócio para os 4 motivos de encerramento:

        1. 'erro' -> jogador recebe o prêmio correspondente aos acertos anteriores
        2. 'entrada_invalida' -> jogador encerra a partida imediatamente
        3. 'desistencia' -> jogador para voluntariamente e leva o prêmio atual
        4. 'concluida' -> jogador responde as 9 e leva R$ 1.000.000,00
        """
        # Caso 1: Erro na 4ª pergunta (3 acertos anteriores)
        acertos_erro = 3
        premio_erro = calcular_premio(acertos_erro)
        self.assertEqual(premio_erro, 10000, "Ao errar a 4ª pergunta, deve manter R$ 10.000,00 dos 3 acertos.")

        # Caso 2: Entrada inválida na 1ª pergunta (0 acertos)
        acertos_invalido = 0
        premio_invalido = calcular_premio(acertos_invalido)
        self.assertEqual(premio_invalido, 0)

        # Caso 3: Desistência voluntária após a 5ª pergunta (5 acertos)
        acertos_parar = 5
        premio_parar = calcular_premio(acertos_parar)
        self.assertEqual(premio_parar, 50000)

        # Caso 4: Conclusão das 9 perguntas
        acertos_vitoria = 9
        premio_vitoria = calcular_premio(acertos_vitoria)
        self.assertEqual(premio_vitoria, 1000000)


def executar_testes_partida():
    print("==================================================")
    print("TESTE: LÓGICA E REGRAS DA PARTIDA (teste_partida.py)")
    print("==================================================")
    suite = unittest.TestLoader().loadTestsFromTestCase(TesteLogicaPartida)
    runner = unittest.TextTestRunner(verbosity=2)
    resultado = runner.run(suite)
    return resultado.wasSuccessful()


if __name__ == "__main__":
    if "--interativo" in sys.argv:
        print("\nModo interativo de partida:")
        res = iniciar_partida()
        print("\nResultado recebido:")
        print(res)
    else:
        sucesso = executar_testes_partida()
        sys.exit(0 if sucesso else 1)
