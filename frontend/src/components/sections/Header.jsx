import { AlignJustify, X } from 'lucide-react'
import { Link } from 'react-router-dom'
import { useState } from 'react'
import logo from '../../assets/logo.png'
import MobileMenu from './MobileMenu.jsx'

export default Header

function Header() {
  const [isMenuOpen, setIsMenuOpen] = useState(false)

  return (
    <header className="header">
      <Link className="logo-header" to="/">
        <img src={logo} alt="Le Grand Cinéma" />
      </Link>
      <nav className="header__nav" aria-label="Navigation principale">
        <Link className="header__link" to="/films">Films</Link>
      </nav>
      <button className="button-black" id="login-button" type="button">Connexion</button>
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
