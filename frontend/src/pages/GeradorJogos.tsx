import { useState } from 'react'
import { useMutation } from '@tanstack/react-query'
import { generatorApi } from '../services/api'
import { Dices, Sparkles, Settings } from 'lucide-react'
import styles from './GeradorJogos.module.css'

type Metodo = 'frequencia' | 'par_impar' | 'quadrantes' | 'soma' | 'trend' | 'posicao' | 'misto'

const GeradorJogos = () => {
  const [metodo, setMetodo] = useState<Metodo>('misto')
  const [quantidade, setQuantidade] = useState(5)
  const [parametros, setParametros] = useState<any>({})

  const mutation = useMutation({
    mutationFn: () => generatorApi.gerarJogos(metodo, quantidade, parametros),
  })

  const handleGerar = () => {
    mutation.mutate()
  }

  const renderParametros = () => {
    switch (metodo) {
      case 'frequencia':
        return (
          <div className={styles.params}>
            <label>
              <span>Tipo:</span>
              <select
                value={parametros.usar_quentes !== false ? 'quentes' : 'frios'}
                onChange={(e) =>
                  setParametros({ ...parametros, usar_quentes: e.target.value === 'quentes' })
                }
              >
                <option value="quentes">Números Quentes (mais frequentes)</option>
                <option value="frios">Números Frios (menos frequentes)</option>
              </select>
            </label>
            <label>
              <span>Top N números:</span>
              <input
                type="number"
                min="10"
                max="40"
                value={parametros.top_n || 20}
                onChange={(e) =>
                  setParametros({ ...parametros, top_n: parseInt(e.target.value) })
                }
              />
            </label>
          </div>
        )

      case 'par_impar':
        return (
          <div className={styles.params}>
            <label>
              <span>Números Pares:</span>
              <input
                type="number"
                min="0"
                max="6"
                value={parametros.pares || 3}
                onChange={(e) =>
                  setParametros({ ...parametros, pares: parseInt(e.target.value), impares: 6 - parseInt(e.target.value) })
                }
              />
            </label>
            <label>
              <span>Números Ímpares:</span>
              <input
                type="number"
                min="0"
                max="6"
                value={parametros.impares || 3}
                disabled
              />
            </label>
          </div>
        )

      case 'soma':
        return (
          <div className={styles.params}>
            <label>
              <span>Soma Mínima:</span>
              <input
                type="number"
                min="21"
                max="300"
                value={parametros.soma_min || 150}
                onChange={(e) =>
                  setParametros({ ...parametros, soma_min: parseInt(e.target.value) })
                }
              />
            </label>
            <label>
              <span>Soma Máxima:</span>
              <input
                type="number"
                min="21"
                max="300"
                value={parametros.soma_max || 220}
                onChange={(e) =>
                  setParametros({ ...parametros, soma_max: parseInt(e.target.value) })
                }
              />
            </label>
          </div>
        )

      case 'trend':
        return (
          <div className={styles.params}>
            <label>
              <span>Últimos Concursos:</span>
              <input
                type="number"
                min="10"
                max="200"
                value={parametros.ultimos_concursos || 50}
                onChange={(e) =>
                  setParametros({ ...parametros, ultimos_concursos: parseInt(e.target.value) })
                }
              />
            </label>
            <label>
              <span>Top N números:</span>
              <input
                type="number"
                min="6"
                max="30"
                value={parametros.top_n || 15}
                onChange={(e) =>
                  setParametros({ ...parametros, top_n: parseInt(e.target.value) })
                }
              />
            </label>
          </div>
        )

      case 'misto':
        return (
          <div className={styles.params}>
            <label className={styles.checkbox}>
              <input
                type="checkbox"
                checked={parametros.usar_frequencia !== false}
                onChange={(e) =>
                  setParametros({ ...parametros, usar_frequencia: e.target.checked })
                }
              />
              <span>Usar análise de frequência</span>
            </label>
            <label className={styles.checkbox}>
              <input
                type="checkbox"
                checked={parametros.usar_quadrantes !== false}
                onChange={(e) =>
                  setParametros({ ...parametros, usar_quadrantes: e.target.checked })
                }
              />
              <span>Usar distribuição por quadrantes</span>
            </label>
            <label className={styles.checkbox}>
              <input
                type="checkbox"
                checked={parametros.usar_soma !== false}
                onChange={(e) =>
                  setParametros({ ...parametros, usar_soma: e.target.checked })
                }
              />
              <span>Respeitar intervalo de soma (150-220)</span>
            </label>
            <label>
              <span>Números Pares:</span>
              <input
                type="number"
                min="0"
                max="6"
                value={parametros.pares || 3}
                onChange={(e) =>
                  setParametros({ ...parametros, pares: parseInt(e.target.value) })
                }
              />
            </label>
          </div>
        )

      default:
        return null
    }
  }

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Gerador Inteligente de Jogos</h1>

      <div className={styles.layout}>
        <div className={styles.sidebar}>
          <div className={styles.card}>
            <div className={styles.cardHeader}>
              <Settings size={24} />
              <h2>Configurações</h2>
            </div>

            <div className={styles.form}>
              <label>
                <span>Método de Geração:</span>
                <select
                  value={metodo}
                  onChange={(e) => {
                    setMetodo(e.target.value as Metodo)
                    setParametros({})
                  }}
                  className={styles.select}
                >
                  <option value="misto">Misto (Recomendado)</option>
                  <option value="frequencia">Por Frequência</option>
                  <option value="trend">Trend (Tendências Recentes)</option>
                  <option value="par_impar">Balanceado Pares/Ímpares</option>
                  <option value="quadrantes">Por Quadrantes</option>
                  <option value="soma">Por Soma das Dezenas</option>
                  <option value="posicao">Por Posição</option>
                </select>
              </label>

              <label>
                <span>Quantidade de Jogos:</span>
                <input
                  type="number"
                  min="1"
                  max="50"
                  value={quantidade}
                  onChange={(e) => setQuantidade(parseInt(e.target.value))}
                  className={styles.input}
                />
              </label>

              {renderParametros()}

              <button
                onClick={handleGerar}
                disabled={mutation.isPending}
                className={styles.button}
              >
                <Sparkles size={20} />
                {mutation.isPending ? 'Gerando...' : 'Gerar Jogos'}
              </button>
            </div>
          </div>

          <div className={styles.info}>
            <h3>Sobre o Método Selecionado</h3>
            {metodo === 'misto' && (
              <p>
                Combina múltiplos critérios estatísticos para gerar jogos equilibrados,
                considerando frequência, distribuição e padrões históricos.
              </p>
            )}
            {metodo === 'frequencia' && (
              <p>
                Gera jogos baseados nos números mais ou menos frequentes no histórico completo.
              </p>
            )}
            {metodo === 'trend' && (
              <p>
                Foca nos números com maior tendência de saída nos concursos mais recentes.
              </p>
            )}
            {metodo === 'par_impar' && (
              <p>
                Gera jogos respeitando a proporção de números pares e ímpares desejada.
              </p>
            )}
            {metodo === 'quadrantes' && (
              <p>
                Distribui os números pelos 4 quadrantes do volante (1-15, 16-30, 31-45, 46-60).
              </p>
            )}
            {metodo === 'soma' && (
              <p>
                Gera jogos cuja soma das dezenas fica dentro de um intervalo estatisticamente favorável.
              </p>
            )}
            {metodo === 'posicao' && (
              <p>
                Usa os números mais frequentes em cada uma das 6 posições do sorteio.
              </p>
            )}
          </div>
        </div>

        <div className={styles.main}>
          {mutation.isPending && (
            <div className={styles.loading}>
              <Dices size={48} className={styles.spinner} />
              <p>Gerando jogos...</p>
            </div>
          )}

          {mutation.isError && (
            <div className={styles.error}>
              <p>Erro ao gerar jogos. Tente novamente.</p>
            </div>
          )}

          {mutation.isSuccess && mutation.data && (
            <div className={styles.results}>
              <div className={styles.resultsHeader}>
                <h2>Jogos Gerados</h2>
                <p>
                  {mutation.data.data.quantidade_gerada} jogo(s) usando o método{' '}
                  <strong>{mutation.data.data.metodo}</strong>
                </p>
              </div>

              <div className={styles.games}>
                {mutation.data.data.jogos.map((jogo: number[], index: number) => (
                  <div key={index} className={styles.game}>
                    <span className={styles.gameNumber}>#{index + 1}</span>
                    <div className={styles.balls}>
                      {jogo.map((numero) => (
                        <div key={numero} className={styles.ball}>
                          {numero.toString().padStart(2, '0')}
                        </div>
                      ))}
                    </div>
                    <div className={styles.gameInfo}>
                      <span>Soma: {jogo.reduce((a, b) => a + b, 0)}</span>
                      <span>
                        Pares: {jogo.filter((n) => n % 2 === 0).length} | Ímpares:{' '}
                        {jogo.filter((n) => n % 2 === 1).length}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {!mutation.isPending && !mutation.isError && !mutation.isSuccess && (
            <div className={styles.placeholder}>
              <Dices size={64} />
              <p>Configure os parâmetros e clique em "Gerar Jogos"</p>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}

export default GeradorJogos
