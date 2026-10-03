import { ArrowRight } from 'lucide-react'
import { Link, Route, Routes } from 'react-router-dom'

import Footer from './components/Footer.jsx'
import Header from './components/Header.jsx'

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
      </Routes>
      <Footer />
    </div>
  )
}
