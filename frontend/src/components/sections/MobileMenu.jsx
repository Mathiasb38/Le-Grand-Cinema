import { Link } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext.jsx'
import { CalendarDays } from 'lucide-react'

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
        <Link className="button-gold" to="/admin/recherche" onClick={onClose}>
          <CalendarDays aria-hidden="true" />
          Réservations
        </Link>
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
