import { AlignJustify } from 'lucide-react'
import { Link } from 'react-router-dom'
import logo from '../assets/logo.png'

export default Header

function Header() {
  return (
    <header className="header">
      <Link className="logo-header" to="/" aria-label="Le Grand Cinéma">
        <img src={logo} alt="Le Grand Cinéma" />
      </Link>
      <button className="button-black" id="login-button" type="button">Connexion</button>
      <button className="mobile-menu" type="button" aria-label="Ouvrir le menu">
        <AlignJustify />
      </button>
    </header>
  )
}

