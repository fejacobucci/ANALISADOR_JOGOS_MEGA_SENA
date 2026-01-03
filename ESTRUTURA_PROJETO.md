# Estrutura do Projeto Mega Sena

## Visão Geral

```
MEGA_SENA/
│
├── 📄 Projeto.md                    # Especificação do projeto
├── 📄 README.md                     # Documentação completa
├── 📄 QUICK_START.md               # Guia de início rápido
├── 📄 ESTRUTURA_PROJETO.md         # Este arquivo
│
├── 📊 resultados_MegaSena.xlsx     # Dados históricos (2.955 concursos)
│
├── 🗄️ database/
│   └── schema.sql                   # Schema do banco PostgreSQL
│
├── 🐍 backend/                      # API Python (FastAPI)
│   ├── .env                         # Configurações (criado)
│   ├── .env.example                 # Template de configurações
│   ├── requirements.txt             # Dependências Python
│   │
│   └── app/
│       ├── __init__.py
│       ├── main.py                  # Aplicação FastAPI principal
│       │
│       ├── api/
│       │   ├── __init__.py
│       │   └── routes.py            # Todas as rotas da API
│       │
│       ├── models/
│       │   ├── __init__.py
│       │   ├── database.py          # Configuração SQLAlchemy
│       │   └── models.py            # Modelos (Concurso, Dezena, Cidade)
│       │
│       └── services/
│           ├── __init__.py
│           ├── import_service.py    # Importação do Excel
│           ├── analytics_service.py # Análises estatísticas
│           └── generator_service.py # Geração de jogos
│
├── ⚛️ frontend/                     # Interface React + TypeScript
│   ├── .env                         # Configurações (criado)
│   ├── package.json                 # Dependências Node
│   ├── tsconfig.json                # Configuração TypeScript
│   ├── vite.config.ts               # Configuração Vite
│   ├── index.html                   # HTML principal
│   │
│   └── src/
│       ├── main.tsx                 # Entry point
│       ├── App.tsx                  # Componente principal
│       ├── index.css                # Estilos globais
│       │
│       ├── components/
│       │   ├── Layout.tsx           # Layout com sidebar
│       │   └── Layout.module.css
│       │
│       ├── pages/
│       │   ├── Dashboard.tsx        # Página inicial
│       │   ├── Dashboard.module.css
│       │   ├── Import.tsx           # Importação de dados
│       │   ├── Import.module.css
│       │   ├── GeradorJogos.tsx     # Gerador inteligente
│       │   ├── GeradorJogos.module.css
│       │   ├── FrequenciaGeral.tsx  # Análise de frequência
│       │   ├── FrequenciaPosicao.tsx
│       │   ├── NumerosQuentesFrios.tsx
│       │   ├── ParesImpares.tsx
│       │   ├── Quadrantes.tsx
│       │   ├── SomaDezenas.tsx
│       │   └── Analytics.module.css # Estilos compartilhados
│       │
│       └── services/
│           └── api.ts               # Cliente da API
│
└── 🔧 Scripts/
    ├── setup.sh                     # Setup inicial completo
    ├── start-backend.sh             # Inicia backend
    └── start-frontend.sh            # Inicia frontend
```

## Componentes Principais

### Backend (API)

#### 1. Modelos de Dados
- **Concurso**: Informações do concurso (data, premiação, etc.)
- **DezenaSorteada**: Números sorteados (normalizado)
- **CidadeGanhadora**: Cidades com ganhadores

#### 2. Serviços

**import_service.py** - Importação de Dados
- Lê arquivo Excel
- Processa 2.955 registros
- Barra de progresso via streaming
- Tratamento de erros

**analytics_service.py** - Análises Estatísticas
- `frequencia_geral()`: Frequência de todas as dezenas
- `frequencia_ultimos_anos()`: Frequência por período
- `frequencia_por_posicao()`: Por posição (1ª a 6ª)
- `numeros_quentes_frios()`: Tendências
- `numeros_atrasados()`: Números que não saem
- `analise_pares_impares()`: Distribuição par/ímpar
- `analise_quadrantes()`: 4 áreas do volante
- `analise_soma_dezenas()`: Intervalos de soma
- `combinacao_ja_sorteada()`: Verifica duplicidade
- `estatisticas_gerais()`: Dashboard

