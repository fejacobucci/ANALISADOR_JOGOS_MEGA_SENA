# Quick Start - Mega Sena

## Instalação Rápida

### 1. Execute o script de setup
```bash
./setup.sh
```

### 2. Configure o banco de dados
```bash
# Crie o banco
psql -U felipejacobucci -c "CREATE DATABASE mega_sena_base;"

# Execute o schema
psql -U felipejacobucci -d mega_sena_base -f database/schema.sql
```

### 3. Inicie os servidores

**Terminal 1 - Backend:**
```bash
./start-backend.sh
```

**Terminal 2 - Frontend:**
```bash
./start-frontend.sh
```

## Acessar a Aplicação

- **Frontend**: http://localhost:3000
- **Backend API**: http://localhost:8000
- **Documentação da API**: http://localhost:8000/docs

## Primeiro Uso

1. Acesse http://localhost:3000
2. Vá em "Importar Dados"
3. Clique em "Iniciar Importação"
4. Aguarde a conclusão da importação (pode levar alguns minutos)
5. Explore as análises e gere seus jogos!

## Solução de Problemas

### Erro de conexão com o banco
Verifique se o PostgreSQL está rodando:
```bash
pg_ctl status
```

### Porta já em uso
Backend (8000) ou Frontend (3000) já estão em uso? Mude as portas:
- Backend: Edite `start-backend.sh` e mude `--port 8000`
- Frontend: Edite `frontend/vite.config.ts` e mude `port: 3000`

### Módulos não encontrados
Backend:
```bash
cd backend
source venv/bin/activate
pip install -r requirements.txt
```

Frontend:
```bash
cd frontend
npm install
```

## Estrutura Básica

```
MEGA_SENA/
├── backend/          # API em Python (FastAPI)
├── frontend/         # Interface em React
├── database/         # Schema SQL
├── resultados_MegaSena.xlsx  # Dados históricos
└── README.md         # Documentação completa
```

## Comandos Úteis

### Backend
```bash
cd backend
source venv/bin/activate

# Iniciar servidor
uvicorn app.main:app --reload

# Verificar rotas
python -m app.main
```

### Frontend
```bash
cd frontend

# Iniciar dev server
npm run dev

# Build para produção
npm run build

# Preview build
npm run preview
```

### Banco de Dados
```bash
# Conectar ao banco
psql -U felipejacobucci -d mega_sena_base

# Ver tabelas
\dt

# Ver dados de uma tabela
SELECT * FROM concursos LIMIT 5;

# Resetar banco (cuidado!)
DROP DATABASE mega_sena_base;
CREATE DATABASE mega_sena_base;
\c mega_sena_base
\i database/schema.sql
```

## Próximos Passos

Consulte o [README.md](README.md) para documentação completa sobre:
- Todas as funcionalidades
- API endpoints
- Como adicionar novas análises
- Detalhes dos algoritmos
