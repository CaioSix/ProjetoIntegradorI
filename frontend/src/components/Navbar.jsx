import { useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { api } from '../api/client';

const NAV_LINKS = [
  { to: '/', label: 'Dashboard', icon: '📊' },
  { to: '/tarefas', label: 'Tarefas', icon: '✅' },
  { to: '/empresas', label: 'Empresas', icon: '🏢' },
  { to: '/obrigacoes', label: 'Obrigações', icon: '📋' },
];

export default function Navbar() {
  const location = useLocation();
  const navigate = useNavigate();
  const username = localStorage.getItem('username') || 'Usuário';
  const [menuOpen, setMenuOpen] = useState(false);

  async function handleLogout() {
    try { await api.logout(); } catch {}
    localStorage.removeItem('token');
    localStorage.removeItem('username');
    navigate('/login');
  }

  return (
    <>
      {/* Navbar desktop */}
      <nav className="navbar">
        <div className="navbar-brand">📋 Contábil</div>

        <ul className="navbar-links">
          {NAV_LINKS.map(({ to, label }) => (
            <li key={to}>
              <Link to={to} className={location.pathname === to ? 'active' : ''}>
                {label}
              </Link>
            </li>
          ))}
        </ul>

        <div className="navbar-user">
          <span className="navbar-username">{username}</span>
          <button onClick={handleLogout} className="btn btn-ghost btn-sm">
            Sair
          </button>
        </div>

        {/* Botão hamburguer – só aparece no mobile */}
        <button
          className="navbar-hamburger"
          onClick={() => setMenuOpen((v) => !v)}
          aria-label="Menu"
        >
          {menuOpen ? '✕' : '☰'}
        </button>
      </nav>

      {/* Menu mobile – overlay */}
      {menuOpen && (
        <div
          className="mobile-menu-overlay"
          onClick={() => setMenuOpen(false)}
        >
          <div
            className="mobile-menu"
            onClick={(e) => e.stopPropagation()}
          >
            <div className="mobile-menu-user">
              <span>👤 {username}</span>
            </div>
            <ul>
              {NAV_LINKS.map(({ to, label, icon }) => (
                <li key={to}>
                  <Link
                    to={to}
                    className={location.pathname === to ? 'active' : ''}
                    onClick={() => setMenuOpen(false)}
                  >
                    <span className="mobile-menu-icon">{icon}</span>
                    {label}
                  </Link>
                </li>
              ))}
            </ul>
            <button
              className="btn btn-ghost btn-sm mobile-menu-logout"
              onClick={handleLogout}
            >
              Sair
            </button>
          </div>
        </div>
      )}
    </>
  );
}
