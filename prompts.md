# Registro de Prompts — Código Milionário

Este documento reúne e organiza os principais prompts e direcionamentos técnicos utilizados durante o planejamento, desenvolvimento, integração, teste e finalização do projeto **Código Milionário**.

O conteúdo a seguir representa uma organização estruturada e resumida das solicitações formuladas ao longo de cada etapa do ciclo de vida do projeto.

---

## 1. Planejamento e Arquitetura do Projeto

**Objetivo:** Definir os requisitos funcionais e não-funcionais, estrutura de arquivos, regras de negócio e tecnologias empregadas.

**Solicitações e Prompts Utilizados:**
- "Como estruturar um jogo de perguntas e respostas em Python inspirado no Show do Milhão, dividindo em camadas de banco de dados, lógica da partida, interface de terminal e página web?"
- "Qual a melhor organização de pastas para separar o código Python (`jogo/`), os scripts SQL de banco de dados (`database/`) e o site de ranking (`site/`)?"
- "Como definir uma tabela de premiações progressivas de 0 a 9 acertos que garanta ao jogador o prêmio dos acertos anteriores caso ele erre ou decida parar?"

---

## 2. Desenvolvimento da Lógica em Python

**Objetivo:** Implementar o fluxo da partida, sorteio de perguntas, controle de tempo e interface de terminal.

**Solicitações e Prompts Utilizados:**
- "Como implementar uma função em Python para sortear 9 perguntas no formato: 3 fáceis, 3 médias e 3 difíceis, garantindo ausência de repetição durante a partida?"
- "Como medir com precisão (`time.perf_counter`) o tempo ativo de resposta do jogador, desconsiderando o tempo de conexão com o banco de dados, navegação em menus e salvamento do resultado?"
- "Como encerrar a partida imediatamente quando o usuário digita uma entrada inválida (fora de A, B, C, D ou S) e garantir que ele leve o prêmio acumulado?"
- "Como criar um menu principal limpo e funcional com opções para iniciar partida, consultar ranking oficial e sair?"

---

## 3. Banco de Dados, Supabase e Segurança

**Objetivo:** Desenvolver o script SQL completo no PostgreSQL/Supabase, implementar funções RPC seguras e configurar políticas de Row Level Security (RLS).

**Solicitações e Prompts Utilizados:**
- "Como escrever o script SQL completo (`database/estrutura.sql`) para criar as tabelas `jogos`, `perguntas` e `partidas`, incluindo índices de performance e restrições de integridade?"
- "Como criar a função RPC `buscar_perguntas(p_dificuldade)` com `SECURITY DEFINER` para retornar as perguntas de determinada dificuldade sem expor a coluna `correta` ao cliente?"
- "Como criar a função RPC `validar_resposta(p_pergunta_id, p_resposta)` para que o gabarito seja conferido diretamente no servidor de banco de dados?"
- "Como implementar a função RPC `salvar_partida(...)` utilizando identificador UUID gerado na partida para evitar duplicidade de registros (idempotência com `ON CONFLICT (id) DO NOTHING`)?"
- "Como criar a função RPC `buscar_ranking()` que retorne o Top 10 considerando apenas a melhor partida de cada jogador, ordenando por maior prêmio, menor tempo de resposta e data mais antiga?"
- "Como ativar Row Level Security (RLS) nas tabelas e conceder permissões adequadas às roles `anon` e `authenticated` para uso com chave pública?"

---

## 4. Desenvolvimento da Interface Web do Ranking

**Objetivo:** Construir uma página web moderna, elegante e responsiva utilizando HTML5, CSS3 e JavaScript integrado ao Supabase via CDN.

**Solicitações e Prompts Utilizados:**
- "Como estruturar uma página HTML semântica com visual escuro (dark theme) e detalhes dourados discretos para exibir o ranking do Código Milionário?"
- "Como estilizar a tabela de classificação em CSS Grid com destaques em medalhas (ouro, prata e bronze) para os três primeiros colocados?"
- "Como conectar a biblioteca oficial `@supabase/supabase-js` no navegador usando a chave pública (publishable/anon key) e chamar a RPC `buscar_ranking()`?"
- "Como formatar valores monetários em Real (BRL), tempos em minutos e segundos (`Xmin YYs`) e datas no padrão brasileiro (`DD/MM/AAAA`) no JavaScript?"
- "Como implementar sanitização contra ataques XSS ao exibir os apelidos dos jogadores e criar mensagens amigáveis de carregamento (spinner), erro e lista vazia?"

---

## 5. Testes, Tratamento de Falhas e Robustez

**Objetivo:** Validar todas as regras de negócio, assegurar a tolerância a falhas de rede e garantir a integridade dos dados.

**Solicitações e Prompts Utilizados:**
- "Como criar uma suíte automatizada de testes unitários para validar a tabela de prêmios, a distribuição de perguntas e a formatação de dinheiro?"
- "Como tratar erros de conexão de forma que, se o envio ao Supabase falhar após a partida, o resultado seja salvo localmente em `partidas_pendentes.json` e reenviado assim que a conexão retornar?"
- "Como testar a proteção contra duplicidade reenviando uma mesma partida com o mesmo UUID duas vezes consecutivas?"
- "Como criar um script único (`executar_testes.py`) que execute todos os testes de perguntas, partidas, banco e ranking, gerando um relatório consolidado?"

---

## 6. Documentação, Segurança e Preparação para o GitHub

**Objetivo:** Elaborar a documentação completa do projeto, proteger credenciais sensíveis e preparar o repositório para entrega e publicação.

**Solicitações e Prompts Utilizados:**
- "Como estruturar o `README.md` detalhando o funcionamento do jogo, requisitos, instalação, configuração do Supabase, execução e publicação?"
- "Como configurar o `.gitignore` para impedir que `.env`, `__pycache__`, arquivos `.pyc`, logs e arquivos temporários sejam enviados ao repositório?"
- "Como estruturar o `.env.example` utilizando somente valores de exemplo e placeholders, garantindo que credenciais reais nunca sejam commitadas?"
- "Quais são as instruções passo a passo para criar o repositório no GitHub e publicar o site via GitHub Pages?"

---

## Observação Metodológica

A inteligência artificial foi empregada como ferramenta de assistência no planejamento arquitetural, implementação de boas práticas de programação, reforço de segurança contra injeção e XSS, e elaboração de testes automatizados completos. Todas as soluções foram verificadas e executadas no ambiente do projeto.