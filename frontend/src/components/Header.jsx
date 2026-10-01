import { AlignJustify } from 'lucide-react'
import logo from '../assets/logo.png'

export default Header

function Header() {
  return (
    <header className="header">
      <a className="logo-header" href="#accueil" aria-label="Le Grand Cinéma">
        <img src={logo} alt="Le Grand Cinéma" />
      </a>
      <button className="button-black" id="login-button" type="button">Connexion</button>
      <button className="mobile-menu" type="button" aria-label="Ouvrir le menu">
        <AlignJustify />
      </button>
    </header>
  )
}

