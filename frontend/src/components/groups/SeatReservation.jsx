import { useRef, useState } from 'react'

export default SeatReservation

function SeatReservation({ film, session, places = [], readOnly = false, children }) {
  const [selectedIds, setSelectedIds] = useState([])
  const [isZoomed, setIsZoomed] = useState(false)
  const scrollRef = useRef(null)
  const rows = [...new Set(places.map((place) => place.rangee))].sort()
  const columns = [...new Set(places.map((place) => place.numero))].sort((a, b) => a - b)
  const selectedPlaces = places.filter((place) => place.disponible && selectedIds.includes(place.id_place))
  const date = new Date(session.date_heure_debut)

  function togglePlace(id) {
    if (readOnly) return

    setSelectedIds((ids) => ids.includes(id)
      ? ids.filter((selectedId) => selectedId !== id)
      : [...ids, id])
    setIsZoomed(false)
  }

  return (
    <div className="seat-reservation" role="region" aria-label="Plan des places">
      <div className={`seat-reservation__plan${isZoomed ? ' seat-reservation__plan--zoomed' : ''}`}>
        <div className="seat-reservation__viewport">
          <div
            className="seat-reservation__scroll"
            ref={scrollRef}
            tabIndex={0}
            role="region"
            aria-label="Plan de la salle"
            onClick={(event) => {
              if (isZoomed && !event.target.closest('.seat-reservation__seat')) {
                setIsZoomed(false)
              }
            }}
            onFocusCapture={() => {
              if (window.matchMedia('(max-width: 650px)').matches) setIsZoomed(true)
            }}
          >
            <div className="seat-reservation__map">
              <svg className="seat-reservation__screen" viewBox="0 0 720 48" role="img" aria-label="Écran" preserveAspectRatio="none">
                <path d="M 4 36 C 241 6 479 6 716 36" />
              </svg>
              <table className="seat-reservation__seats" aria-label="Places de la salle">
                <thead>
                  <tr>
                    <td />
                    {columns.map((number) => <th scope="col" key={number}>{number}</th>)}
                  </tr>
                </thead>
                <tbody>
                  {rows.map((row) => (
                    <tr key={row}>
                      <th className="principal" scope="row">{row}</th>
                      {columns.map((number) => {
                        const place = places.find((place) => place.rangee === row && place.numero === number)
                        if (!place) return <td className="principal" key={number} />
                        const selected = place.disponible && selectedIds.includes(place.id_place)

                        return (
                          <td className="principal" key={number}>
                            <button
                              className={`seat-reservation__seat${selected ? ' seat-reservation__seat--selected' : ''}${!place.disponible ? ' seat-reservation__seat--unavailable' : ''}`}
                              type="button"
                              aria-label={`Place ${row}${number}${!place.disponible ? ', indisponible' : ''}`}
                              aria-pressed={selected}
                              disabled={!place.disponible || readOnly}
                              onClick={() => togglePlace(place.id_place)}
                            />
                          </td>
                        )
                      })}
                    </tr>
                  ))}
                </tbody>
              </table>
              <ul className="seat-reservation__legend petit" aria-label="Légende des places">
                <li><span className="seat-reservation__seat" aria-hidden="true" />Place disponible</li>
                {!readOnly && <li><span className="seat-reservation__seat seat-reservation__seat--selected" aria-hidden="true" />Place sélectionnée</li>}
                <li><span className="seat-reservation__seat seat-reservation__seat--unavailable" aria-hidden="true" />Place indisponible</li>
              </ul>
            </div>
          </div>
          {!isZoomed && (
            <button
              className="seat-reservation__map-zoom"
              type="button"
              aria-label="Agrandir le plan de la salle"
              onClick={() => {
                setIsZoomed(true)
                requestAnimationFrame(() => {
                  const scroll = scrollRef.current
                  scroll.scrollLeft = (scroll.scrollWidth - scroll.clientWidth) / 2
                  scroll.scrollIntoView({ block: 'center' })
                })
              }}
            />
          )}
        </div>
        {places.length === 0 && <p className="muted">Aucune place disponible.</p>}
      </div>

      <div className="seat-reservation__summary">
        <p className="titre">{film.titre}</p>
        <p className="principal">
          Séance : <time dateTime={session.date_heure_debut}>
            {date.toLocaleDateString('fr-FR')} à {date.toLocaleTimeString('fr-FR', { hour: '2-digit', minute: '2-digit' })}
          </time>
        </p>
        <p className="secondaire">{session.nom_salle} - Salle {session.numero_salle}</p>
        {!readOnly && (
          <ul className="seat-reservation__selection" aria-label="Places sélectionnées" aria-live="polite">
            {selectedPlaces.map((place) => (
              <li key={place.id_place}>{place.rangee}{place.numero}</li>
            ))}
          </ul>
        )}
        {children}
      </div>
    </div>
  )
}
