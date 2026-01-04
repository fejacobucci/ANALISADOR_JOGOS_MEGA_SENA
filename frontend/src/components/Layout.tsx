import { Outlet, Link, useLocation } from 'react-router-dom'
import { Home, Upload, BarChart3, TrendingUp, Percent, Grid3x3, Plus, Dices, MapPin } from 'lucide-react'
import styles from './Layout.module.css'

const Layout = () => {
  const location = useLocation()

  const menuItems = [
    { path: '/dashboard', icon: Home, label: 'Dashboard' },
    { path: '/importar', icon: Upload, label: 'Importar Dados' },
    { path: '/frequencia-geral', icon: BarChart3, label: 'Frequência Geral' },
    { path: '/frequencia-posicao', icon: TrendingUp, label: 'Frequência por Posição' },
    { path: '/quentes-frios', icon: TrendingUp, label: 'Quentes e Frios' },
    { path: '/pares-impares', icon: Percent, label: 'Pares e Ímpares' },
    { path: '/quadrantes', icon: Grid3x3, label: 'Quadrantes' },
    { path: '/soma-dezenas', icon: Plus, label: 'Soma das Dezenas' },
    { path: '/cidades-ganhadoras', icon: MapPin, label: 'Cidades Ganhadoras' },
    { path: '/gerador', icon: Dices, label: 'Gerador de Jogos' },
  ]

  return (
    <div className={styles.container}>
      <aside className={styles.sidebar}>
        <div className={styles.logo}>
          <h1>Mega Sena</h1>
          <p>Análises e Gerador</p>
        </div>
        <nav className={styles.nav}>
          {menuItems.map((item) => {
            const Icon = item.icon
            const isActive = location.pathname === item.path
            return (
              <Link
                key={item.path}
                to={item.path}
                className={`${styles.navItem} ${isActive ? styles.active : ''}`}
              >
                <Icon size={20} />
                <span>{item.label}</span>
              </Link>
            )
          })}
        </nav>
      </aside>
      <main className={styles.main}>
        <Outlet />
      </main>
    </div>
  )
}

export default Layout
