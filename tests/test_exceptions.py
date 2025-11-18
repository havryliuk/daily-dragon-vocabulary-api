from daily_dragon.exceptions import WordAlreadyExistsError


def test_word_already_exists_error():
    try:
        raise WordAlreadyExistsError("Word already exists in the database.")
    except WordAlreadyExistsError as e:
        assert str(e) == "Word already exists in the database."