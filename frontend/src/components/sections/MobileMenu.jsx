import { Link } from 'react-router-dom'
import { useAuth } from '../../context/AuthContext.jsx'

export default MobileMenu

function MobileMenu({ onClose }) {
  const { isAuthenticated } = useAuth()

  return (
    <nav className="mobile-nav" aria-label="Navigation mobile">
      <Link
        className="header__link mobile-nav__link--active"
        to="/films"
        onClick={onClose}
      >
        Films
      </Link>
      {isAuthenticated ? (
        <Link className="header__link" to="/compte" onClick={onClose}>
          Mon compte
        </Link>
      ) : (
        <Link className="button-black" to="/connexion" onClick={onClose}>
          Connexion
        </Link>
      )}
    </nav>
  )
}
