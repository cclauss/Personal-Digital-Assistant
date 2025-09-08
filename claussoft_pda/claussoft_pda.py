#!/usr/bin/env python3

# /// script
# requires-python = ">=3.13"
# dependencies = [
#     "PyAudio",
#     "pygame",
#     "pyjokes",
#     "pyttsx3",
#     "SpeechRecognition",
#     "wikipedia",
# ]
# ///

from __future__ import annotations

from datetime import datetime
from getpass import getuser
from string import digits
from time import sleep

import pyttsx3
import speech_recognition
import wikipedia
from pyjokes import get_joke


def init_text_to_speech() -> pyttsx3.Engine:
    engine = pyttsx3.init()
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    return engine


class PDA:
    def __init__(self):
        self.username = getuser()
        if self.username == "cclauss":
            self.username = "Christian"
        print(self.username)
        self.speech_recognizer = speech_recognition.Recognizer()
        self.speech_recognizer.pause_threshold = 0.5
        self.text_to_speech_engine = init_text_to_speech()
        self.print_and_say()

    @property
    def greeting(self) -> str:
        hour = datetime.now().hour
        if hour < 12:
            time_of_day = "Morning"
        else:
            time_of_day = "Afternoon" if hour < 18 else "Evening"
        return f"Good {time_of_day}, {self.username}"

    def listen(self) -> str:
        with speech_recognition.Microphone() as source:
            print(f"Listening... {self.speech_recognizer.pause_threshold}")
            audio = self.speech_recognizer.listen(source)
            return self.speech_recognizer.recognize_google(audio, language="en-us")

    def say(self, msg: str = "") -> str:
        msg = msg or self.greeting
        self.text_to_speech_engine.say(msg)
        self.text_to_speech_engine.runAndWait()
        return msg

    def print_and_say(self, msg: str = "") -> str:
        msg = msg or self.greeting
        print(msg)
        return self.say(msg)

    def date(self) -> str:
        return self.print_and_say(f"{datetime.now():%A, %B %d, %Y}")

    def time(self) -> str:
        return self.print_and_say(f"{datetime.now():%I %M %p}")

    def joke(self) -> str:
        return self.print_and_say(get_joke())

    def chuck_norris_joke(self) -> str:
        return self.print_and_say(get_joke(category="chuck"))

    def wikipedia(self, topic: str = "") -> str:
        return self.print_and_say(wikipedia.summary(topic or "PDA", sentences=2))

    def try_commands(self, user_request) -> str:
        # Is user_request a math problem to be solved?
        if all(char in f"{digits} +-*/" for char in user_request):
            return self.print_and_say(str(eval(user_request)))  # noqa: S307

        words = user_request.lower().split()
        commands = {
            "chuck": self.chuck_norris_joke,
            "norris": self.chuck_norris_joke,
            "joke": self.joke,
            "time": self.time,
            "date": self.date,
            "hello": self.print_and_say,
        }
        for command, method in commands.items():
            if command in words:
                return method()  # type: ignore[operator]
        return ""

    def run_loop(self) -> None:
        while True:
            user_request = self.listen()
            if user_request:
                print(f"You said: {user_request}")
                words = user_request.lower().split()
                if "exit" in words or "quit" in words:
                    return
                if user_request.lower().startswith("wikipedia"):
                    self.wikipedia(" ".join(words[1:]))
                elif not self.try_commands(user_request):
                    self.print_and_say("Sorry, I do not understand.  Please try again.")
            sleep(1)


if __name__ == "__main__":
    PDA().run_loop()
