from app.services.film_service import get_film_details, get_programmed_films


def test_get_programmed_films(film_data) -> None:
    db_session, past_film, programmed_film, far_film, _, _, _ = film_data
    result = get_programmed_films(db_session)

    assert programmed_film in result
    assert past_film not in result
    assert far_film not in result


def test_get_film_details(film_data) -> None:
    db_session, _, film, _, past_seance, programmed_seance, far_seance = film_data
    result = get_film_details(
        db_session,
        film.id_film,
        programmed_seance.date_heure_debut.date(),
    )

    assert result.id_film == film.id_film
    assert result.seances[0].id_seance == programmed_seance.id_seance
    assert result.seances[0].places_disponibles == 7
    result_ids = [seance.id_seance for seance in result.seances]
    assert past_seance.id_seance not in result_ids
    assert far_seance.id_seance not in result_ids
