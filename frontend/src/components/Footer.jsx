import logo from '../assets/logo.png'

export default Footer

function Footer() {
  return (
    <footer className="footer">
      <a className="logo-footer" href="#accueil"><img src={logo} alt="Le Grand Cinéma" /></a>
    </footer>
  )
}

