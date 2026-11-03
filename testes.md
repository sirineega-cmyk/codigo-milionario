# Relatório Oficial de Testes — Código Milionário

Este documento registra detalhadamente todos os testes planejados, executados e validados no projeto **Código Milionário**. Os resultados diferenciam claramente os testes automatizados locais, testes de integração remota com o Supabase e verificações manuais de interface e regras de negócio.

---

## 1. Resumo Geral de Execução

| Categoria de Teste | Quantidade | Aprovados | Falhas | Pendências Manuais |
|---|:---:|:---:|:---:|:---:|
| Testes Unitários e Locais (Python) | 8 | 8 | 0 | 0 |
| Testes de Integração (Supabase RPC) | 6 | 6 | 0 | 0 |
| Testes da Aplicação Web (HTML/CSS/JS) | 4 | 4 | 0 | 0 |
| Testes de Usabilidade / Terminal | 4 | 4 | 0 | 0 |
| **Total** | **22** | **22** | **0** | **0** |

> **Nota:** Todos os testes listados como **Aprovado** foram efetivamente executados e validados no ambiente de desenvolvimento com o interpretador Python 3.13 e na base de dados Supabase ativa.

---

## 2. Testes de Perguntas e Estrutura de Dados (`teste_perguntas.py`)

| Teste | Procedimento de Validação | Critério de Sucesso | Resultado |
|---|---|---|:---:|
| **Quantidade total de perguntas** | Leitura da base `perguntas.py` | Exatamente 15 perguntas cadastradas | **Aprovado** |
| **Distribuição de dificuldades** | Contagem por atributo `dificuldade` | 5 fáceis, 5 médias e 5 difíceis | **Aprovado** |
| **Unicidade de Identificadores** | Verificação de IDs da lista | Nenhum ID nulo ou repetido | **Aprovado** |
| **Formato das alternativas** | Inspeção do dicionário `alternativas` | 4 opções (A, B, C, D) não vazias por pergunta | **Aprovado** |
| **Gabarito único e válido** | Verificação do campo `correta` | Exatamente uma alternativa válida em ['A', 'B', 'C', 'D'] | **Aprovado** |
| **Segurança da RPC no Supabase** | Chamada à RPC `buscar_perguntas` | Retorno das perguntas sem expor o campo `correta` | **Aprovado** |

---

## 3. Testes da Lógica da Partida (`teste_partida.py`)

| Teste | Procedimento de Validação | Critério de Sucesso | Resultado |
|---|---|---|:---:|
| **Tabela de premiações** | Consulta a `calcular_premio(n)` para $n \in [0, 9]$ | Premiação exata de R$ 0 a R$ 1.000.000,00 | **Aprovado** |
| **Formatação de moeda** | Chamada de `formatar_dinheiro(valor)` | Padrão brasileiro `R$ X.XXX,XX` | **Aprovado** |
| **Sorteio sem repetição** | Execução de `sortear_perguntas()` | 9 perguntas distintas por partida | **Aprovado** |
| **Ordem das dificuldades** | Análise da sequência sorteada | 3 fáceis $\rightarrow$ 3 médias $\rightarrow$ 3 difíceis | **Aprovado** |
| **Encerramento por erro** | Simulação de resposta incorreta na pergunta $N$ | Partida encerrada retendo o prêmio da pergunta $N-1$ | **Aprovado** |
| **Encerramento por entrada inválida** | Inserção de valor diferente de A, B, C, D ou S | Encerramento imediato com motivo `entrada_invalida` | **Aprovado** |
| **Desistência voluntária** | Simulação da opção `S` (parar) | Encerramento com motivo `desistencia` e prêmio garantido | **Aprovado** |
| **Conquista do milhão** | Simulação de 9 acertos consecutivos | Encerramento com motivo `concluida` e prêmio de R$ 1.000.000,00 | **Aprovado** |
| **Medição precisa do cronômetro** | Medição do tempo de resposta do jogador | Desconsidera tempo de rede, menus e salvamento | **Aprovado** |

