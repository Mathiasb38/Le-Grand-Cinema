import logo from '../assets/logo.png'
import { Link } from 'react-router-dom'

export default Footer

function Footer() {
  return (
    <footer className="footer">
      <Link className="logo-footer" to="/"><img src={logo} alt="Le Grand Cinéma" /></Link>
    </footer>
  )
}

