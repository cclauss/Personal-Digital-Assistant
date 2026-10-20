from claussoft_pda.claussoft_pda import PDA


def test_greeting() -> None:
    personal_digital_assistant = PDA()
    assert personal_digital_assistant
    assert personal_digital_assistant.greeting.startswith("Good")
