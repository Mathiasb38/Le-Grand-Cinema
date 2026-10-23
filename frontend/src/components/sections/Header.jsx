import { AlignJustify, User, X, CalendarDays, Ticket, ChartNoAxesCombined } from 'lucide-react'
import { Link, NavLink } from 'react-router-dom'
import { useState } from 'react'
import logo from '../../assets/logo.png'
import { useAuth } from '../../context/AuthContext.jsx'
import MobileMenu from './MobileMenu.jsx'

export default Header

function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)
  const { isAuthenticated, isAdmin } = useAuth()

  return (
    <header className="header">
      <Link className="logo-header" to="/">
        <img src={logo} alt="Le Grand Cinéma" />
      </Link>
      <nav className="header__nav" aria-label="Navigation principale">
        <Link className="header__link" to="/films">Films</Link>
      </nav>
      {isAdmin && (
        <div className="header__admin-links">
          <NavLink
            className={({ isActive }) => `${isActive ? 'button-gold' : 'button-black'} header__admin-link`}
            end
            to="/admin/analyse"
          >
            <ChartNoAxesCombined aria-hidden="true" />
            Analyse
          </NavLink>
          <NavLink
            className={({ isActive }) => `${isActive ? 'button-gold' : 'button-black'} header__admin-link`}
            end
            to="/admin/ventes"
          >
            <Ticket aria-hidden="true" />
            Vente guichet
          </NavLink>
          <NavLink
            className={({ isActive }) => `${isActive ? 'button-gold' : 'button-black'} header__admin-link`}
            end
            to="/admin/recherche"
          >
            <CalendarDays aria-hidden="true" />
            Réservations
          </NavLink>
        </div>
      )}
      {!isAdmin && isAuthenticated ? (
        <Link className="user-icon" to="/compte" aria-label="Mon compte">
          <User aria-hidden="true" />
        </Link>
      ) : !isAdmin && (
        <Link className="button-black" id="login-button" to="/connexion">Connexion</Link>
      )}
      <button
        className="mobile-menu"
        type="button"
        aria-label={isMenuOpen ? 'Fermer' : 'Ouvrir'}
        aria-expanded={isMenuOpen}
        onClick={() => setIsMenuOpen(!isMenuOpen)}
      >
        {isMenuOpen ? <X /> : <AlignJustify />}
      </button>
      {isMenuOpen && <MobileMenu onClose={() => setIsMenuOpen(false)} />}
    </header>
  )
}
