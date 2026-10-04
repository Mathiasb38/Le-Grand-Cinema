import { ArrowRight } from 'lucide-react'
import { Link, Route, Routes } from 'react-router-dom'

import Footer from './components/Footer.jsx'
import Header from './components/Header.jsx'
import FilmCatalog from './components/FilmCatalog.jsx'

export default App

function App() {
  return (
    <div className="app">
      <Header />
      <Routes>
        <Route path="/" element={
          <main className="home">
            <h1>LE GRAND CINÉMA</h1>
            <Link className="button-gold" to="/films">
              Voir les films
              <ArrowRight />
            </Link>
          </main>
        } />
        <Route path="/films" element={<FilmCatalog />} />
      </Routes>
      <Footer />
    </div>
  )
}
