import { Link, NavLink } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext.jsx'
import { CalendarDays, Ticket } from 'lucide-react'

export default MobileMenu

function MobileMenu({ onClose }) {
  const { isAuthenticated, isAdmin } = useAuth()

  return (
    <nav className="mobile-nav" aria-label="Navigation mobile">
      {!isAdmin && (
        <Link
          className="header__link mobile-nav__link--active"
          to="/films"
          onClick={onClose}
        >
          Films
        </Link>
      )}
      {isAdmin && (
        <>
          <NavLink
            className={({ isActive }) => isActive ? 'button-gold' : 'button-black'}
            end
            to="/admin/ventes"
            onClick={onClose}
          >
            <Ticket aria-hidden="true" />
            Vente guichet
          </NavLink>
          <NavLink
            className={({ isActive }) => isActive ? 'button-gold' : 'button-black'}
            end
            to="/admin/recherche"
            onClick={onClose}
          >
            <CalendarDays aria-hidden="true" />
            Réservations
          </NavLink>
        </>
      )}
      {!isAdmin && isAuthenticated ? (
        <Link className="header__link" to="/compte" onClick={onClose}>
          Mon compte
        </Link>
      ) : !isAdmin && (
        <Link className="button-black" to="/connexion" onClick={onClose}>
          Connexion
        </Link>
      )}
    </nav>
  )
}
