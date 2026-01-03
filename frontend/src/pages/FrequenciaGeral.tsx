import { useQuery } from '@tanstack/react-query'
import { analyticsApi } from '../services/api'
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts'
import styles from './Analytics.module.css'

const FrequenciaGeral = () => {
  const { data, isLoading } = useQuery({
    queryKey: ['frequencia-geral'],
    queryFn: () => analyticsApi.getFrequenciaGeral().then(res => res.data),
  })

  if (isLoading) return <div className={styles.loading}>Carregando...</div>

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Frequência Geral das Dezenas</h1>

      <div className={styles.card}>
        <h2>Gráfico de Frequência</h2>
        <ResponsiveContainer width="100%" height={400}>
          <BarChart data={data?.slice(0, 20)}>
            <CartesianGrid strokeDasharray="3 3" />
            <XAxis dataKey="dezena" />
            <YAxis />
            <Tooltip />
            <Bar dataKey="frequencia" fill="#209869" />
          </BarChart>
        </ResponsiveContainer>
      </div>

      <div className={styles.card}>
        <h2>Top 20 Números Mais Frequentes</h2>
        <div className={styles.table}>
          <div className={styles.tableHeader}>
            <span>Dezena</span>
            <span>Frequência</span>
            <span>Percentual</span>
          </div>
          {data?.slice(0, 20).map((item: any) => (
            <div key={item.dezena} className={styles.tableRow}>
              <span className={styles.number}>{item.dezena}</span>
              <span>{item.frequencia}</span>
              <span>{item.percentual}%</span>
            </div>
          ))}
        </div>
      </div>
    </div>
  )
}

export default FrequenciaGeral
