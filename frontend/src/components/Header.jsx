import logo from '../assets/logo.png'

export default Header

function Header() {
  return (
    <header className="header">
      <a className="logo-header" href="#accueil" aria-label="Le Grand Cinéma">
        <img src={logo} alt="Le Grand Cinéma" />
      </a>
      <button id="login-button" className="button-black" type="button">Connexion</button>
    </header>
  )
}

