import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { analyticsApi } from '../services/api'
import { TrendingUp, TrendingDown } from 'lucide-react'
import styles from './Analytics.module.css'

const NumerosQuentesFrios = () => {
  const [ultimos, setUltimos] = useState(100)

  const { data, isLoading } = useQuery({
    queryKey: ['quentes-frios', ultimos],
    queryFn: () => analyticsApi.getNumerosQuentesFrios(10, ultimos).then(res => res.data),
  })

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Números Quentes e Frios</h1>

      <div className={styles.controls}>
        <label>
          <span>Considerar últimos:</span>
          <select value={ultimos} onChange={(e) => setUltimos(Number(e.target.value))}>
            <option value={50}>50 concursos</option>
            <option value={100}>100 concursos</option>
            <option value={200}>200 concursos</option>
            <option value={500}>500 concursos</option>
          </select>
        </label>
      </div>

      {isLoading ? (
        <div className={styles.loading}>Carregando...</div>
      ) : (
        <div className={styles.grid}>
          <div className={styles.card}>
            <div className={styles.cardHeader}>
              <TrendingUp size={24} color="#ff6b6b" />
              <h2>Números Quentes</h2>
            </div>
            <p className={styles.subtitle}>Mais frequentes nos últimos {ultimos} concursos</p>
            <div className={styles.numberGrid}>
              {data?.quentes?.map((item: any) => (
                <div key={item.dezena} className={styles.hotNumber}>
                  <span className={styles.bigNumber}>{item.dezena}</span>
                  <span className={styles.freq}>{item.frequencia}x</span>
                </div>
              ))}
            </div>
          </div>

          <div className={styles.card}>
            <div className={styles.cardHeader}>
              <TrendingDown size={24} color="#4dabf7" />
              <h2>Números Frios</h2>
            </div>
            <p className={styles.subtitle}>Menos frequentes nos últimos {ultimos} concursos</p>
            <div className={styles.numberGrid}>
              {data?.frios?.map((item: any) => (
                <div key={item.dezena} className={styles.coldNumber}>
                  <span className={styles.bigNumber}>{item.dezena}</span>
                  <span className={styles.freq}>{item.frequencia}x</span>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default NumerosQuentesFrios
