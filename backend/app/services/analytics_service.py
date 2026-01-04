from sqlalchemy.orm import Session
from sqlalchemy import func, text, and_, desc
from ..models.models import Concurso, DezenaSorteada
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import itertools


class AnalyticsService:
    """Serviço para análises estatísticas da Mega Sena"""

    def __init__(self, db: Session):
        self.db = db

    def frequencia_geral(self) -> List[Dict]:
        """Retorna frequência de todas as dezenas ao longo do tempo"""
        resultado = self.db.query(
            DezenaSorteada.dezena,
            func.count(DezenaSorteada.id).label('frequencia')
        ).group_by(
            DezenaSorteada.dezena
        ).order_by(
            desc('frequencia')
        ).all()

        total_sorteios = self.db.query(func.count(func.distinct(Concurso.id))).scalar()

        return [
            {
                'dezena': r.dezena,
                'frequencia': r.frequencia,
                'percentual': round((r.frequencia / total_sorteios) * 100, 2) if total_sorteios > 0 else 0
            }
            for r in resultado
        ]

    def frequencia_ultimos_anos(self, anos: int = 2) -> List[Dict]:
        """Retorna frequência das dezenas nos últimos N anos"""
        data_limite = datetime.now() - timedelta(days=anos * 365)

        resultado = self.db.query(
            DezenaSorteada.dezena,
            func.count(DezenaSorteada.id).label('frequencia')
        ).join(
            Concurso
        ).filter(
            Concurso.data_sorteio >= data_limite
        ).group_by(
            DezenaSorteada.dezena
        ).order_by(
            desc('frequencia')
        ).all()

        total_sorteios = self.db.query(
            func.count(func.distinct(Concurso.id))
        ).filter(
            Concurso.data_sorteio >= data_limite
        ).scalar()

        return [
            {
                'dezena': r.dezena,
                'frequencia': r.frequencia,
                'percentual': round((r.frequencia / total_sorteios) * 100, 2) if total_sorteios > 0 else 0
            }
            for r in resultado
        ]

    def frequencia_por_posicao(self, posicao: Optional[int] = None) -> List[Dict]:
        """Retorna frequência das dezenas por posição"""
        query = self.db.query(
            DezenaSorteada.posicao,
            DezenaSorteada.dezena,
            func.count(DezenaSorteada.id).label('frequencia')
        )

        if posicao:
            query = query.filter(DezenaSorteada.posicao == posicao)

        resultado = query.group_by(
            DezenaSorteada.posicao,
            DezenaSorteada.dezena
        ).order_by(
            DezenaSorteada.posicao,
            desc('frequencia')
        ).all()

        return [
            {
                'posicao': r.posicao,
                'dezena': r.dezena,
                'frequencia': r.frequencia
            }
            for r in resultado
        ]

    def numeros_quentes_frios(self, limite: int = 10, ultimos_concursos: int = 100) -> Dict:
        """
        Retorna números quentes (mais frequentes) e frios (menos frequentes)

        Args:
            limite: Quantidade de números a retornar em cada categoria
            ultimos_concursos: Considerar os últimos N concursos
        """
        # Busca os últimos concursos
        concursos_ids = self.db.query(Concurso.id).order_by(
            desc(Concurso.numero_concurso)
        ).limit(ultimos_concursos).subquery()

        # Frequência nos últimos concursos
        resultado = self.db.query(
            DezenaSorteada.dezena,
            func.count(DezenaSorteada.id).label('frequencia')
        ).filter(
            DezenaSorteada.concurso_id.in_(concursos_ids)
        ).group_by(
            DezenaSorteada.dezena
        ).order_by(
            desc('frequencia')
        ).all()

        # Números quentes (mais frequentes)
        quentes = [
            {'dezena': r.dezena, 'frequencia': r.frequencia}
            for r in resultado[:limite]
        ]

        # Números frios (menos frequentes)
        frios = [
            {'dezena': r.dezena, 'frequencia': r.frequencia}
            for r in resultado[-limite:]
        ]

        return {
            'quentes': quentes,
            'frios': frios,
            'ultimos_concursos': ultimos_concursos
        }

    def numeros_atrasados(self, limite: int = 10) -> List[Dict]:
        """Retorna números que estão há mais tempo sem sair"""
        # Para cada número de 1 a 60, encontra o último concurso em que saiu
        resultado = []

        ultimo_concurso = self.db.query(
            func.max(Concurso.numero_concurso)
        ).scalar()

        for dezena in range(1, 61):
            ultimo_sorteio = self.db.query(
                Concurso.numero_concurso,
                Concurso.data_sorteio
            ).join(
                DezenaSorteada
            ).filter(
                DezenaSorteada.dezena == dezena
            ).order_by(
                desc(Concurso.numero_concurso)
            ).first()

            if ultimo_sorteio:
                atraso = ultimo_concurso - ultimo_sorteio.numero_concurso
                resultado.append({
                    'dezena': dezena,
                    'ultimo_concurso': ultimo_sorteio.numero_concurso,
                    'data_ultimo_sorteio': ultimo_sorteio.data_sorteio.strftime('%Y-%m-%d'),
                    'concursos_atrasados': atraso
                })

        # Ordena por atraso
        resultado = sorted(resultado, key=lambda x: x['concursos_atrasados'], reverse=True)

        return resultado[:limite]

    def analise_pares_impares(self) -> Dict:
        """Analisa a distribuição de pares e ímpares nos sorteios"""
        resultado = self.db.query(
            Concurso.numero_concurso,
            func.sum(func.cast(DezenaSorteada.dezena % 2 == 0, type_=func.INTEGER())).label('pares'),
            func.sum(func.cast(DezenaSorteada.dezena % 2 == 1, type_=func.INTEGER())).label('impares')
        ).join(
            DezenaSorteada
        ).group_by(
            Concurso.id, Concurso.numero_concurso
        ).all()

        # Estatísticas de distribuição
        distribuicao = {}
        for r in resultado:
            chave = f"{r.pares}P-{r.impares}I"
            distribuicao[chave] = distribuicao.get(chave, 0) + 1

        # Calcula percentuais
        total = len(resultado)
        distribuicao_percentual = {
            k: {
                'quantidade': v,
                'percentual': round((v / total) * 100, 2)
            }
            for k, v in distribuicao.items()
        }

        return {
            'distribuicao': distribuicao_percentual,
            'mais_comum': max(distribuicao.items(), key=lambda x: x[1])[0] if distribuicao else None
        }

    def analise_quadrantes(self) -> Dict:
        """
        Divide o volante em 4 quadrantes e analisa a distribuição
        Q1: 1-15, Q2: 16-30, Q3: 31-45, Q4: 46-60
        """
        quadrantes = {
            'Q1': (1, 15),
            'Q2': (16, 30),
            'Q3': (31, 45),
            'Q4': (46, 60)
        }

        resultado = {}

        for nome_quad, (inicio, fim) in quadrantes.items():
            frequencia = self.db.query(
                func.count(DezenaSorteada.id)
            ).filter(
                and_(
                    DezenaSorteada.dezena >= inicio,
                    DezenaSorteada.dezena <= fim
                )
            ).scalar()

            resultado[nome_quad] = {
                'range': f'{inicio}-{fim}',
                'frequencia': frequencia
            }

        total = sum(r['frequencia'] for r in resultado.values())

        for quad in resultado.values():
            quad['percentual'] = round((quad['frequencia'] / total) * 100, 2) if total > 0 else 0

        return resultado

    def analise_soma_dezenas(self) -> Dict:
        """Analisa a soma das dezenas em cada sorteio"""
        resultado = self.db.query(
            Concurso.numero_concurso,
            Concurso.data_sorteio,
            func.sum(DezenaSorteada.dezena).label('soma')
        ).join(
            DezenaSorteada
        ).group_by(
            Concurso.id, Concurso.numero_concurso, Concurso.data_sorteio
        ).all()

        somas = [r.soma for r in resultado]

        return {
            'minima': min(somas) if somas else 0,
            'maxima': max(somas) if somas else 0,
            'media': round(sum(somas) / len(somas), 2) if somas else 0,
            'mediana': sorted(somas)[len(somas) // 2] if somas else 0,
            'distribuicao': self._criar_histograma(somas, 10)
        }

    def _criar_histograma(self, valores: List[int], bins: int) -> List[Dict]:
        """Cria histograma dos valores"""
        if not valores:
            return []

        minimo = min(valores)
        maximo = max(valores)
        intervalo = (maximo - minimo) / bins

        histograma = []
        for i in range(bins):
            inicio = minimo + (i * intervalo)
            fim = inicio + intervalo
            count = sum(1 for v in valores if inicio <= v < fim)

            histograma.append({
                'range': f'{int(inicio)}-{int(fim)}',
                'quantidade': count
            })

        return histograma

    def combinacao_ja_sorteada(self, dezenas: List[int]) -> bool:
        """Verifica se uma combinação já foi sorteada"""
        if len(dezenas) != 6:
            return False

        dezenas_ordenadas = sorted(dezenas)

        # Busca todos os concursos
        concursos = self.db.query(Concurso.id).all()

        for concurso in concursos:
            dezenas_concurso = self.db.query(
                DezenaSorteada.dezena
            ).filter(
                DezenaSorteada.concurso_id == concurso.id
            ).order_by(
                DezenaSorteada.dezena
            ).all()

            dezenas_concurso_lista = sorted([d.dezena for d in dezenas_concurso])

            if dezenas_ordenadas == dezenas_concurso_lista:
                return True

        return False

    def estatisticas_gerais(self) -> Dict:
        """Retorna estatísticas gerais do banco de dados"""
        total_concursos = self.db.query(func.count(Concurso.id)).scalar()
        primeiro_concurso = self.db.query(Concurso).order_by(Concurso.numero_concurso).first()
        ultimo_concurso = self.db.query(Concurso).order_by(desc(Concurso.numero_concurso)).first()

        total_ganhadores_sena = self.db.query(func.sum(Concurso.ganhadores_sena)).scalar()
        concursos_acumulados = self.db.query(func.count(Concurso.id)).filter(
            Concurso.ganhadores_sena == 0
        ).scalar()

        return {
            'total_concursos': total_concursos,
            'primeiro_concurso': {
                'numero': primeiro_concurso.numero_concurso if primeiro_concurso else None,
                'data': primeiro_concurso.data_sorteio.strftime('%Y-%m-%d') if primeiro_concurso else None
            },
            'ultimo_concurso': {
                'numero': ultimo_concurso.numero_concurso if ultimo_concurso else None,
                'data': ultimo_concurso.data_sorteio.strftime('%Y-%m-%d') if ultimo_concurso else None
            },
            'total_ganhadores_sena': total_ganhadores_sena or 0,
            'concursos_acumulados': concursos_acumulados or 0,
            'percentual_acumulados': round((concursos_acumulados / total_concursos) * 100, 2) if total_concursos > 0 else 0
        }

    def intervalo_repeticoes_por_posicao(self, posicao: int = 1, limite: int = 20) -> List[Dict]:
        """
        Analisa o intervalo em dias entre repetições de números em uma posição específica

        Args:
            posicao: Posição a analisar (1-6)
            limite: Quantidade de números a retornar

        Returns:
            Lista com dezenas e seus intervalos médios, mínimos e máximos
        """
        # Busca todos os sorteios de uma posição específica ordenados por data
        sorteios = self.db.query(
            DezenaSorteada.dezena,
            Concurso.data_sorteio,
            Concurso.numero_concurso
        ).join(
            Concurso
        ).filter(
            DezenaSorteada.posicao == posicao
        ).order_by(
            Concurso.data_sorteio
        ).all()

        # Agrupa por dezena
        dezenas_dados = {}
        for sorteio in sorteios:
            dezena = sorteio.dezena
            if dezena not in dezenas_dados:
                dezenas_dados[dezena] = {
                    'dezena': dezena,
                    'datas': [],
                    'intervalos': []
                }
            dezenas_dados[dezena]['datas'].append(sorteio.data_sorteio)

        # Calcula intervalos para cada dezena
        resultado = []
        for dezena, dados in dezenas_dados.items():
            datas = dados['datas']

            if len(datas) < 2:
                # Se apareceu apenas uma vez, não há intervalo
                continue

            # Calcula intervalos em dias
            intervalos = []
            for i in range(1, len(datas)):
                diff = (datas[i] - datas[i-1]).days
                intervalos.append(diff)

            if intervalos:
                resultado.append({
                    'dezena': dezena,
                    'frequencia': len(datas),
                    'intervalo_medio': round(sum(intervalos) / len(intervalos), 1),
                    'intervalo_minimo': min(intervalos),
                    'intervalo_maximo': max(intervalos),
                    'ultimo_sorteio': datas[-1].strftime('%Y-%m-%d'),
                    'total_intervalos': len(intervalos)
                })

        # Ordena por frequência (dezenas mais frequentes primeiro)
        resultado.sort(key=lambda x: x['frequencia'], reverse=True)

        return resultado[:limite]

    def analise_cidades_ganhadoras(self, limite: int = 20) -> Dict:
        """
        Analisa as cidades que mais tiveram ganhadores da Mega Sena

        Args:
            limite: Quantidade de cidades a retornar

        Returns:
            Estatísticas de cidades ganhadoras
        """
        from ..models.models import CidadeGanhadora

        # Conta vitórias por cidade
        cidades_ranking = self.db.query(
            CidadeGanhadora.cidade,
            CidadeGanhadora.uf,
            func.count(CidadeGanhadora.id).label('vitorias')
        ).filter(
            CidadeGanhadora.cidade.isnot(None)
        ).group_by(
            CidadeGanhadora.cidade,
            CidadeGanhadora.uf
        ).order_by(
            desc('vitorias')
        ).limit(limite).all()

        # Conta vitórias por estado
        estados_ranking = self.db.query(
            CidadeGanhadora.uf,
            func.count(CidadeGanhadora.id).label('vitorias')
        ).filter(
            CidadeGanhadora.uf.isnot(None)
        ).group_by(
            CidadeGanhadora.uf
        ).order_by(
            desc('vitorias')
        ).all()

        total_vitorias = self.db.query(func.count(CidadeGanhadora.id)).scalar()

        return {
            'cidades': [
                {
                    'cidade': c.cidade,
                    'uf': c.uf,
                    'vitorias': c.vitorias,
                    'percentual': round((c.vitorias / total_vitorias) * 100, 2) if total_vitorias > 0 else 0
                }
                for c in cidades_ranking
            ],
            'estados': [
                {
                    'uf': e.uf,
                    'vitorias': e.vitorias,
                    'percentual': round((e.vitorias / total_vitorias) * 100, 2) if total_vitorias > 0 else 0
                }
                for e in estados_ranking
            ],
            'total_vitorias': total_vitorias
        }

    def numeros_vencedores_por_cidade(self, cidade: str, uf: str, limite: int = 10) -> List[Dict]:
        """
        Retorna os números que mais saíram em jogos vencedores de uma cidade específica

        Args:
            cidade: Nome da cidade
            uf: Sigla do estado
            limite: Quantidade de números a retornar

        Returns:
            Lista de dezenas mais sorteadas em jogos vencedores da cidade
        """
        from ..models.models import CidadeGanhadora

        # Busca concursos vencedores da cidade
        concursos_vencedores = self.db.query(
            CidadeGanhadora.concurso_id
        ).filter(
            CidadeGanhadora.cidade == cidade,
            CidadeGanhadora.uf == uf
        ).all()

        concursos_ids = [c.concurso_id for c in concursos_vencedores]

        if not concursos_ids:
            return []

        # Conta frequência das dezenas nesses concursos
        frequencias = self.db.query(
            DezenaSorteada.dezena,
            func.count(DezenaSorteada.id).label('frequencia')
        ).filter(
            DezenaSorteada.concurso_id.in_(concursos_ids)
        ).group_by(
            DezenaSorteada.dezena
        ).order_by(
            desc('frequencia')
        ).limit(limite).all()

        total_concursos = len(concursos_ids)

        return [
            {
                'dezena': f.dezena,
                'frequencia': f.frequencia,
                'percentual': round((f.frequencia / (total_concursos * 6)) * 100, 2) if total_concursos > 0 else 0,
                'total_concursos_cidade': total_concursos
            }
            for f in frequencias
        ]

    def numeros_vencedores_por_estado(self, uf: str, limite: int = 10) -> List[Dict]:
        """
        Retorna os números que mais saíram em jogos vencedores de um estado

        Args:
            uf: Sigla do estado
            limite: Quantidade de números a retornar

        Returns:
            Lista de dezenas mais sorteadas em jogos vencedores do estado
        """
        from ..models.models import CidadeGanhadora

        # Busca concursos vencedores do estado
        concursos_vencedores = self.db.query(
            CidadeGanhadora.concurso_id
        ).filter(
            CidadeGanhadora.uf == uf
        ).all()

        concursos_ids = [c.concurso_id for c in concursos_vencedores]

        if not concursos_ids:
            return []

        # Conta frequência das dezenas nesses concursos
        frequencias = self.db.query(
            DezenaSorteada.dezena,
            func.count(DezenaSorteada.id).label('frequencia')
        ).filter(
            DezenaSorteada.concurso_id.in_(concursos_ids)
        ).group_by(
            DezenaSorteada.dezena
        ).order_by(
            desc('frequencia')
        ).limit(limite).all()

        total_concursos = len(concursos_ids)

        return [
            {
                'dezena': f.dezena,
                'frequencia': f.frequencia,
                'percentual': round((f.frequencia / (total_concursos * 6)) * 100, 2) if total_concursos > 0 else 0,
                'total_concursos_estado': total_concursos
            }
            for f in frequencias
        ]
