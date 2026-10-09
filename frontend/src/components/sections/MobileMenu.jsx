import { Link } from 'react-router-dom'

export default MobileMenu

function MobileMenu({ onClose }) {
  return (
    <nav className="mobile-nav" aria-label="Navigation mobile">
      <Link
        className="header__link mobile-nav__link--active"
        to="/films"
        onClick={onClose}
      >
        Films
      </Link>
      <Link className="button-black" to="/connexion" onClick={onClose}>
        Connexion
      </Link>
    </nav>
  )
}
