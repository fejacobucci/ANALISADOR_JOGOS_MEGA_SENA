import { useQuery } from '@tanstack/react-query'
import { analyticsApi } from '../services/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import styles from './Analytics.module.css'

const SomaDezenas = () => {
  const { data, isLoading } = useQuery({
    queryKey: ['soma-dezenas'],
    queryFn: () => analyticsApi.getAnaliseSoma().then(res => res.data),
  })

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Análise da Soma das Dezenas</h1>

      {isLoading ? (
        <div className={styles.loading}>Carregando...</div>
      ) : (
        <>
          <div className={styles.grid}>
            <div className={styles.card}>
              <h2>Soma Mínima</h2>
              <div className={styles.stat}>
                <span className={styles.bigNumber}>{data?.minima}</span>
              </div>
            </div>
            <div className={styles.card}>
              <h2>Soma Média</h2>
              <div className={styles.stat}>
                <span className={styles.bigNumber}>{data?.media}</span>
              </div>
            </div>
            <div className={styles.card}>
              <h2>Soma Mediana</h2>
              <div className={styles.stat}>
                <span className={styles.bigNumber}>{data?.mediana}</span>
              </div>
            </div>
            <div className={styles.card}>
              <h2>Soma Máxima</h2>
              <div className={styles.stat}>
                <span className={styles.bigNumber}>{data?.maxima}</span>
              </div>
            </div>
          </div>

          <div className={styles.card}>
            <h2>Distribuição das Somas</h2>
            <p className={styles.info}>
              A maioria dos sorteios tem soma entre 150 e 220. Use este intervalo para
              gerar jogos mais equilibrados.
            </p>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={data?.distribuicao}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="range" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="quantidade" fill="#209869" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </>
      )}
    </div>
  )
}

export default SomaDezenas
