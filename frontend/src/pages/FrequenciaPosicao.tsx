import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { analyticsApi } from '../services/api'
import { Clock, TrendingUp } from 'lucide-react'
import styles from './Analytics.module.css'

const FrequenciaPosicao = () => {
  const [posicao, setPosicao] = useState(1)
  const [visao, setVisao] = useState<'frequencia' | 'intervalo'>('frequencia')

  const { data: dataFrequencia, isLoading: loadingFrequencia } = useQuery({
    queryKey: ['frequencia-posicao', posicao],
    queryFn: () => analyticsApi.getFrequenciaPosicao(posicao).then(res => res.data),
  })

  const { data: dataIntervalo, isLoading: loadingIntervalo } = useQuery({
    queryKey: ['intervalo-repeticoes-posicao', posicao],
    queryFn: () => analyticsApi.getIntervaloRepeticoesPosicao(posicao, 15).then(res => res.data),
    enabled: visao === 'intervalo',
  })

  const dadosPosicao = dataFrequencia?.filter((item: any) => item.posicao === posicao).slice(0, 15)
  const isLoading = visao === 'frequencia' ? loadingFrequencia : loadingIntervalo

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Frequência por Posição</h1>

      <div className={styles.controls}>
        <label>
          <span>Selecione a Posição:</span>
          <select value={posicao} onChange={(e) => setPosicao(Number(e.target.value))}>
            {[1, 2, 3, 4, 5, 6].map(p => (
              <option key={p} value={p}>Posição {p}</option>
            ))}
          </select>
        </label>

        <label>
          <span>Visualização:</span>
          <select value={visao} onChange={(e) => setVisao(e.target.value as any)}>
            <option value="frequencia">Frequência de Aparições</option>
            <option value="intervalo">Intervalo entre Repetições</option>
          </select>
        </label>
      </div>

      {isLoading ? (
        <div className={styles.loading}>Carregando...</div>
      ) : visao === 'frequencia' ? (
        <div className={styles.card}>
          <div className={styles.cardHeader}>
            <TrendingUp size={24} />
            <h2>Top 15 Números Mais Frequentes na Posição {posicao}</h2>
          </div>
          <p className={styles.subtitle}>
            Números que mais aparecem na {posicao}ª posição do sorteio
          </p>
          <div className={styles.table}>
            <div className={styles.tableHeader}>
              <span>Posição</span>
              <span>Dezena</span>
              <span>Frequência</span>
            </div>
            {dadosPosicao?.map((item: any) => (
              <div key={`${item.posicao}-${item.dezena}`} className={styles.tableRow}>
                <span>{item.posicao}ª</span>
                <span className={styles.number}>{item.dezena}</span>
                <span>{item.frequencia}x</span>
              </div>
            ))}
          </div>
        </div>
      ) : (
        <div className={styles.card}>
          <div className={styles.cardHeader}>
            <Clock size={24} />
            <h2>Intervalo entre Repetições na Posição {posicao}</h2>
          </div>
          <p className={styles.subtitle}>
            Análise do tempo (em dias) entre as aparições de cada número na {posicao}ª posição
          </p>
          <div className={styles.info}>
            <p>
              <strong>Intervalo Médio:</strong> Média de dias entre as repetições do número.
            </p>
            <p>
              <strong>Intervalo Mínimo/Máximo:</strong> Menor e maior tempo entre repetições.
            </p>
          </div>
          <div className={styles.table}>
            <div className={styles.tableHeader} style={{ gridTemplateColumns: 'repeat(6, 1fr)' }}>
              <span>Dezena</span>
              <span>Frequência</span>
              <span>Int. Médio (dias)</span>
              <span>Int. Mínimo</span>
              <span>Int. Máximo</span>
              <span>Último Sorteio</span>
            </div>
            {dataIntervalo?.map((item: any) => (
              <div key={item.dezena} className={styles.tableRow} style={{ gridTemplateColumns: 'repeat(6, 1fr)' }}>
                <span className={styles.number}>{item.dezena}</span>
                <span>{item.frequencia}x</span>
                <span style={{ fontWeight: 600, color: '#209869' }}>{item.intervalo_medio} dias</span>
                <span>{item.intervalo_minimo} dias</span>
                <span>{item.intervalo_maximo} dias</span>
                <span style={{ fontSize: '0.875rem' }}>
                  {new Date(item.ultimo_sorteio).toLocaleDateString('pt-BR')}
                </span>
              </div>
            ))}
          </div>

          <div className={styles.card} style={{ marginTop: '2rem', background: '#f0f9f4' }}>
            <h3 style={{ fontSize: '1.125rem', marginBottom: '1rem', color: '#046635' }}>
              Como interpretar os intervalos?
            </h3>
            <ul style={{ listStyle: 'none', padding: 0, lineHeight: '1.8' }}>
              <li style={{ marginBottom: '0.5rem' }}>
                ✓ <strong>Intervalo médio baixo:</strong> O número tende a se repetir com mais frequência
              </li>
              <li style={{ marginBottom: '0.5rem' }}>
                ✓ <strong>Intervalo médio alto:</strong> O número demora mais para se repetir
              </li>
              <li style={{ marginBottom: '0.5rem' }}>
                ✓ <strong>Intervalo mínimo de 2 dias:</strong> Indica que o número já saiu em concursos consecutivos
              </li>
              <li>
                ✓ <strong>Último sorteio recente:</strong> Número apareceu recentemente nesta posição
              </li>
            </ul>
          </div>
        </div>
      )}
    </div>
  )
}

export default FrequenciaPosicao
