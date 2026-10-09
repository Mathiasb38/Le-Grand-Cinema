import { Eye, EyeOff, LockKeyhole, Mail } from 'lucide-react'
import { useState } from 'react'
import { Link } from 'react-router-dom'

export default AuthPanel

function AuthPanel({
  ariaLabel,
  linkLabel,
  linkTo,
  onSubmit = () => {},
  passwordMinLength,
  submitLabel,
}) {
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPassword, setShowPassword] = useState(false)

  function handleSubmit(event) {
    event.preventDefault()
    onSubmit({
      email,
      password,
      clearForm: () => {
        setEmail('')
        setPassword('')
      },
    })
  }

  return (
    <section className="auth-panel" aria-label={ariaLabel}>
      <form
        className="auth-form"
        onSubmit={handleSubmit}
      >
        <label className="auth-field">
          <span>Adresse e-mail</span>
          <span className="auth-field__control">
            <Mail aria-hidden="true" />
            <input
              type="email"
              placeholder="votre@email.com"
              value={email}
              onChange={(event) => setEmail(event.target.value)}
              required
            />
          </span>
        </label>

        <label className="auth-field">
          <span>Mot de passe</span>
          <span className="auth-field__control">
            <LockKeyhole aria-hidden="true" />
            <input
              type={showPassword ? 'text' : 'password'}
              placeholder="Votre mot de passe"
              value={password}
              onChange={(event) => setPassword(event.target.value)}
              minLength={passwordMinLength}
              required
            />
            <button
              className="auth-password-toggle"
              type="button"
              aria-label={showPassword ? 'Masquer le mot de passe' : 'Afficher le mot de passe'}
              onClick={() => setShowPassword(!showPassword)}
            >
              {showPassword ? <EyeOff aria-hidden="true" /> : <Eye aria-hidden="true" />}
            </button>
          </span>
        </label>

        {linkLabel && <Link className="lien" to={linkTo}>{linkLabel}</Link>}
        <button className="button-black" type="submit">
          {submitLabel}
        </button>
      </form>
    </section>
  )
}
