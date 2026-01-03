# Mega Sena - Análises e Gerador de Jogos

Sistema completo para análise estatística dos resultados históricos da Mega Sena e geração inteligente de jogos baseada em múltiplos critérios.

## Funcionalidades

### Análises Estatísticas
- **Frequência Geral**: Dezenas mais e menos sorteadas ao longo do tempo
- **Frequência por Período**: Análise dos últimos 2 anos
- **Frequência por Posição**: Quais números aparecem mais em cada posição (1ª a 6ª)
- **Números Quentes e Frios**: Identificação de tendências recentes
- **Números Atrasados**: Dezenas que estão há mais tempo sem sair
- **Análise de Pares e Ímpares**: Distribuição estatística
- **Análise de Quadrantes**: Distribuição do volante em 4 áreas
- **Soma das Dezenas**: Intervalos mais comuns de soma total

### Geradores Inteligentes de Jogos
- **Por Frequência**: Baseado em números quentes ou frios
- **Balanceado**: Respeitando proporção de pares/ímpares
- **Por Quadrantes**: Distribuindo pelos 4 quadrantes do volante
- **Por Soma**: Respeitando intervalo de soma (150-220)
- **Trend**: Baseado em tendências recentes
- **Por Posição**: Usando números mais frequentes em cada posição
- **Misto**: Combina múltiplos critérios
- **Desdobramento**: Garantia matemática de premiação

### Recursos Técnicos
- Importação de dados do Excel com barra de progresso
- Verificação automática de combinações já sorteadas
- Interface responsiva e moderna
- Dashboard com estatísticas gerais
- API REST completa
- Banco de dados normalizado

## Stack Tecnológica

### Backend
- **Python 3.11+**
- **FastAPI**: Framework web moderno e rápido
- **SQLAlchemy**: ORM para PostgreSQL
- **Pandas**: Processamento de dados
- **Pydantic**: Validação de dados

### Frontend
- **React 18**: Biblioteca UI
- **TypeScript**: Tipagem estática
- **Vite**: Build tool moderna
- **React Query**: Gerenciamento de estado
- **Recharts**: Gráficos e visualizações
- **CSS Modules**: Estilização

### Banco de Dados
- **PostgreSQL**: Banco relacional

## Instalação

### Pré-requisitos
- Python 3.11 ou superior
- Node.js 18 ou superior
- PostgreSQL 14 ou superior

### 1. Configurar Banco de Dados

```bash
# Acesse o PostgreSQL
psql -U felipejacobucci

# Crie o banco de dados
CREATE DATABASE mega_sena_base;

# Execute o schema
\c mega_sena_base
\i database/schema.sql
```

### 2. Backend

```bash
# Entre no diretório backend
cd backend

# Crie um ambiente virtual
python3 -m venv venv

# Ative o ambiente virtual
source venv/bin/activate  # macOS/Linux
# ou
venv\Scripts\activate  # Windows

# Instale as dependências
pip install -r requirements.txt

# Configure as variáveis de ambiente
cp .env.example .env
# Edite o .env com suas credenciais

# Inicie o servidor
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

O backend estará disponível em: http://localhost:8000
Documentação da API: http://localhost:8000/docs

### 3. Frontend

```bash
# Entre no diretório frontend
cd frontend

# Instale as dependências
npm install

