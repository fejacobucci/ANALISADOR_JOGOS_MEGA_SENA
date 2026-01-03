import { useQuery } from '@tanstack/react-query'
import { analyticsApi } from '../services/api'
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts'
import styles from './Analytics.module.css'

const ParesImpares = () => {
  const { data, isLoading } = useQuery({
    queryKey: ['pares-impares'],
    queryFn: () => analyticsApi.getAnaliseParesImpares().then(res => res.data),
  })

  const chartData = Object.entries(data?.distribuicao || {}).map(([key, value]: [string, any]) => ({
    name: key,
    value: value.quantidade,
    percentual: value.percentual,
  }))

  const COLORS = ['#209869', '#046635', '#4caf50', '#81c784', '#a5d6a7', '#c8e6c9']

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Análise de Pares e Ímpares</h1>

      {isLoading ? (
        <div className={styles.loading}>Carregando...</div>
      ) : (
        <>
          <div className={styles.card}>
            <h2>Distribuição Mais Comum</h2>
            <div className={styles.highlight}>
              <span>Padrão mais frequente:</span>
              <strong>{data?.mais_comum}</strong>
            </div>
          </div>

          <div className={styles.card}>
            <h2>Distribuição de Combinações</h2>
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

          <div className={styles.card}>
            <h2>Tabela de Distribuições</h2>
            <div className={styles.table}>
              <div className={styles.tableHeader}>
                <span>Combinação</span>
                <span>Quantidade</span>
                <span>Percentual</span>
              </div>
              {Object.entries(data?.distribuicao || {}).map(([key, value]: [string, any]) => (
                <div key={key} className={styles.tableRow}>
                  <span>{key}</span>
                  <span>{value.quantidade}</span>
                  <span>{value.percentual}%</span>
                </div>
              ))}
            </div>
          </div>
        </>
      )}
    </div>
  )
}

export default ParesImpares