**generator_service.py** - Geração de Jogos
- `gerar_por_frequencia()`: Usa números quentes/frios
- `gerar_balanceado_par_impar()`: Balanceamento
- `gerar_por_quadrantes()`: Distribuição espacial
- `gerar_por_soma()`: Intervalo 150-220
- `gerar_trend()`: Tendências recentes
- `gerar_por_posicao()`: Por posição estatística
- `gerar_misto()`: Múltiplos critérios
- `desdobramento_garantido()`: Garantia matemática

#### 3. API Endpoints

**Analytics** (`/api/v1/analytics/`)
- GET `/estatisticas-gerais`
- GET `/frequencia-geral`
- GET `/frequencia-anos/{anos}`
- GET `/frequencia-posicao`
- GET `/numeros-quentes-frios`
- GET `/numeros-atrasados`
- GET `/pares-impares`
- GET `/quadrantes`
- GET `/soma-dezenas`
- POST `/verificar-combinacao`

**Generator** (`/api/v1/generator/`)
- POST `/gerar`
- POST `/desdobramento`

**Import** (`/api/v1/import/`)
- POST `/file-path`
- POST `/upload`

### Frontend (Interface)

#### 1. Páginas

- **Dashboard**: Visão geral e estatísticas
- **Importar**: Upload e importação com progresso
- **Frequência Geral**: Gráfico e tabela
- **Frequência por Posição**: Análise posicional
- **Quentes e Frios**: Números em tendência
- **Pares e Ímpares**: Distribuição
- **Quadrantes**: Análise espacial
- **Soma das Dezenas**: Intervalos
- **Gerador**: Interface de geração de jogos

#### 2. Componentes

- **Layout**: Sidebar com navegação
- **Cards**: Exibição de estatísticas
- **Gráficos**: Recharts (bar, pie)
- **Tabelas**: Listagem de dados
- **Formulários**: Configuração de geradores

#### 3. Serviços

- **api.ts**: Cliente HTTP (axios)
- **React Query**: Cache e estado
- **Router**: Navegação SPA

### Banco de Dados

#### Tabelas

**concursos**
- Concurso principal
- Premiações (sena, quina, quadra)
- Valores monetários
- Timestamps

**dezenas_sorteadas**
- Números sorteados
- Posição (1-6)
- Foreign key para concurso

**cidades_ganhadoras**
- Cidade e UF
- Foreign key para concurso

#### Views

- `vw_concursos_completos`: Concurso com todas as bolas
- `vw_frequencia_dezenas`: Frequência geral
- `vw_frequencia_por_posicao`: Por posição
- `vw_analise_pares_impares`: Distribuição
- `vw_soma_dezenas`: Soma total

#### Índices

- Otimização para consultas frequentes
- Performance em análises

## Fluxo de Dados

```
1. Importação:
   Excel → import_service → PostgreSQL

2. Análise:
   PostgreSQL → analytics_service → API → Frontend → Gráficos

3. Geração:
   Frontend → generator_service → Algoritmos → API → Frontend → Exibição
```

## Tecnologias Utilizadas

### Backend
- Python 3.11+
- FastAPI (web framework)
- SQLAlchemy (ORM)
- Pandas (processamento)
- psycopg2 (PostgreSQL)
- Pydantic (validação)

### Frontend
- React 18
- TypeScript
- Vite
- React Query
- React Router
- Recharts
- Axios
- CSS Modules

### Database
- PostgreSQL 14+

### DevOps
- Shell scripts
- Virtual environments
- Environment variables

## Métricas do Projeto

- **Linhas de Código**: ~5.000+
- **Arquivos**: 30+
- **Endpoints API**: 13
- **Páginas Frontend**: 9
- **Métodos de Geração**: 7
- **Análises Estatísticas**: 10+
- **Tabelas do Banco**: 3
- **Views do Banco**: 5

## Próximas Melhorias Sugeridas

1. **Autenticação**: Login de usuários
2. **Histórico**: Salvar jogos gerados
3. **Comparação**: Comparar jogos com sorteios
4. **Notificações**: Alertas de novos sorteios
5. **Mobile**: App mobile (React Native)
6. **Testes**: Unit tests e integration tests
7. **Docker**: Containerização
8. **CI/CD**: Deploy automatizado
9. **Cache**: Redis para consultas frequentes
10. **Machine Learning**: Previsões avançadas

## Licença

Uso pessoal e educacional