# Inicie o servidor de desenvolvimento
npm run dev
```

O frontend estará disponível em: http://localhost:3000

## Uso

### 1. Importar Dados

Acesse a página "Importar Dados" e clique em "Iniciar Importação". O sistema irá:
- Ler o arquivo `resultados_MegaSena.xlsx`
- Processar os dados
- Importar para o banco de dados
- Exibir barra de progresso

### 2. Visualizar Análises

Navegue pelas diferentes páginas de análise:
- Dashboard: Visão geral
- Frequência Geral: Números mais sorteados
- Frequência por Posição: Análise por posição
- Quentes e Frios: Tendências atuais
- Pares e Ímpares: Distribuição
- Quadrantes: Análise espacial
- Soma das Dezenas: Intervalos de soma

### 3. Gerar Jogos

Na página "Gerador de Jogos":
1. Escolha o método de geração
2. Configure os parâmetros
3. Defina a quantidade de jogos
4. Clique em "Gerar Jogos"

O sistema garante que nenhum jogo gerado já foi sorteado anteriormente.

## Estrutura do Projeto

```
MEGA_SENA/
├── backend/
│   ├── app/
│   │   ├── api/
│   │   │   └── routes.py          # Rotas da API
│   │   ├── models/
│   │   │   ├── database.py        # Configuração do banco
│   │   │   └── models.py          # Modelos SQLAlchemy
│   │   ├── services/
│   │   │   ├── import_service.py  # Importação de dados
│   │   │   ├── analytics_service.py # Análises
│   │   │   └── generator_service.py # Geração de jogos
│   │   └── main.py                # Aplicação FastAPI
│   ├── requirements.txt
│   └── .env.example
├── frontend/
│   ├── src/
│   │   ├── components/           # Componentes React
│   │   ├── pages/                # Páginas
│   │   ├── services/             # API clients
│   │   ├── App.tsx
│   │   └── main.tsx
│   ├── package.json
│   └── vite.config.ts
├── database/
│   └── schema.sql                # Schema do banco
├── resultados_MegaSena.xlsx      # Dados históricos
└── README.md
```

## API Endpoints

### Analytics
- `GET /api/v1/analytics/estatisticas-gerais` - Estatísticas gerais
- `GET /api/v1/analytics/frequencia-geral` - Frequência de todas as dezenas
- `GET /api/v1/analytics/frequencia-anos/{anos}` - Frequência por período
- `GET /api/v1/analytics/frequencia-posicao` - Frequência por posição
- `GET /api/v1/analytics/numeros-quentes-frios` - Números quentes e frios
- `GET /api/v1/analytics/numeros-atrasados` - Números atrasados
- `GET /api/v1/analytics/pares-impares` - Análise pares/ímpares
- `GET /api/v1/analytics/quadrantes` - Análise por quadrantes
- `GET /api/v1/analytics/soma-dezenas` - Análise de soma
- `POST /api/v1/analytics/verificar-combinacao` - Verifica se combinação já saiu

### Generator
- `POST /api/v1/generator/gerar` - Gera jogos
- `POST /api/v1/generator/desdobramento` - Gera desdobramento

### Import
- `POST /api/v1/import/file-path` - Importa arquivo por caminho
- `POST /api/v1/import/upload` - Upload e importação

## Modelos de Banco de Dados

### Concursos
- Dados principais do concurso
- Premiações
- Arrecadação

### Dezenas Sorteadas
- Números sorteados
- Posição de cada número
- Relacionamento com concurso

### Cidades Ganhadoras
- Cidades com ganhadores
- UF

## Métricas e Algoritmos

### Frequência
Calcula quantas vezes cada dezena foi sorteada no período analisado.

### Números Quentes/Frios
- **Quentes**: Dezenas com maior frequência nos últimos N concursos
- **Frios**: Dezenas com menor frequência nos últimos N concursos

### Análise de Pares/Ímpares
Identifica as combinações mais comuns de números pares e ímpares.

### Quadrantes
Divide o volante em 4 áreas:
- Q1: 1-15
- Q2: 16-30
- Q3: 31-45
- Q4: 46-60

### Soma das Dezenas
A maioria dos sorteios tem soma entre 150 e 220. O gerador pode usar este critério.

## Desenvolvimento

### Adicionar Nova Análise

1. Crie método em `analytics_service.py`
2. Adicione rota em `routes.py`
3. Crie componente em `frontend/src/pages/`
4. Adicione rota em `App.tsx`
5. Adicione item no menu do `Layout.tsx`

### Adicionar Novo Método de Geração

1. Implemente em `generator_service.py`
2. Adicione opção no endpoint de geração
3. Atualize frontend em `GeradorJogos.tsx`

## Licença

Este projeto é de uso pessoal e educacional.

## Autor

Felipe Jacobucci

## Observações

- Todos os jogos gerados são verificados contra o histórico
- Nenhum jogo já sorteado será sugerido
- Os algoritmos são baseados em análise estatística
- Não há garantia de vitória (é uma loteria!)
