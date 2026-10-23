import { NavLink, Route, Routes } from 'react-router-dom'
import PropTypes from 'prop-types'
import Home from './pages/Home/Home'
import Stats from './pages/Stats/Stats'
import './App.css'

function AppShell({ children }) {
  return <div className="app-shell"><header className="topbar"><NavLink className="brand" to="/"><span className="brand-mark">S</span><span>Sudut Baca</span></NavLink><nav className="main-nav" aria-label="Navigasi utama"><NavLink className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'} to="/">Koleksi</NavLink><NavLink className={({ isActive }) => isActive ? 'nav-link active' : 'nav-link'} to="/stats">Statistik</NavLink></nav><div className="profile-chip"><span className="profile-avatar">AR</span><span>Alfino</span></div></header><main className="page-content">{children}</main><footer className="app-footer"><span>Sudut Baca · Manajemen Buku Pribadi</span><span>Data tersimpan di perangkatmu</span></footer></div>
}

AppShell.propTypes = { children: PropTypes.node.isRequired }

export default function App() {
  return <AppShell><Routes><Route path="/" element={<Home />} /><Route path="/stats" element={<Stats />} /><Route path="*" element={<Home />} /></Routes></AppShell>
}
