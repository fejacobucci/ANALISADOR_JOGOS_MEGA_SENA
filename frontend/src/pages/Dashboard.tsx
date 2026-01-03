import { useQuery } from '@tanstack/react-query'
import { analyticsApi } from '../services/api'
import { TrendingUp, Trophy, Calendar, BarChart } from 'lucide-react'
import styles from './Dashboard.module.css'

const Dashboard = () => {
  const { data: stats, isLoading } = useQuery({
    queryKey: ['estatisticas-gerais'],
    queryFn: () => analyticsApi.getEstatisticasGerais().then(res => res.data),
  })

  if (isLoading) {
    return <div className={styles.loading}>Carregando...</div>
  }

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Dashboard - Mega Sena</h1>

      <div className={styles.grid}>
        <div className={styles.card}>
          <div className={styles.cardIcon} style={{ background: '#4caf50' }}>
            <BarChart size={32} />
          </div>
          <div className={styles.cardContent}>
            <p className={styles.cardLabel}>Total de Concursos</p>
            <p className={styles.cardValue}>{stats?.total_concursos || 0}</p>
          </div>
        </div>

        <div className={styles.card}>
          <div className={styles.cardIcon} style={{ background: '#2196f3' }}>
            <Trophy size={32} />
          </div>
          <div className={styles.cardContent}>
            <p className={styles.cardLabel}>Total de Ganhadores</p>
            <p className={styles.cardValue}>{stats?.total_ganhadores_sena || 0}</p>
          </div>
        </div>

        <div className={styles.card}>
          <div className={styles.cardIcon} style={{ background: '#ff9800' }}>
            <TrendingUp size={32} />
          </div>
          <div className={styles.cardContent}>
            <p className={styles.cardLabel}>Concursos Acumulados</p>
            <p className={styles.cardValue}>{stats?.concursos_acumulados || 0}</p>
            <p className={styles.cardSubtext}>
              {stats?.percentual_acumulados.toFixed(1)}% do total
            </p>
          </div>
        </div>

        <div className={styles.card}>
          <div className={styles.cardIcon} style={{ background: '#9c27b0' }}>
            <Calendar size={32} />
          </div>
          <div className={styles.cardContent}>
            <p className={styles.cardLabel}>Último Concurso</p>
            <p className={styles.cardValue}>{stats?.ultimo_concurso?.numero || '-'}</p>
            <p className={styles.cardSubtext}>
              {stats?.ultimo_concurso?.data ?
                new Date(stats.ultimo_concurso.data).toLocaleDateString('pt-BR') : '-'}
            </p>
          </div>
        </div>
      </div>

      <div className={styles.info}>
        <h2>Bem-vindo ao Sistema de Análise da Mega Sena</h2>
        <p>
          Este sistema oferece análises estatísticas completas dos resultados históricos da Mega Sena
          e ferramentas para geração inteligente de jogos.
        </p>
        <div className={styles.features}>
          <div className={styles.feature}>
            <h3>Análises Disponíveis</h3>
            <ul>
              <li>Frequência geral e por período</li>
              <li>Números quentes e frios</li>
              <li>Análise de pares e ímpares</li>
              <li>Distribuição por quadrantes</li>
              <li>Soma das dezenas</li>
              <li>Frequência por posição</li>
            </ul>
          </div>
          <div className={styles.feature}>
            <h3>Geradores de Jogos</h3>
            <ul>
              <li>Por frequência (quentes/frios)</li>
              <li>Balanceado (pares/ímpares)</li>
              <li>Por quadrantes</li>
              <li>Por soma das dezenas</li>
              <li>Trend (tendências recentes)</li>
              <li>Misto (múltiplos critérios)</li>
              <li>Desdobramento garantido</li>
            </ul>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Dashboard
