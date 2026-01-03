import { useQuery } from '@tanstack/react-query'
import { analyticsApi } from '../services/api'
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'
import styles from './Analytics.module.css'

const Quadrantes = () => {
  const { data, isLoading } = useQuery({
    queryKey: ['quadrantes'],
    queryFn: () => analyticsApi.getAnaliseQuadrantes().then(res => res.data),
  })

  const chartData = Object.entries(data || {}).map(([key, value]: [string, any]) => ({
    name: `${key} (${value.range})`,
    value: value.frequencia,
    percentual: value.percentual,
  }))

  const COLORS = ['#209869', '#046635', '#4caf50', '#81c784']

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Análise por Quadrantes</h1>

      {isLoading ? (
        <div className={styles.loading}>Carregando...</div>
      ) : (
        <>
          <div className={styles.grid}>
            {Object.entries(data || {}).map(([key, value]: [string, any]) => (
              <div key={key} className={styles.card}>
                <h2>{key}</h2>
                <div className={styles.range}>Dezenas {value.range}</div>
                <div className={styles.stat}>
                  <span className={styles.bigNumber}>{value.frequencia}</span>
                  <span className={styles.label}>sorteios</span>
                </div>
                <div className={styles.percentage}>{value.percentual}%</div>
              </div>
            ))}
          </div>

          <div className={styles.card}>
            <h2>Distribuição por Quadrante</h2>
            <ResponsiveContainer width="100%" height={400}>
              <PieChart>
                <Pie
                  data={chartData}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, percentual }) => `${name}: ${percentual}%`}
                  outerRadius={120}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {chartData.map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>
        </>
      )}
    </div>
  )
}

export default Quadrantes
