import { ArrowRight } from 'lucide-react'
import { Link, Route, Routes } from 'react-router-dom'

import Footer from './components/sections/Footer.jsx'
import Header from './components/sections/Header.jsx'
import FilmCatalog from './pages/FilmCatalog.jsx'
import FilmDetail from './pages/FilmDetail.jsx'
import AdminLogin from './pages/AdminLogin.jsx'
import Login from './pages/Login.jsx'
import Register from './pages/Register.jsx'

export default App

function App() {
  return (
    <div className="app">
      <Header />
      <Routes>
        <Route path="/" element={
          <main className="home hero">
            <h1 className="display-xl">LE GRAND CINÉMA</h1>
            <Link className="button-gold" to="/films">
              Voir les films
              <ArrowRight />
            </Link>
          </main>
        } />
        <Route path="/films" element={<FilmCatalog />} />
        <Route path="/films/:idFilm" element={<FilmDetail />} />
        <Route path="/connexion" element={<Login />} />
        <Route path="/admin/connexion" element={<AdminLogin />} />
        <Route path="/inscription" element={<Register />} />
      </Routes>
      <Footer />
    </div>
  )
}
