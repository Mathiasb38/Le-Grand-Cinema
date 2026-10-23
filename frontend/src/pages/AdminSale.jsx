import { useEffect, useRef, useState } from 'react'
import { ArrowRight } from 'lucide-react'
import { useAuth } from '../context/AuthContext.jsx'
import { getSeancePlaces, getAdminFilmDetails, getFilms } from '../services/filmService.js'
import { createAdminSale } from '../services/reservationService.js'
import SeatReservation from '../components/groups/SeatReservation.jsx'
import Modal from '../components/sections/Modal.jsx'
import AdminSaleFilms from '../components/groups/AdminSaleFilms.jsx'
import AdminSaleSessions from '../components/groups/AdminSaleSessions.jsx'

export default AdminSale

function AdminSale() {
  const { isAdmin, token } = useAuth()
  const pageRef = useRef(null)
  const hasInteractedRef = useRef(false)
  const [films, setFilms] = useState([])
  const [selectedFilmId, setSelectedFilmId] = useState(null)
  const [film, setFilm] = useState(null)
  const [session, setSession] = useState(null)
  const [places, setPlaces] = useState([])
  const [selectedIds, setSelectedIds] = useState([])
  const [isLoadingFilms, setIsLoadingFilms] = useState(true)
  const [isLoadingSessions, setIsLoadingSessions] = useState(false)
  const [isLoadingPlaces, setIsLoadingPlaces] = useState(false)
  const [isSelling, setIsSelling] = useState(false)
  const [error, setError] = useState(null)
  const [modal, setModal] = useState(null)
  const sessions = film?.seances ?? []
  useEffect(() => {
    if (!isAdmin) return
    getFilms()
      .then(setFilms)
      .catch((loadError) => setError(loadError.message))
      .finally(() => setIsLoadingFilms(false))
  }, [isAdmin])

  useEffect(() => {
    if (!selectedFilmId) {
      setFilm(null)
      setSession(null)
      return
    }

    let isCurrent = true
    setError(null)
    setFilm(null)
    setSession(null)
    setIsLoadingSessions(true)
    getAdminFilmDetails(selectedFilmId, token)
      .then((filmDetails) => {
        if (isCurrent) setFilm(filmDetails)
      })
      .catch((loadError) => {
        if (isCurrent) setError(loadError.message)
      })
      .finally(() => {
        if (isCurrent) setIsLoadingSessions(false)
      })

    return () => { isCurrent = false }
  }, [selectedFilmId, token])

  useEffect(() => {
    setPlaces([])
    setSelectedIds([])

    if (!session) {
      return
    }

    let isCurrent = true
    setError(null)
    setIsLoadingPlaces(true)
    getSeancePlaces(session.id_seance, token)
      .then((items) => {
        if (isCurrent) setPlaces(items)
      })
      .catch((loadError) => {
        if (isCurrent) setError(loadError.message)
      })
      .finally(() => {
        if (isCurrent) setIsLoadingPlaces(false)
      })

    return () => { isCurrent = false }
  }, [session?.id_seance, token])

  useEffect(() => {
    if (hasInteractedRef.current) {
      requestAnimationFrame(() => pageRef.current?.scrollIntoView({ block: 'end', behavior: 'smooth' }))
    }
  }, [selectedFilmId, session?.id_seance, selectedIds, isLoadingSessions, isLoadingPlaces, places.length])

  if (!isAdmin) return null

  function handleSale(event) {
    event.preventDefault()
    setModal({
      type: 'validation',
      message: `Confirmer la vente de ${selectedIds.length} place${selectedIds.length > 1 ? 's' : ''} ?`,
    })
  }

  async function confirmSale() {
    setIsSelling(true)
    setError(null)

    try {
      const billets = await createAdminSale(session.id_seance, selectedIds, token)
      setPlaces((items) => items.map((place) => (
        selectedIds.includes(place.id_place) ? { ...place, disponible: false } : place
      )))
      const updatedSession = {
        ...session,
        places_disponibles: Math.max(session.places_disponibles - selectedIds.length, 0),
      }
      setSession(updatedSession)
      setFilm((current) => ({
        ...current,
        seances: current.seances.map((item) => (
          item.id_seance === session.id_seance ? updatedSession : item
        )),
      }))
      setSelectedIds([])
      setModal({
        type: 'confirmation',
        message: `Vente enregistrée. Billets : ${billets.map((billet) => billet.code_billet).join(', ')}`,
      })
    } catch (saleError) {
      setModal({ type: 'error', message: saleError.message })
    } finally {
      setIsSelling(false)
    }
  }

  return (
    <main className="admin-sale-page" ref={pageRef}>
      <section className="panel admin-sale" aria-label="Vente de billets au guichet">
        {error && <p className="secondaire" role="alert">{error}</p>}
        {isLoadingFilms ? (
          <p className="muted">Chargement des films...</p>
        ) : films.length === 0 ? (
          <p className="muted">Aucun film disponible.</p>
        ) : (
          <AdminSaleFilms
            films={films}
            selectedFilmId={selectedFilmId}
            onSelectFilm={(selectedFilm) => {
              hasInteractedRef.current = true
              setSelectedFilmId(selectedFilm.id_film)
            }}
          />
        )}
        {selectedFilmId && film && (
          <>
            <h2 className="titre">{film.titre}</h2>
            {isLoadingSessions ? (
              <p className="muted">Chargement des séances...</p>
            ) : sessions.length ? (
              <AdminSaleSessions
                sessions={sessions}
                selectedSessionId={session?.id_seance}
                onSelectSession={(selectedSession) => {
                  hasInteractedRef.current = true
                  setSession({ ...selectedSession, idFilm: film.id_film, titreFilm: film.titre })
                }}
              />
            ) : (
              <p className="sessions__empty muted">Aucune séance à venir.</p>
            )}
              {session && (
                <section className="admin-sale__seats" aria-label="Choix des places">
                  {isLoadingPlaces ? (
                    <p className="muted">Chargement des places...</p>
                  ) : (
                    <SeatReservation
                      film={film}
                      session={session}
                      places={places}
                      selectedIds={selectedIds}
                      onSelectionChange={(ids) => {
                        hasInteractedRef.current = true
                        setSelectedIds(ids)
                      }}
                      isLoading={isSelling}
                    >
                      <form className="reservation-form" onSubmit={handleSale}>
                        <button className="button-gold" type="submit" disabled={isSelling || selectedIds.length === 0}>
                          {isSelling ? 'Enregistrement...' : 'Enregistrer la vente'}
                          <ArrowRight aria-hidden="true" />
                        </button>
                      </form>
                    </SeatReservation>
                  )}
                </section>
              )}
          </>
        )}
      </section>
      {modal && (
        <Modal
          {...modal}
          onClose={() => setModal(null)}
          onConfirm={confirmSale}
          onCancel={() => setModal(null)}
          isLoading={isSelling}
        />
      )}
    </main>
  )
}
