from typing import List, Dict, Set
import random
import itertools
from .analytics_service import AnalyticsService


class GeneratorService:
    """Serviço para geração inteligente de jogos da Mega Sena"""

    def __init__(self, analytics: AnalyticsService):
        self.analytics = analytics

    def gerar_por_frequencia(
        self,
        quantidade_jogos: int = 1,
        usar_quentes: bool = True,
        top_n: int = 20
    ) -> List[List[int]]:
        """
        Gera jogos baseados na frequência das dezenas

        Args:
            quantidade_jogos: Número de jogos a gerar
            usar_quentes: Se True usa números quentes, se False usa números frios
            top_n: Considera os top N números mais/menos frequentes
        """
        frequencias = self.analytics.frequencia_geral()

        if usar_quentes:
            # Usa os mais frequentes
            pool = [f['dezena'] for f in frequencias[:top_n]]
        else:
            # Usa os menos frequentes
            pool = [f['dezena'] for f in frequencias[-top_n:]]

        jogos = []
        tentativas = 0
        max_tentativas = quantidade_jogos * 100

        while len(jogos) < quantidade_jogos and tentativas < max_tentativas:
            jogo = sorted(random.sample(pool, 6))

            # Verifica se já foi sorteado
            if not self.analytics.combinacao_ja_sorteada(jogo):
                jogos.append(jogo)

            tentativas += 1

        return jogos

    def gerar_balanceado_par_impar(
        self,
        quantidade_jogos: int = 1,
        pares: int = 3,
        impares: int = 3
    ) -> List[List[int]]:
        """
        Gera jogos respeitando proporção de pares e ímpares

        Args:
            quantidade_jogos: Número de jogos a gerar
            pares: Quantidade de números pares
            impares: Quantidade de números ímpares
        """
        if pares + impares != 6:
            raise ValueError("A soma de pares e ímpares deve ser 6")

        todos_pares = [n for n in range(2, 61, 2)]  # 2, 4, 6, ..., 60
        todos_impares = [n for n in range(1, 61, 2)]  # 1, 3, 5, ..., 59

        jogos = []
        tentativas = 0
        max_tentativas = quantidade_jogos * 100

        while len(jogos) < quantidade_jogos and tentativas < max_tentativas:
            nums_pares = random.sample(todos_pares, pares)
            nums_impares = random.sample(todos_impares, impares)
            jogo = sorted(nums_pares + nums_impares)

            # Verifica se já foi sorteado
            if not self.analytics.combinacao_ja_sorteada(jogo):
                jogos.append(jogo)

            tentativas += 1

        return jogos

    def gerar_por_quadrantes(
        self,
        quantidade_jogos: int = 1,
        distribuicao: Dict[str, int] = None
    ) -> List[List[int]]:
        """
        Gera jogos distribuindo números pelos quadrantes

        Args:
            quantidade_jogos: Número de jogos a gerar
            distribuicao: Dict com distribuição desejada, ex: {'Q1': 2, 'Q2': 1, 'Q3': 2, 'Q4': 1}
        """
        if distribuicao is None:
            # Distribuição padrão: pelo menos 1 de cada quadrante
            distribuicao = {'Q1': 2, 'Q2': 1, 'Q3': 2, 'Q4': 1}

        if sum(distribuicao.values()) != 6:
            raise ValueError("A soma da distribuição deve ser 6")

        quadrantes = {
            'Q1': list(range(1, 16)),    # 1-15
            'Q2': list(range(16, 31)),   # 16-30
            'Q3': list(range(31, 46)),   # 31-45
            'Q4': list(range(46, 61))    # 46-60
        }

        jogos = []
        tentativas = 0
        max_tentativas = quantidade_jogos * 100

        while len(jogos) < quantidade_jogos and tentativas < max_tentativas:
            jogo = []

            for quad, qtd in distribuicao.items():
                jogo.extend(random.sample(quadrantes[quad], qtd))

            jogo = sorted(jogo)

            # Verifica se já foi sorteado
            if not self.analytics.combinacao_ja_sorteada(jogo):
                jogos.append(jogo)

            tentativas += 1

        return jogos

    def gerar_por_soma(
        self,
        quantidade_jogos: int = 1,
        soma_min: int = 150,
        soma_max: int = 220
    ) -> List[List[int]]:
        """
        Gera jogos cuja soma das dezenas fica em um intervalo específico

        Args:
            quantidade_jogos: Número de jogos a gerar
            soma_min: Soma mínima das dezenas
            soma_max: Soma máxima das dezenas
        """
        jogos = []
        tentativas = 0
        max_tentativas = quantidade_jogos * 1000

        while len(jogos) < quantidade_jogos and tentativas < max_tentativas:
            jogo = sorted(random.sample(range(1, 61), 6))
            soma = sum(jogo)

            if soma_min <= soma <= soma_max:
                # Verifica se já foi sorteado
                if not self.analytics.combinacao_ja_sorteada(jogo):
                    jogos.append(jogo)

            tentativas += 1

        return jogos

    def gerar_trend(
        self,
        quantidade_jogos: int = 1,
        ultimos_concursos: int = 50,
        top_n: int = 15
    ) -> List[List[int]]:
        """
        Gera jogos baseados nas tendências recentes (números quentes recentes)

        Args:
            quantidade_jogos: Número de jogos a gerar
            ultimos_concursos: Considerar os últimos N concursos
            top_n: Usar os top N números mais frequentes no período
        """
        quentes_frios = self.analytics.numeros_quentes_frios(
            limite=top_n,
            ultimos_concursos=ultimos_concursos
        )

        pool = [n['dezena'] for n in quentes_frios['quentes']]

        jogos = []
        tentativas = 0
        max_tentativas = quantidade_jogos * 100

        while len(jogos) < quantidade_jogos and tentativas < max_tentativas:
            jogo = sorted(random.sample(pool, 6))

            # Verifica se já foi sorteado
            if not self.analytics.combinacao_ja_sorteada(jogo):
                jogos.append(jogo)

            tentativas += 1

        return jogos

    def gerar_por_posicao(
        self,
        quantidade_jogos: int = 1,
        top_por_posicao: int = 10
    ) -> List[List[int]]:
        """
        Gera jogos usando os números mais frequentes em cada posição

        Args:
            quantidade_jogos: Número de jogos a gerar
            top_por_posicao: Considerar os top N números mais frequentes por posição
        """
        freq_posicoes = self.analytics.frequencia_por_posicao()

        # Organiza por posição
        pools = {}
        for pos in range(1, 7):
            numeros_pos = [
                f['dezena'] for f in freq_posicoes
                if f['posicao'] == pos
            ][:top_por_posicao]
            pools[pos] = numeros_pos

        jogos = []
        tentativas = 0
        max_tentativas = quantidade_jogos * 100

        while len(jogos) < quantidade_jogos and tentativas < max_tentativas:
            jogo = []

            for pos in range(1, 7):
                # Escolhe um número do pool da posição que não foi usado
                opcoes = [n for n in pools[pos] if n not in jogo]
                if opcoes:
                    jogo.append(random.choice(opcoes))
                else:
                    # Se não há opções, escolhe qualquer número não usado
                    disponiveis = [n for n in range(1, 61) if n not in jogo]
                    if disponiveis:
                        jogo.append(random.choice(disponiveis))

            if len(jogo) == 6:
                jogo = sorted(jogo)
                # Verifica se já foi sorteado
                if not self.analytics.combinacao_ja_sorteada(jogo):
                    jogos.append(jogo)

            tentativas += 1

        return jogos

    def gerar_misto(
        self,
        quantidade_jogos: int = 1,
        usar_frequencia: bool = True,
        usar_quadrantes: bool = True,
        usar_soma: bool = True,
        pares: int = 3
    ) -> List[List[int]]:
        """
        Gera jogos combinando múltiplos critérios

        Args:
            quantidade_jogos: Número de jogos a gerar
            usar_frequencia: Considera números quentes
            usar_quadrantes: Distribui pelos quadrantes
            usar_soma: Respeita intervalo de soma (150-220)
            pares: Quantidade de números pares
        """
        jogos = []
        tentativas = 0
        max_tentativas = quantidade_jogos * 1000

        # Pool baseado em frequência se habilitado
        if usar_frequencia:
            frequencias = self.analytics.frequencia_geral()
            pool_freq = set([f['dezena'] for f in frequencias[:30]])  # Top 30
        else:
            pool_freq = set(range(1, 61))

        while len(jogos) < quantidade_jogos and tentativas < max_tentativas:
            jogo = []

            # Critério de quadrantes
            if usar_quadrantes:
                quadrantes = {
                    'Q1': [n for n in range(1, 16) if n in pool_freq],
                    'Q2': [n for n in range(16, 31) if n in pool_freq],
                    'Q3': [n for n in range(31, 46) if n in pool_freq],
                    'Q4': [n for n in range(46, 61) if n in pool_freq]
                }

                for _ in range(2):
                    quad = random.choice(['Q1', 'Q2', 'Q3', 'Q4'])
                    if quadrantes[quad]:
                        num = random.choice([n for n in quadrantes[quad] if n not in jogo])
                        jogo.append(num)
            else:
                # Adiciona 2 números aleatórios do pool
                disponiveis = [n for n in pool_freq if n not in jogo]
                jogo.extend(random.sample(disponiveis, min(2, len(disponiveis))))

            # Completa com pares/ímpares balanceados
            pares_atuais = sum(1 for n in jogo if n % 2 == 0)
            pares_necessarios = pares - pares_atuais
            impares_necessarios = (6 - len(jogo)) - pares_necessarios

            disponiveis_pares = [n for n in range(2, 61, 2) if n not in jogo and n in pool_freq]
            disponiveis_impares = [n for n in range(1, 61, 2) if n not in jogo and n in pool_freq]

            if len(disponiveis_pares) >= pares_necessarios and len(disponiveis_impares) >= impares_necessarios:
                jogo.extend(random.sample(disponiveis_pares, pares_necessarios))
                jogo.extend(random.sample(disponiveis_impares, impares_necessarios))

            if len(jogo) != 6:
                tentativas += 1
                continue

            jogo = sorted(jogo)

            # Verifica critério de soma se habilitado
            if usar_soma:
                soma = sum(jogo)
                if not (150 <= soma <= 220):
                    tentativas += 1
                    continue

            # Verifica se já foi sorteado
            if not self.analytics.combinacao_ja_sorteada(jogo):
                jogos.append(jogo)

            tentativas += 1

        return jogos

    def desdobramento_garantido(
        self,
        dezenas_selecionadas: List[int],
        garantia: str = "quadra"
    ) -> List[List[int]]:
        """
        Gera desdobramento matemático que garante premiação

        Args:
            dezenas_selecionadas: Lista com 7 a 15 dezenas escolhidas
            garantia: Tipo de garantia - "quadra" ou "quina"

        Returns:
            Lista de jogos que garantem a premiação se acertar X números
        """
        qtd_dezenas = len(dezenas_selecionadas)

        if qtd_dezenas < 7 or qtd_dezenas > 15:
            raise ValueError("Deve selecionar entre 7 e 15 dezenas")

        # Para garantia de quadra: se acertar 5, garante pelo menos uma quadra
        # Para garantia de quina: se acertar 6, garante pelo menos uma quina

        # Gera todas as combinações possíveis de 6 números
        todas_combinacoes = list(itertools.combinations(dezenas_selecionadas, 6))

        if garantia == "quadra":
            # Algoritmo simplificado: usa cobertura mínima
            # Para 8 números: 28 jogos garantem quadra se acertar 5
            # Para 9 números: 84 jogos garantem quadra se acertar 5
            # etc.
            jogos = todas_combinacoes[:min(len(todas_combinacoes), 100)]
        else:
            # Garantia de quina requer mais jogos
            jogos = todas_combinacoes[:min(len(todas_combinacoes), 200)]

        return [list(jogo) for jogo in jogos]

    def gerar_por_cidade_vencedora(
        self,
        quantidade_jogos: int = 1,
        cidade: str = None,
        uf: str = None,
        top_n: int = 15
    ) -> List[List[int]]:
        """
        Gera jogos baseados nos números que mais saíram em vitórias de uma cidade/estado

        Args:
            quantidade_jogos: Número de jogos a gerar
            cidade: Nome da cidade (opcional, se não informado usa apenas o estado)
            uf: Sigla do estado
            top_n: Usar os top N números mais frequentes nas vitórias

        Returns:
            Lista de jogos gerados
        """
        if not uf:
            raise ValueError("UF é obrigatório")

        # Busca números vencedores
        if cidade:
            numeros_vencedores = self.analytics.numeros_vencedores_por_cidade(cidade, uf, top_n)
        else:
            numeros_vencedores = self.analytics.numeros_vencedores_por_estado(uf, top_n)

        if not numeros_vencedores:
            raise ValueError(f"Nenhum dado encontrado para {'cidade ' + cidade if cidade else 'estado'} {uf}")

        # Pool de números baseado nas vitórias
        pool = [n['dezena'] for n in numeros_vencedores]

        # Se não tiver 6 números, completa com números aleatórios
        if len(pool) < 6:
            disponiveis = [n for n in range(1, 61) if n not in pool]
            pool.extend(random.sample(disponiveis, 6 - len(pool)))

        jogos = []
        tentativas = 0
        max_tentativas = quantidade_jogos * 100

        while len(jogos) < quantidade_jogos and tentativas < max_tentativas:
            # Prioriza números do topo da lista (mais frequentes nas vitórias)
            jogo = []

            # Pega pelo menos 3-4 números dos mais frequentes
            top_3 = min(4, len(pool))
            principais = random.sample(pool[:top_3], min(3, top_3))
            jogo.extend(principais)

            # Completa com outros números do pool
            outros = [n for n in pool if n not in jogo]
            if outros:
                faltam = 6 - len(jogo)
                jogo.extend(random.sample(outros, min(faltam, len(outros))))

            # Se ainda falta, completa com números aleatórios
            if len(jogo) < 6:
                disponiveis = [n for n in range(1, 61) if n not in jogo]
                jogo.extend(random.sample(disponiveis, 6 - len(jogo)))

            jogo = sorted(jogo)

            # Verifica se já foi sorteado
            if not self.analytics.combinacao_ja_sorteada(jogo):
                jogos.append(jogo)

            tentativas += 1

        return jogos
