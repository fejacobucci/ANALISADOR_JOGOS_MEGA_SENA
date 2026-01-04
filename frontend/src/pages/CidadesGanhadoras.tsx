import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { analyticsApi } from '../services/api'
import { MapPin, Award, TrendingUp } from 'lucide-react'
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip, BarChart, Bar, XAxis, YAxis, CartesianGrid } from 'recharts'
import styles from './Analytics.module.css'

const COLORS = ['#209869', '#046635', '#4caf50', '#81c784', '#a5d6a7', '#c8e6c9', '#e8f5e9', '#f1f8e9']

const CidadesGanhadoras = () => {
  const [visao, setVisao] = useState<'cidades' | 'estados'>('cidades')
  const [cidadeSelecionada, setCidadeSelecionada] = useState<{cidade: string, uf: string} | null>(null)
  const [estadoSelecionado, setEstadoSelecionado] = useState<string | null>(null)

  const { data, isLoading } = useQuery({
    queryKey: ['cidades-ganhadoras'],
    queryFn: () => analyticsApi.getCidadesGanhadoras(20).then(res => res.data),
  })

  const { data: numerosCidade, isLoading: loadingNumerosCidade } = useQuery({
    queryKey: ['numeros-cidade', cidadeSelecionada?.cidade, cidadeSelecionada?.uf],
    queryFn: () => analyticsApi.getNumerosVencedoresCidade(
      cidadeSelecionada!.cidade,
      cidadeSelecionada!.uf,
      15
    ).then(res => res.data),
    enabled: !!cidadeSelecionada,
  })

  const { data: numerosEstado, isLoading: loadingNumerosEstado } = useQuery({
    queryKey: ['numeros-estado', estadoSelecionado],
    queryFn: () => analyticsApi.getNumerosVencedoresEstado(estadoSelecionado!, 15).then(res => res.data),
    enabled: !!estadoSelecionado,
  })

  if (isLoading) return <div className={styles.loading}>Carregando...</div>

  const chartDataEstados = data?.estados?.slice(0, 8).map((item: any) => ({
    name: item.uf,
    value: item.vitorias,
  }))

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Cidades e Estados Ganhadores</h1>

      <div className={styles.controls}>
        <label>
          <span>Visualização:</span>
          <select value={visao} onChange={(e) => setVisao(e.target.value as any)}>
            <option value="cidades">Por Cidade</option>
            <option value="estados">Por Estado</option>
          </select>
        </label>
      </div>

      {visao === 'cidades' ? (
        <div className={styles.grid}>
          <div className={styles.card}>
            <div className={styles.cardHeader}>
              <MapPin size={24} />
              <h2>Top 20 Cidades com Mais Vitórias</h2>
            </div>
            <p className={styles.subtitle}>
              Cidades que mais tiveram ganhadores da Mega Sena
            </p>
            <div className={styles.table}>
              <div className={styles.tableHeader} style={{ gridTemplateColumns: 'repeat(4, 1fr)' }}>
                <span>Posição</span>
                <span>Cidade</span>
                <span>UF</span>
                <span>Vitórias</span>
              </div>
              {data?.cidades?.map((item: any, index: number) => (
                <div
                  key={`${item.cidade}-${item.uf}`}
                  className={styles.tableRow}
                  style={{
                    gridTemplateColumns: 'repeat(4, 1fr)',
                    cursor: 'pointer',
                    background: cidadeSelecionada?.cidade === item.cidade && cidadeSelecionada?.uf === item.uf
                      ? '#f0f9f4'
                      : undefined
                  }}
                  onClick={() => setCidadeSelecionada({ cidade: item.cidade, uf: item.uf })}
                >
                  <span style={{ fontWeight: 600 }}>{index + 1}º</span>
                  <span className={styles.number}>{item.cidade}</span>
                  <span>{item.uf}</span>
                  <span>
                    <Award size={16} style={{ verticalAlign: 'middle', marginRight: '0.25rem' }} />
                    {item.vitorias}x ({item.percentual}%)
                  </span>
                </div>
              ))}
            </div>
          </div>

          {cidadeSelecionada && (
            <div className={styles.card}>
              <div className={styles.cardHeader}>
                <TrendingUp size={24} />
                <h2>Números Vencedores - {cidadeSelecionada.cidade}/{cidadeSelecionada.uf}</h2>
              </div>
              <p className={styles.subtitle}>
                Números que mais saíram em jogos vencedores desta cidade
              </p>
              {loadingNumerosCidade ? (
                <div className={styles.loading}>Carregando...</div>
              ) : numerosCidade && numerosCidade.length > 0 ? (
                <>
                  <div className={styles.info}>
                    <p>
                      Total de vitórias da cidade: <strong>{numerosCidade[0]?.total_concursos_cidade || 0}</strong>
                    </p>
                  </div>
                  <div className={styles.numberGrid}>
                    {numerosCidade?.map((item: any) => (
                      <div key={item.dezena} className={styles.hotNumber}>
                        <span className={styles.bigNumber}>{item.dezena}</span>
                        <span className={styles.freq}>{item.frequencia}x</span>
                        <span style={{ fontSize: '0.75rem' }}>{item.percentual}%</span>
                      </div>
                    ))}
                  </div>
                </>
              ) : (
                <p>Nenhum dado disponível para esta cidade.</p>
              )}
            </div>
          )}
        </div>
      ) : (
        <div className={styles.grid}>
          <div className={styles.card}>
            <div className={styles.cardHeader}>
              <MapPin size={24} />
              <h2>Estados com Mais Vitórias</h2>
            </div>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={data?.estados}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="uf" />
                <YAxis />
                <Tooltip />
                <Bar dataKey="vitorias" fill="#209869" />
              </BarChart>
            </ResponsiveContainer>
          </div>

          <div className={styles.card}>
            <h2>Distribuição por Estado (Top 8)</h2>
            <ResponsiveContainer width="100%" height={400}>
              <PieChart>
                <Pie
                  data={chartDataEstados}
                  cx="50%"
                  cy="50%"
                  labelLine={false}
                  label={({ name, value }) => `${name}: ${value}`}
                  outerRadius={120}
                  fill="#8884d8"
                  dataKey="value"
                >
                  {chartDataEstados?.map((entry: any, index: number) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip />
                <Legend />
              </PieChart>
            </ResponsiveContainer>
          </div>

          <div className={styles.card}>
            <div className={styles.cardHeader}>
              <TrendingUp size={24} />
              <h2>Selecione um Estado</h2>
            </div>
            <div className={styles.controls}>
              <label>
                <span>Estado:</span>
                <select
                  value={estadoSelecionado || ''}
                  onChange={(e) => setEstadoSelecionado(e.target.value || null)}
                >
                  <option value="">Selecione...</option>
                  {data?.estados?.map((item: any) => (
                    <option key={item.uf} value={item.uf}>
                      {item.uf} ({item.vitorias} vitórias)
                    </option>
                  ))}
                </select>
              </label>
            </div>

            {estadoSelecionado && (
              <>
                {loadingNumerosEstado ? (
                  <div className={styles.loading}>Carregando...</div>
                ) : numerosEstado && numerosEstado.length > 0 ? (
                  <>
                    <p className={styles.subtitle}>
                      Números que mais saíram em vitórias do estado {estadoSelecionado}
                    </p>
                    <div className={styles.info}>
                      <p>
                        Total de vitórias do estado: <strong>{numerosEstado[0]?.total_concursos_estado || 0}</strong>
                      </p>
                    </div>
                    <div className={styles.numberGrid}>
                      {numerosEstado?.map((item: any) => (
                        <div key={item.dezena} className={styles.hotNumber}>
                          <span className={styles.bigNumber}>{item.dezena}</span>
                          <span className={styles.freq}>{item.frequencia}x</span>
                          <span style={{ fontSize: '0.75rem' }}>{item.percentual}%</span>
                        </div>
                      ))}
                    </div>
                  </>
                ) : (
                  <p>Nenhum dado disponível para este estado.</p>
                )}
              </>
            )}
          </div>
        </div>
      )}

      <div className={styles.card} style={{ marginTop: '2rem', background: '#f0f9f4' }}>
        <h3 style={{ fontSize: '1.125rem', marginBottom: '1rem', color: '#046635' }}>
          Como usar esta informação?
        </h3>
        <ul style={{ listStyle: 'none', padding: 0, lineHeight: '1.8' }}>
          <li style={{ marginBottom: '0.5rem' }}>
            ✓ <strong>Números da sorte local:</strong> Veja quais números mais saíram em vitórias da sua cidade/estado
          </li>
          <li style={{ marginBottom: '0.5rem' }}>
            ✓ <strong>Gerador baseado em cidades:</strong> Use estes números no gerador de jogos com o método "Cidade Vencedora"
          </li>
          <li style={{ marginBottom: '0.5rem' }}>
            ✓ <strong>Padrões regionais:</strong> Identifique se existem padrões específicos por região
          </li>
          <li>
            ✓ <strong>Clique em uma cidade:</strong> Para ver os números que mais saíram em suas vitórias
          </li>
        </ul>
      </div>
    </div>
  )
}

export default CidadesGanhadoras
