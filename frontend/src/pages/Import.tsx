import { useState } from 'react'
import { Upload, CheckCircle, AlertCircle } from 'lucide-react'
import styles from './Import.module.css'

const Import = () => {
  const [importing, setImporting] = useState(false)
  const [progress, setProgress] = useState(0)
  const [status, setStatus] = useState<'idle' | 'importing' | 'success' | 'error'>('idle')
  const [message, setMessage] = useState('')
  const [stats, setStats] = useState<any>(null)

  const handleImport = async () => {
    setImporting(true)
    setStatus('importing')
    setProgress(0)
    setMessage('Iniciando importação...')

    try {
      const filePath = '/Volumes/Micro64Gb/PROJETOS/MEGA_SENA/resultados_MegaSena.xlsx'
      const response = await fetch(
        `http://localhost:8000/api/v1/import/file-path?file_path=${encodeURIComponent(filePath)}`,
        {
          method: 'POST',
        }
      )

      if (!response.ok) {
        throw new Error('Erro ao iniciar importação')
      }

      const reader = response.body?.getReader()
      if (!reader) throw new Error('Stream não disponível')

      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { done, value } = await reader.read()
        if (done) break

        buffer += decoder.decode(value, { stream: true })
        const lines = buffer.split('\n')
        buffer = lines.pop() || ''

        for (const line of lines) {
          if (line.startsWith('data: ')) {
            const data = JSON.parse(line.slice(6))

            if (data.percentual) {
              setProgress(data.percentual)
            }

            setMessage(data.message || '')

            if (data.status === 'concluido') {
              setStatus('success')
              setStats(data)
            } else if (data.status === 'erro') {
              setStatus('error')
            }
          }
        }
      }
    } catch (error: any) {
      setStatus('error')
      setMessage(`Erro: ${error.message}`)
    } finally {
      setImporting(false)
    }
  }

  return (
    <div className={styles.container}>
      <h1 className={styles.title}>Importar Dados da Mega Sena</h1>

      <div className={styles.card}>
        <div className={styles.cardHeader}>
          <Upload size={32} />
          <div>
            <h2>Importação de Arquivo Excel</h2>
            <p>Importa os resultados históricos da Mega Sena para o banco de dados</p>
          </div>
        </div>

        {status === 'idle' && (
          <div className={styles.info}>
            <p>
              <strong>Arquivo:</strong> resultados_MegaSena.xlsx
            </p>
            <p>
              Clique no botão abaixo para iniciar a importação dos dados.
              Este processo pode levar alguns minutos dependendo da quantidade de registros.
            </p>
          </div>
        )}

        {importing && (
          <div className={styles.progressSection}>
            <div className={styles.progressBar}>
              <div
                className={styles.progressFill}
                style={{ width: `${progress}%` }}
              />
            </div>
            <p className={styles.progressText}>{progress.toFixed(1)}%</p>
            <p className={styles.statusMessage}>{message}</p>
          </div>
        )}

        {status === 'success' && (
          <div className={styles.success}>
            <CheckCircle size={48} />
            <h3>Importação Concluída!</h3>
            <p>{message}</p>
            {stats && (
              <div className={styles.stats}>
                <div className={styles.statItem}>
                  <span>Total:</span>
                  <strong>{stats.total}</strong>
                </div>
                <div className={styles.statItem}>
                  <span>Processados:</span>
                  <strong>{stats.processados}</strong>
                </div>
                {stats.erros > 0 && (
                  <div className={styles.statItem}>
                    <span>Erros:</span>
                    <strong className={styles.errorCount}>{stats.erros}</strong>
                  </div>
                )}
              </div>
            )}
          </div>
        )}

        {status === 'error' && (
          <div className={styles.error}>
            <AlertCircle size={48} />
            <h3>Erro na Importação</h3>
            <p>{message}</p>
          </div>
        )}

        <div className={styles.actions}>
          <button
            className={styles.button}
            onClick={handleImport}
            disabled={importing}
          >
            {importing ? 'Importando...' : status === 'success' ? 'Reimportar' : 'Iniciar Importação'}
          </button>
        </div>
      </div>
    </div>
  )
}

export default Import
