# 🏆 Código Milionário

> Um jogo de perguntas e respostas desenvolvido em Python, com persistência e validação no Supabase (PostgreSQL) e uma página web elegante para consulta do ranking oficial em tempo real.

Inspirado em programas televisivos clássicos de premiação, o **Código Milionário** desafia os participantes a responderem corretamente a **9 perguntas** de programação e tecnologia (3 fáceis, 3 médias e 3 difíceis) para conquistar o prêmio máximo de **R$ 1.000.000,00**.

---

## 📋 Sumário

- [Visão Geral e Regras do Jogo](#-visão-geral-e-regras-do-jogo)
- [Tabela de Premiações](#-tabela-de-premiações)
- [Tecnologias Utilizadas](#-tecnologias-utilizadas)
- [Estrutura do Repositório](#-estrutura-do-repositório)
- [Instalação e Configuração](#-instalação-e-configuração)
  - [1. Pré-requisitos](#1-pré-requisitos)
  - [2. Clonagem e Instalação de Dependências](#2-clonagem-e-instalação-de-dependências)
  - [3. Configuração do Banco de Dados no Supabase](#3-configuração-do-banco-de-dados-no-supabase)
  - [4. Configuração das Variáveis de Ambiente (.env)](#4-configuração-das-variáveis-de-ambiente-env)
- [Como Executar o Jogo (Terminal)](#-como-executar-o-jogo-terminal)
- [Como Abrir e Publicar o Site de Ranking](#-como-abrir-e-publicar-o-site-de-ranking)
- [Suíte de Testes](#-suíte-de-testes)
- [Segurança e Boas Práticas](#-segurança-e-boas-práticas)
- [Passo a Passo para Publicação no GitHub](#-passo-a-passo-para-publicação-no-github)

---

## 🎯 Visão Geral e Regras do Jogo

- **Identificação do Jogador:** O participante informa um apelido não vazio no início. Nenhum dado pessoal desnecessário é coletado.
- **Banco de Perguntas:** Possui 15 perguntas oficiais cadastradas e balanceadas: 5 fáceis, 5 médias e 5 difíceis sobre Python, SQL, lógica e Inteligência Artificial.
- **Estrutura da Partida:** Cada partida apresenta exatamente **9 perguntas**, ordenadas obrigatoriamente por nível de dificuldade:
  - 3 perguntas **fáceis**
  - 3 perguntas **médias**
  - 3 perguntas **difíceis**
- **Sorteio sem Repetição:** As perguntas são sorteadas aleatoriamente a cada partida, sem repetição.
- **Alternativas:** Cada pergunta possui 4 alternativas (A, B, C, D) e somente uma resposta correta.
- **Cronômetro Preciso:** O cronômetro inicia na 1ª pergunta e contabiliza apenas o tempo ativo de resposta do jogador, desconsiderando a navegação em menus, latência de rede e etapas de salvamento.
- **Encerramento da Partida:** A partida termina sob quatro circunstâncias:
  1. *Erro na resposta:* O jogador encerra a partida e **mantém o prêmio acumulado nos acertos anteriores**.
  2. *Entrada inválida:* Digitar qualquer caractere fora de A, B, C, D ou S encerra imediatamente a partida, conforme a regra do projeto.
  3. *Desistência voluntária:* O jogador digita `S` a qualquer momento para parar e garantir o prêmio conquistado até então.
  4. *Conclusão:* Ao acertar as 9 perguntas, o jogador é consagrado como o novo Código Milionário e recebe R$ 1.000.000,00.
- **Salvamento Único e Idempotente:** O resultado é associado a um identificador único (UUID), garantindo que quedas de conexão ou novas tentativas não gerem partidas duplicadas.

---

## 💰 Tabela de Premiações

| Acertos | Prêmio Conquistado |
|:---:|---:|
| 0 | R$ 0,00 |
| 1 | R$ 1.000,00 |
| 2 | R$ 5.000,00 |
| 3 | R$ 10.000,00 |
| 4 | R$ 25.000,00 |
| 5 | R$ 50.000,00 |
| 6 | R$ 100.000,00 |
| 7 | R$ 200.000,00 |
| 8 | R$ 500.000,00 |
| **9** | **R$ 1.000.000,00** |

---

## 🛠️ Tecnologias Utilizadas

- **Linguagem Principal:** Python 3.10+ (compatível com Python 3.13)
- **Banco de Dados Relacional:** PostgreSQL hospedado no [Supabase](https://supabase.com)
- **Recursos de Banco:** Funções RPC (`SECURITY DEFINER`), Índices B-Tree, Restrições `CHECK`, Chaves Estrangeiras e Row Level Security (RLS)
- **Frontend do Ranking:** HTML5 semântico, CSS3 moderno (layout responsivo com CSS Grid, tema dark & gold) e JavaScript vanilla
- **Bibliotecas Python:** `supabase`, `python-dotenv`, `truststore`

---

## 📁 Estrutura do Repositório

```text
codigo-milionario/
├── .env.example              # Modelo seguro para variáveis de ambiente (sem credenciais)
├── .gitignore                # Regras de exclusão (.env, caches, logs, temporários)
├── database/
│   └── estrutura.sql         # Script SQL completo de criação, carga, RPCs e RLS
├── jogo/
│   ├── banco.py              # Camada de comunicação RPC e fallback de conexão
│   ├── main.py               # Menu principal em terminal e exibição do ranking
│   ├── partida.py            # Regras da partida, cronômetro e fluxo do jogo
│   ├── perguntas.py          # As 15 perguntas oficiais estruturadas
│   ├── executar_testes.py    # Executor unificado da suíte completa de testes
│   ├── teste_partida.py      # Testes da lógica de partida, premiação e regras
│   ├── teste_perguntas.py    # Testes de integridade das perguntas e segurança da RPC
│   ├── teste_ranking.py      # Testes da estrutura e ordenação do ranking
│   └── teste_salvamento.py   # Testes de persistência e idempotência contra duplicidade
├── prompts.md                # Registro estruturado de prompts de desenvolvimento
├── README.md                 # Documentação oficial do projeto
├── requirements.txt          # Dependências do ecossistema Python
├── site/
│   ├── index.html            # Interface web semântica e acessível
│   ├── script.js             # Integração web via Supabase JS com proteção XSS
│   └── style.css             # Folha de estilos responsiva com tema dark & gold
└── testes.md                 # Relatório detalhado dos testes executados
```

---

## ⚙️ Instalação e Configuração

### 1. Pré-requisitos

- **Python 3.10 ou superior** instalado ([python.org](https://www.python.org/downloads/)).
- Git instalado (para versionamento e publicação).
- Conta gratuita no [Supabase](https://supabase.com).

### 2. Clonagem e Instalação de Dependências

Abra o terminal na pasta do projeto e instale as dependências:

```bash
py -m pip install -r requirements.txt
```

*(No Linux ou macOS, utilize `python3 -m pip install -r requirements.txt`)*

### 3. Configuração do Banco de Dados no Supabase

1. Acesse o painel do seu projeto no [Supabase Dashboard](https://supabase.com/dashboard).
2. No menu lateral esquerdo, clique em **SQL Editor**.
3. Abra o arquivo `database/estrutura.sql` deste projeto, copie todo o seu conteúdo e cole no editor do Supabase.
4. Clique no botão **Run** para executar o script.
5. O script realizará automaticamente:
   - A criação das tabelas `jogos`, `perguntas` e `partidas`.
   - A criação de índices para otimização de consultas e ordenação do ranking.
   - O cadastro do jogo `"Código Milionário"` e das 15 perguntas oficiais.
   - A criação das 4 funções RPC seguras:
     - `buscar_perguntas(p_dificuldade)`
     - `validar_resposta(p_pergunta_id, p_resposta)`
     - `salvar_partida(p_id, p_apelido, p_valor_ganho, p_tempo_segundos, p_acertos, p_motivo_encerramento)`
     - `buscar_ranking()`
   - A ativação do Row Level Security (RLS) e a concessão das permissões de execução para as roles públicas (`anon` e `authenticated`).

### 4. Configuração das Variáveis de Ambiente (.env)

1. Crie uma cópia do arquivo `.env.example` com o nome `.env`:
   ```bash
   cp .env.example .env
   ```
2. Abra o arquivo `.env` e preencha com as credenciais do seu projeto Supabase (disponíveis em *Project Settings* > *API*):
   ```env
   SUPABASE_URL=https://seu-projeto.supabase.co
   SUPABASE_KEY=sua_chave_publica_anon_ou_publishable
   ```
> **Atenção:** Nunca compartilhe nem adicione o arquivo `.env` ao controle de versão Git. O arquivo já está listado no `.gitignore`.

---

## 🎮 Como Executar o Jogo (Terminal)

Na pasta raiz do projeto, execute:

```bash
py jogo/main.py
```

O menu interativo apresentará as seguintes opções:

```text
===================================
         CÓDIGO MILIONÁRIO
===================================
1 - Iniciar partida
2 - Consultar ranking
3 - Sair
===================================
```

- **Opção 1:** Digite seu apelido e responda às 9 perguntas informando a letra da alternativa desejada (`A`, `B`, `C` ou `D`) ou `S` para parar e garantir a premiação acumulada.
- **Opção 2:** Consulta instantaneamente a classificação Top 10 atualizada do Supabase.
- **Opção 3:** Encerra o jogo com uma mensagem amigável.

---

## 🌐 Como Abrir e Publicar o Site de Ranking

### Execução Local

1. Para testar o site localmente, basta abrir o arquivo `site/index.html` em qualquer navegador moderno (Google Chrome, Firefox, Edge, Safari).
2. Se preferir rodar através de um servidor HTTP local:
   ```bash
   py -m http.server 8080 --directory site
   ```
   Em seguida, acesse no navegador: `http://localhost:8080`.

### Publicação no GitHub Pages

1. No seu repositório no GitHub, acesse a aba **Settings** > **Pages**.
2. Na seção **Build and deployment**:
   - Em **Source**, selecione `Deploy from a branch`.
   - Em **Branch**, selecione `main` e a pasta `/site` (ou crie um branch com os arquivos da pasta `site/` na raiz).
3. Salve as alterações. Em poucos instantes o site estará online publicamente!

---

## 🧪 Suíte de Testes

O projeto conta com testes automatizados e independentes. Para rodar a suíte completa com um único comando:

```bash
py jogo/executar_testes.py
```

Você também pode executar os módulos individualmente:

```bash
py jogo/teste_perguntas.py    # Valida estrutura das perguntas e ocultação da resposta na RPC
py jogo/teste_partida.py      # Valida tabela de prêmios, sorteio 3/3/3 e regras de término
py jogo/teste_salvamento.py   # Valida persistência de partidas e proteção contra duplicatas
py jogo/teste_ranking.py      # Valida integridade dos dados e ordenação do Top 10
```

Para maiores detalhes e histórico dos testes realizados, consulte o arquivo [testes.md](testes.md).

---

## 🔒 Segurança e Boas Práticas

1. **Credenciais Protegidas:** As credenciais privadas residem exclusivamente no `.env`. O arquivo `.env.example` contém apenas marcadores explicativos.
2. **Gabarito Seguro:** A tabela `perguntas` possui RLS ativado e a coluna `correta` jamais é exposta ao frontend ou terminal. A conferência é efetuada no próprio servidor do banco através da função `validar_resposta`.
3. **Idempotência no Salvamento:** Toda partida gera um UUID próprio na primeira tentativa. O envio utiliza cláusula `ON CONFLICT (id) DO NOTHING`, impedindo duplicações mesmo diante de instabilidades de rede e retentativas.
4. **Tolerância a Falhas de Conexão:** Caso o jogador esteja temporariamente offline ao término da partida, o jogo armazena os dados em `partidas_pendentes.json` e realiza a sincronização automática assim que a conectividade for restabelecida.
5. **Proteção contra XSS no Site:** Todo apelido e texto de usuário é rigorosamente sanitizado via `escaparHTML` antes de ser inserido no DOM.

---

## 🚀 Passo a Passo para Publicação no GitHub

Para publicar o projeto no seu perfil do GitHub com total segurança:

```bash
# 1. Inicialize o repositório Git (caso ainda não tenha sido iniciado)
git init

# 2. Verifique se o .env está devidamente ignorado
git status

# 3. Adicione os arquivos ao controle de versão
git add .

# 4. Crie o commit com as alterações finalizadas
git commit -m "feat: finalizacao completa do projeto Codigo Milionario"

# 5. Conecte o repositório local ao seu repositório remoto no GitHub
# (Substitua SEU_USUARIO e SEU_REPOSITORIO pelos seus dados reais)
git remote add origin https://github.com/SEU_USUARIO/codigo-milionario.git

# 6. Envie os arquivos para a branch principal
git branch -M main
git push -u origin main
```