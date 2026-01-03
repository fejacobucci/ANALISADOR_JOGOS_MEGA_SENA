import pandas as pd
from datetime import datetime
from sqlalchemy.orm import Session
from typing import Generator, Dict
from ..models.models import Concurso, DezenaSorteada, CidadeGanhadora
import re


def limpar_valor_monetario(valor: str) -> float:
    """Converte string de valor monetário para float"""
    if pd.isna(valor) or valor == '' or valor == 'NaN':
        return None
    if isinstance(valor, (int, float)):
        return float(valor)
    # Remove R$, pontos e substitui vírgula por ponto
    valor_limpo = str(valor).replace('R$', '').replace('.', '').replace(',', '.').strip()
    try:
        return float(valor_limpo)
    except ValueError:
        return None


def parse_data(data_str: str) -> datetime:
    """Converte string de data para datetime"""
    if pd.isna(data_str):
        return None

    # Tenta diferentes formatos de data
    formatos = ['%d/%m/%Y', '%Y-%m-%d', '%d-%m-%Y']
    for formato in formatos:
        try:
            return datetime.strptime(str(data_str), formato)
        except ValueError:
            continue
    return None


def parse_cidades(cidades_str: str) -> list:
    """Parse string de cidades e retorna lista de dicts com cidade e UF"""
    if pd.isna(cidades_str) or cidades_str == '':
        return []

    cidades = []
    # Divide por vírgula ou ponto-e-vírgula
    partes = re.split(r'[,;]', str(cidades_str))

    for parte in partes:
        parte = parte.strip()
        if '/' in parte:
            cidade, uf = parte.rsplit('/', 1)
            cidades.append({
                'cidade': cidade.strip(),
                'uf': uf.strip()
            })

    return cidades


async def importar_xlsx(
    file_path: str,
    db: Session,
    progress_callback: callable = None
) -> Generator[Dict, None, None]:
    """
    Importa dados do arquivo XLSX para o banco de dados

    Args:
        file_path: Caminho do arquivo XLSX
        db: Sessão do banco de dados
        progress_callback: Função de callback para reportar progresso

    Yields:
        Dict com informações de progresso
    """
    try:
        # Lê o arquivo Excel
        df = pd.read_excel(file_path)
        total_registros = len(df)

        yield {
            'status': 'iniciado',
            'total': total_registros,
            'processados': 0,
            'message': f'Iniciando importação de {total_registros} registros'
        }

        # Limpa tabela antes de importar (opcional - pode ser configurado)
        # db.query(Concurso).delete()
        # db.commit()

        processados = 0
        erros = 0

        for index, row in df.iterrows():
            try:
                # Verifica se concurso já existe
                concurso_existente = db.query(Concurso).filter(
                    Concurso.numero_concurso == int(row['Concurso'])
                ).first()

                if concurso_existente:
                    # Pula se já existe
                    processados += 1
                    continue

                # Cria objeto Concurso
                concurso = Concurso(
                    numero_concurso=int(row['Concurso']),
                    data_sorteio=parse_data(row['Data do Sorteio']),
                    ganhadores_sena=int(row['Ganhadores 6 acertos']) if not pd.isna(row['Ganhadores 6 acertos']) else 0,
                    rateio_sena=limpar_valor_monetario(row.get('Rateio 6 acertos', '')),
                    ganhadores_quina=int(row['Ganhadores 5 acertos']) if not pd.isna(row['Ganhadores 5 acertos']) else 0,
                    rateio_quina=limpar_valor_monetario(row.get('Rateio 5 acertos', '')),
                    ganhadores_quadra=int(row['Ganhadores 4 acertos']) if not pd.isna(row['Ganhadores 4 acertos']) else 0,
                    rateio_quadra=limpar_valor_monetario(row.get('Rateio 4 acertos', '')),
                    acumulado=limpar_valor_monetario(row.get('Acumulado 6 acertos', '')),
                    arrecadacao_total=limpar_valor_monetario(row.get('Arrecadação Total', '')),
                    estimativa_premio=limpar_valor_monetario(row.get('Estimativa prêmio', '')),
                    acumulado_mega_virada=limpar_valor_monetario(row.get('Acumulado Sorteio Especial Mega da Virada', '')),
                    observacao=str(row['Observação']) if not pd.isna(row['Observação']) else None
                )

                db.add(concurso)
                db.flush()  # Para obter o ID do concurso

                # Adiciona as dezenas sorteadas
                for pos in range(1, 7):
                    coluna = f'Bola{pos}'
                    if coluna in row and not pd.isna(row[coluna]):
                        dezena = DezenaSorteada(
                            concurso_id=concurso.id,
                            dezena=int(row[coluna]),
                            posicao=pos
                        )
                        db.add(dezena)

                # Adiciona cidades ganhadoras
                if 'Cidade / UF' in row:
                    cidades = parse_cidades(row['Cidade / UF'])
                    for cidade_data in cidades:
                        cidade = CidadeGanhadora(
                            concurso_id=concurso.id,
                            cidade=cidade_data['cidade'],
                            uf=cidade_data['uf']
                        )
                        db.add(cidade)

                # Commit a cada 100 registros para melhor performance
                if processados % 100 == 0:
                    db.commit()
                    yield {
                        'status': 'processando',
                        'total': total_registros,
                        'processados': processados,
                        'percentual': round((processados / total_registros) * 100, 2),
                        'message': f'Processados {processados} de {total_registros} registros'
                    }

                processados += 1

            except Exception as e:
                erros += 1
                print(f"Erro ao processar linha {index}: {str(e)}")
                db.rollback()
                continue

        # Commit final
        db.commit()

        yield {
            'status': 'concluido',
            'total': total_registros,
            'processados': processados,
            'erros': erros,
            'percentual': 100,
            'message': f'Importação concluída! {processados} registros importados, {erros} erros'
        }

    except Exception as e:
        db.rollback()
        yield {
            'status': 'erro',
            'message': f'Erro na importação: {str(e)}'
        }
