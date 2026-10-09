import AuthPanel from '../components/groups/AuthPanel.jsx'

export default Login

function Login() {
  return (
    <main className="auth-page">
      <section className="auth-page__hero hero">
        <h1 className="display-xl">CONNEXION</h1>
      </section>

      <AuthPanel
        ariaLabel="Connexion"
        linkLabel="Créer un compte"
        linkTo="/inscription"
        submitLabel="Connexion"
      />
    </main>
  )
}
