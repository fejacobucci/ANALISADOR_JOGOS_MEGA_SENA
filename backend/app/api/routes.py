from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from typing import List, Optional
from pydantic import BaseModel
import os
import json

from ..models.database import get_db
from ..services.import_service import importar_xlsx
from ..services.analytics_service import AnalyticsService
from ..services.generator_service import GeneratorService

router = APIRouter()


# Schemas Pydantic
class FrequenciaResponse(BaseModel):
    dezena: int
    frequencia: int
    percentual: float


class EstatisticasGeraisResponse(BaseModel):
    total_concursos: int
    primeiro_concurso: dict
    ultimo_concurso: dict
    total_ganhadores_sena: int
    concursos_acumulados: int
    percentual_acumulados: float


class GerarJogosRequest(BaseModel):
    quantidade: int = 1
    metodo: str  # 'frequencia', 'par_impar', 'quadrantes', 'soma', 'trend', 'posicao', 'misto'
    parametros: Optional[dict] = {}


# Rotas de Importação
@router.post("/import/upload")
async def upload_arquivo(
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    """Upload e importação do arquivo XLSX"""
    if not file.filename.endswith('.xlsx'):
        raise HTTPException(status_code=400, detail="Arquivo deve ser .xlsx")

    # Salva arquivo temporariamente
    temp_path = f"/tmp/{file.filename}"
    with open(temp_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)

    async def gerar_progresso():
        """Gera eventos de progresso para streaming"""
        async for progress in importar_xlsx(temp_path, db):
            yield f"data: {json.dumps(progress)}\n\n"

        # Remove arquivo temporário
        if os.path.exists(temp_path):
            os.remove(temp_path)

    return StreamingResponse(
        gerar_progresso(),
        media_type="text/event-stream"
    )


@router.post("/import/file-path")
async def importar_por_caminho(
    file_path: str,
    db: Session = Depends(get_db)
):
    """Importa arquivo XLSX de um caminho específico"""
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Arquivo não encontrado")

    async def gerar_progresso():
        """Gera eventos de progresso para streaming"""
        async for progress in importar_xlsx(file_path, db):
            yield f"data: {json.dumps(progress)}\n\n"

    return StreamingResponse(
        gerar_progresso(),
        media_type="text/event-stream"
    )


# Rotas de Análises
@router.get("/analytics/estatisticas-gerais")
async def get_estatisticas_gerais(db: Session = Depends(get_db)):
    """Retorna estatísticas gerais do banco de dados"""
    analytics = AnalyticsService(db)
    return analytics.estatisticas_gerais()


@router.get("/analytics/frequencia-geral")
async def get_frequencia_geral(db: Session = Depends(get_db)):
    """Retorna frequência geral de todas as dezenas"""
    analytics = AnalyticsService(db)
    return analytics.frequencia_geral()


@router.get("/analytics/frequencia-anos/{anos}")
async def get_frequencia_anos(anos: int = 2, db: Session = Depends(get_db)):
    """Retorna frequência das dezenas nos últimos N anos"""
    analytics = AnalyticsService(db)
    return analytics.frequencia_ultimos_anos(anos)


@router.get("/analytics/frequencia-posicao")
async def get_frequencia_posicao(
    posicao: Optional[int] = None,
    db: Session = Depends(get_db)
):
    """Retorna frequência das dezenas por posição"""
    analytics = AnalyticsService(db)
    return analytics.frequencia_por_posicao(posicao)


@router.get("/analytics/intervalo-repeticoes-posicao")
async def get_intervalo_repeticoes_posicao(
    posicao: int = 1,
    limite: int = 20,
    db: Session = Depends(get_db)
):
    """Retorna intervalo em dias entre repetições de números em uma posição"""
    if posicao < 1 or posicao > 6:
        raise HTTPException(status_code=400, detail="Posição deve estar entre 1 e 6")

    analytics = AnalyticsService(db)
    return analytics.intervalo_repeticoes_por_posicao(posicao, limite)


@router.get("/analytics/numeros-quentes-frios")
async def get_numeros_quentes_frios(
    limite: int = 10,
    ultimos_concursos: int = 100,
    db: Session = Depends(get_db)
):
    """Retorna números quentes e frios"""
    analytics = AnalyticsService(db)
    return analytics.numeros_quentes_frios(limite, ultimos_concursos)


@router.get("/analytics/numeros-atrasados")
async def get_numeros_atrasados(
    limite: int = 10,
    db: Session = Depends(get_db)
):
    """Retorna números mais atrasados"""
    analytics = AnalyticsService(db)
    return analytics.numeros_atrasados(limite)


@router.get("/analytics/pares-impares")
async def get_analise_pares_impares(db: Session = Depends(get_db)):
    """Retorna análise de distribuição de pares e ímpares"""
    analytics = AnalyticsService(db)
    return analytics.analise_pares_impares()


@router.get("/analytics/quadrantes")
async def get_analise_quadrantes(db: Session = Depends(get_db)):
    """Retorna análise de distribuição por quadrantes"""
    analytics = AnalyticsService(db)
    return analytics.analise_quadrantes()


@router.get("/analytics/soma-dezenas")
async def get_analise_soma(db: Session = Depends(get_db)):
    """Retorna análise da soma das dezenas"""
    analytics = AnalyticsService(db)
    return analytics.analise_soma_dezenas()


@router.post("/analytics/verificar-combinacao")
async def verificar_combinacao(
    dezenas: List[int],
    db: Session = Depends(get_db)
):
    """Verifica se uma combinação já foi sorteada"""
    if len(dezenas) != 6:
        raise HTTPException(status_code=400, detail="Deve conter exatamente 6 dezenas")

    if any(d < 1 or d > 60 for d in dezenas):
        raise HTTPException(status_code=400, detail="Dezenas devem estar entre 1 e 60")

    analytics = AnalyticsService(db)
    ja_sorteada = analytics.combinacao_ja_sorteada(dezenas)

    return {
        "dezenas": sorted(dezenas),
        "ja_sorteada": ja_sorteada
    }


# Rotas de Geração de Jogos
@router.post("/generator/gerar")
async def gerar_jogos(
    request: GerarJogosRequest,
    db: Session = Depends(get_db)
):
    """Gera jogos baseados em diferentes métodos"""
    analytics = AnalyticsService(db)
    generator = GeneratorService(analytics)

    metodo = request.metodo
    quantidade = request.quantidade
    params = request.parametros or {}

    try:
        if metodo == "frequencia":
            jogos = generator.gerar_por_frequencia(
                quantidade,
                params.get('usar_quentes', True),
                params.get('top_n', 20)
            )
        elif metodo == "par_impar":
            jogos = generator.gerar_balanceado_par_impar(
                quantidade,
                params.get('pares', 3),
                params.get('impares', 3)
            )
        elif metodo == "quadrantes":
            jogos = generator.gerar_por_quadrantes(
                quantidade,
                params.get('distribuicao')
            )
        elif metodo == "soma":
            jogos = generator.gerar_por_soma(
                quantidade,
                params.get('soma_min', 150),
                params.get('soma_max', 220)
            )
        elif metodo == "trend":
            jogos = generator.gerar_trend(
                quantidade,
                params.get('ultimos_concursos', 50),
                params.get('top_n', 15)
            )
        elif metodo == "posicao":
            jogos = generator.gerar_por_posicao(
                quantidade,
                params.get('top_por_posicao', 10)
            )
        elif metodo == "misto":
            jogos = generator.gerar_misto(
                quantidade,
                params.get('usar_frequencia', True),
                params.get('usar_quadrantes', True),
                params.get('usar_soma', True),
                params.get('pares', 3)
            )
        else:
            raise HTTPException(status_code=400, detail=f"Método '{metodo}' não reconhecido")

        return {
            "metodo": metodo,
            "quantidade_gerada": len(jogos),
            "jogos": jogos,
            "parametros": params
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/generator/desdobramento")
async def gerar_desdobramento(
    dezenas: List[int],
    garantia: str = "quadra",
    db: Session = Depends(get_db)
):
    """Gera desdobramento matemático"""
    if len(dezenas) < 7 or len(dezenas) > 15:
        raise HTTPException(
            status_code=400,
            detail="Deve selecionar entre 7 e 15 dezenas"
        )

    if any(d < 1 or d > 60 for d in dezenas):
        raise HTTPException(
            status_code=400,
            detail="Dezenas devem estar entre 1 e 60"
        )

    analytics = AnalyticsService(db)
    generator = GeneratorService(analytics)

    jogos = generator.desdobramento_garantido(dezenas, garantia)

    return {
        "dezenas_selecionadas": sorted(dezenas),
        "garantia": garantia,
        "quantidade_jogos": len(jogos),
        "jogos": jogos
    }


# Rota de Health Check
@router.get("/health")
async def health_check():
    """Verifica se a API está funcionando"""
    return {"status": "ok", "message": "API Mega Sena está funcionando"}
