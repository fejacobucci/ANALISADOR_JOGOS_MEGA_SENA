#!/bin/bash

echo "Iniciando Backend da Mega Sena..."
echo ""

cd backend

# Ativa ambiente virtual
source venv/bin/activate

# Inicia o servidor
echo "Servidor rodando em: http://localhost:8000"
echo "Documentação da API: http://localhost:8000/docs"
echo ""

uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
