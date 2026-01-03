import axios from 'axios'

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api/v1'

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Analytics
export const analyticsApi = {
  getEstatisticasGerais: () => api.get('/analytics/estatisticas-gerais'),
  getFrequenciaGeral: () => api.get('/analytics/frequencia-geral'),
  getFrequenciaAnos: (anos: number) => api.get(`/analytics/frequencia-anos/${anos}`),
  getFrequenciaPosicao: (posicao?: number) =>
    api.get('/analytics/frequencia-posicao', { params: { posicao } }),
  getIntervaloRepeticoesPosicao: (posicao: number = 1, limite: number = 20) =>
    api.get('/analytics/intervalo-repeticoes-posicao', { params: { posicao, limite } }),
  getNumerosQuentesFrios: (limite: number = 10, ultimos_concursos: number = 100) =>
    api.get('/analytics/numeros-quentes-frios', { params: { limite, ultimos_concursos } }),
  getNumerosAtrasados: (limite: number = 10) =>
    api.get('/analytics/numeros-atrasados', { params: { limite } }),
  getAnaliseParesImpares: () => api.get('/analytics/pares-impares'),
  getAnaliseQuadrantes: () => api.get('/analytics/quadrantes'),
  getAnaliseSoma: () => api.get('/analytics/soma-dezenas'),
  verificarCombinacao: (dezenas: number[]) =>
    api.post('/analytics/verificar-combinacao', { dezenas }),
}

// Generator
export const generatorApi = {
  gerarJogos: (metodo: string, quantidade: number, parametros: any) =>
    api.post('/generator/gerar', { metodo, quantidade, parametros }),
  gerarDesdobramento: (dezenas: number[], garantia: string) =>
    api.post('/generator/desdobramento', { dezenas, garantia }),
}

// Import
export const importApi = {
  importarPorCaminho: (file_path: string) =>
    api.post('/import/file-path', { file_path }),
}

export default api
