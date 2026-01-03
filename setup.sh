#!/bin/bash

echo "========================================="
echo "   Mega Sena - Setup Inicial"
echo "========================================="
echo ""

# Cores para output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Função para verificar se comando existe
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Verifica Python
echo -e "${YELLOW}Verificando Python...${NC}"
if command_exists python3; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ Python encontrado: $PYTHON_VERSION${NC}"
else
    echo -e "${RED}✗ Python 3 não encontrado. Por favor, instale Python 3.11+${NC}"
    exit 1
fi

# Verifica Node.js
echo -e "${YELLOW}Verificando Node.js...${NC}"
if command_exists node; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Node.js encontrado: $NODE_VERSION${NC}"
else
    echo -e "${RED}✗ Node.js não encontrado. Por favor, instale Node.js 18+${NC}"
    exit 1
fi

# Verifica PostgreSQL
echo -e "${YELLOW}Verificando PostgreSQL...${NC}"
if command_exists psql; then
    PSQL_VERSION=$(psql --version)
    echo -e "${GREEN}✓ PostgreSQL encontrado: $PSQL_VERSION${NC}"
else
    echo -e "${RED}✗ PostgreSQL não encontrado. Por favor, instale PostgreSQL 14+${NC}"
    exit 1
fi

echo ""
echo "========================================="
echo "   Configurando Backend"
echo "========================================="
echo ""

cd backend

# Cria ambiente virtual
echo -e "${YELLOW}Criando ambiente virtual...${NC}"
python3 -m venv venv
echo -e "${GREEN}✓ Ambiente virtual criado${NC}"

# Ativa ambiente virtual
echo -e "${YELLOW}Ativando ambiente virtual...${NC}"
source venv/bin/activate
echo -e "${GREEN}✓ Ambiente virtual ativado${NC}"

# Instala dependências
echo -e "${YELLOW}Instalando dependências do Python...${NC}"
pip install --upgrade pip
pip install -r requirements.txt
echo -e "${GREEN}✓ Dependências instaladas${NC}"

# Cria arquivo .env
if [ ! -f .env ]; then
    echo -e "${YELLOW}Criando arquivo .env...${NC}"
    cp .env.example .env
    echo -e "${GREEN}✓ Arquivo .env criado${NC}"
    echo -e "${YELLOW}⚠ Por favor, edite o arquivo backend/.env com suas credenciais${NC}"
else
    echo -e "${GREEN}✓ Arquivo .env já existe${NC}"
fi

cd ..

echo ""
echo "========================================="
echo "   Configurando Frontend"
echo "========================================="
echo ""

cd frontend

# Instala dependências do Node
echo -e "${YELLOW}Instalando dependências do Node.js...${NC}"
npm install
echo -e "${GREEN}✓ Dependências instaladas${NC}"

cd ..

echo ""
echo "========================================="
echo "   Configurando Banco de Dados"
echo "========================================="
echo ""

echo -e "${YELLOW}Para configurar o banco de dados, execute:${NC}"
echo ""
echo "psql -U felipejacobucci -c 'CREATE DATABASE mega_sena_base;'"
echo "psql -U felipejacobucci -d mega_sena_base -f database/schema.sql"
echo ""

echo "========================================="
echo "   Setup Completo!"
echo "========================================="
echo ""
echo -e "${GREEN}Para iniciar o projeto:${NC}"
echo ""
echo "1. Configure o banco de dados (comandos acima)"
echo "2. Inicie o backend:"
echo "   cd backend"
echo "   source venv/bin/activate"
echo "   uvicorn app.main:app --reload --host 0.0.0.0 --port 8000"
echo ""
echo "3. Em outro terminal, inicie o frontend:"
echo "   cd frontend"
echo "   npm run dev"
echo ""
echo -e "${GREEN}Acesse:${NC}"
echo "  Frontend: http://localhost:3000"
echo "  Backend API: http://localhost:8000"
echo "  API Docs: http://localhost:8000/docs"
echo ""
