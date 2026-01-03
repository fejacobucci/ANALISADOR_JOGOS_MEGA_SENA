from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .api import routes
from .models.database import engine, Base

# Cria as tabelas no banco de dados
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Mega Sena API",
    description="API para análise e geração de jogos da Mega Sena",
    version="1.0.0"
)

# Configuração CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Em produção, especificar origens permitidas
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Inclui as rotas
app.include_router(routes.router, prefix="/api/v1", tags=["Mega Sena"])


@app.get("/")
async def root():
    return {
        "message": "Bem-vindo à API Mega Sena",
        "docs": "/docs",
        "version": "1.0.0"
    }
