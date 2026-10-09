import { X } from 'lucide-react'

export default Modal

const modalTypes = {
  error: { title: 'Erreur', buttonLabel: 'Fermer' },
  confirmation: { title: 'Confirmation', buttonLabel: 'Fermer' },
  validation: { title: 'Validation', confirmLabel: 'Oui', cancelLabel: 'Non' },
}

function Modal({ type, message, onClose, onConfirm, onCancel }) {
  const content = modalTypes[type]
  const isValidation = type === 'validation'

  return (
    <div className="modal-overlay">
      <section
        className={`modal modal--${type}`}
        role="dialog"
        aria-modal="true"
        aria-labelledby="modal-title"
      >
        <button className="modal__close" type="button" aria-label="Fermer" onClick={onClose}>
          <X aria-hidden="true" />
        </button>
        <h2 className="titre" id="modal-title">{content.title}</h2>
        <p className="petit">{message}</p>
        <div className="modal__actions">
          {isValidation ? (
            <>
              <button className="button-gold" type="button" onClick={onConfirm}>
                {content.confirmLabel}
              </button>
              <button className="button-black" type="button" onClick={onCancel}>
                {content.cancelLabel}
              </button>
            </>
          ) : (
            <button className="button-gold" type="button" onClick={onClose}>
              {content.buttonLabel}
            </button>
          )}
        </div>
      </section>
    </div>
  )
}
