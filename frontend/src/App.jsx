import { ArrowRight } from 'lucide-react'
import Footer from './components/Footer.jsx'
import Header from './components/Header.jsx'

export default App

function App() {
  return (
    <div className="app">
      <Header />
      <main className="home">
        <h1>LE GRAND CINÉMA</h1>
        <button className="button-gold" type="button">
          Voir les films
          <ArrowRight />
        </button>
      </main>
      <Footer />
    </div>
  )
}
