from claussoft_pda.claussoft_pda import PDA


def test_greeting() -> None:
    assert PDA().greeting.startswith("Good")
