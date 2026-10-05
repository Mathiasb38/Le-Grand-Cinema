from app.services.film_service import get_film_details, get_programmed_films


def test_get_programmed_films(film_data) -> None:
    db_session, past_film, programmed_film, _, _ = film_data
    result = get_programmed_films(db_session)

    assert programmed_film in result
    assert past_film not in result


def test_get_film_details(film_data) -> None:
    db_session, _, film, past_session, programmed_session = film_data
    result_film, result_sessions = get_film_details(db_session, film.id_film)

    assert result_film == film
    assert programmed_session in result_sessions
    assert past_session not in result_sessions