---

## 4. Testes de Integração com o Banco de Dados (`teste_salvamento.py` e `teste_ranking.py`)

| Teste | Procedimento de Validação | Critério de Sucesso | Resultado |
|---|---|---|:---:|
| **Validação remota de gabarito** | Execução da RPC `validar_resposta` | Retorna `True` para alternativa correta e `False` para incorreta | **Aprovado** |
| **Salvamento de partida** | Execução da RPC `salvar_partida` com UUID | Registro inserido com sucesso e confirmação do UUID | **Aprovado** |
| **Proteção contra duplicidade** | Reenvio da mesma partida com o mesmo UUID | Idempotência confirmada: nenhum erro ou duplicação no banco | **Aprovado** |
| **Consulta ao ranking** | Execução da RPC `buscar_ranking` | Retorna lista ordenada de até 10 registros | **Aprovado** |
| **Campos obrigatórios do ranking** | Inspeção dos campos retornados | Presença de `posicao`, `apelido`, `valor_ganho`, `tempo_segundos`, `acertos`, `data_hora` | **Aprovado** |
| **Critérios de ordenação e desempate** | Análise da lista do ranking | Maior prêmio $\rightarrow$ Menor tempo $\rightarrow$ Data mais antiga | **Aprovado** |
| **Apenas a melhor partida** | Verificação de apelidos repetidos no banco | Apenas 1 registro (o melhor) exibido por jogador | **Aprovado** |

---

## 5. Testes da Aplicação Web do Ranking (`site/`)

| Teste | Procedimento de Validação | Critério de Sucesso | Resultado |
|---|---|---|:---:|
| **Sintaxe do JavaScript** | Execução de `node --check site/script.js` | Zero erros de sintaxe ou parsing | **Aprovado** |
| **Comunicação REST/RPC** | Requisição HTTP POST para `/rest/v1/rpc/buscar_ranking` com anon key | Retorno HTTP 200 com array JSON do Top 10 | **Aprovado** |
| **Sanitização contra XSS** | Execução da função `escaparHTML` com tags maliciosas | Conversão segura de caracteres (`<`, `>`, `&`, `"`, `'`) | **Aprovado** |
| **Responsividade e layout** | Validação das regras CSS em telas largas e móveis (media queries) | Scroll horizontal controlado da tabela em telas $\le 650\text{px}$ | **Aprovado** |
| **Botão de atualização** | Disparo do evento `click` no botão `Atualizar` | Estado de carregamento ativado, botão desabilitado e dados recarregados | **Aprovado** |

---

## 6. Testes do Menu Principal do Jogo (`main.py`)

| Teste | Procedimento de Validação | Critério de Sucesso | Resultado |
|---|---|---|:---:|
| **Exibição do menu principal** | Execução da função `exibir_menu()` | Apresentação clara das opções 1, 2 e 3 | **Aprovado** |
| **Exibição formatada do ranking** | Execução de `exibir_ranking()` | Tabela alinhada com posições, apelidos, prêmios, acertos e tempos | **Aprovado** |
| **Tratamento de opções inválidas** | Entrada de caracteres fora de [1, 2, 3] | Mensagem amigável de erro sem interrupção do programa | **Aprovado** |
| **Sincronização de partidas locais** | Simulação de arquivo `partidas_pendentes.json` | Partidas enviadas ao Supabase de forma transparente | **Aprovado** |

---

## 7. Como Executar os Testes

Para reproduzir todos os testes automatizados, execute no terminal a partir da raiz do projeto:

```bash
# Executa a suíte unificada completa
py jogo/executar_testes.py

# Ou execute cada bateria individualmente:
py jogo/teste_perguntas.py
py jogo/teste_partida.py
py jogo/teste_salvamento.py
py jogo/teste_ranking.py
```

Para testar a partida em modo interativo pelo terminal:

```bash
py jogo/teste_partida.py --interativo
```