import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom'
import Layout from './components/Layout'
import Dashboard from './pages/Dashboard'
import Import from './pages/Import'
import FrequenciaGeral from './pages/FrequenciaGeral'
import FrequenciaPosicao from './pages/FrequenciaPosicao'
import NumerosQuentesFrios from './pages/NumerosQuentesFrios'
import ParesImpares from './pages/ParesImpares'
import Quadrantes from './pages/Quadrantes'
import SomaDezenas from './pages/SomaDezenas'
import GeradorJogos from './pages/GeradorJogos'

function App() {
  return (
    <BrowserRouter>
      <Routes>
        <Route path="/" element={<Layout />}>
          <Route index element={<Navigate to="/dashboard" replace />} />
          <Route path="dashboard" element={<Dashboard />} />
          <Route path="importar" element={<Import />} />
          <Route path="frequencia-geral" element={<FrequenciaGeral />} />
          <Route path="frequencia-posicao" element={<FrequenciaPosicao />} />
          <Route path="quentes-frios" element={<NumerosQuentesFrios />} />
          <Route path="pares-impares" element={<ParesImpares />} />
          <Route path="quadrantes" element={<Quadrantes />} />
          <Route path="soma-dezenas" element={<SomaDezenas />} />
          <Route path="gerador" element={<GeradorJogos />} />
        </Route>
      </Routes>
    </BrowserRouter>
  )
}

export default App
