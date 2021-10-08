#!/usr/bin/env python3

from __future__ import annotations

import platform
from datetime import datetime
from getpass import getuser

import pyttsx3
import speech_recognition
import wikipedia
from pyjokes import get_joke


def init_text_to_speech() -> pyttsx3.Engine:
    driver = {"Darwin": "nsss", "Windows": "sapi5"}.get(platform.system(), "espeak")
    engine = pyttsx3.init(driver)
    voices = engine.getProperty("voices")
    engine.setProperty("voice", voices[0].id)
    return engine


class PDA(object):
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

    def listen() -> str:
        with speech_recognition.Microphone() as source:
            print("Listening....")
            return self.speech_recognizer.listen(source)
    
    def say(self, msg: str = "") -> str:
        msg = msg or self.greeting
        self.text_to_speech_engine.say(msg)
        self.text_to_speech_engine.runAndWait()
        return msg

    def print_and_say(self, msg: str = "") -> str:
        msg = msg or self.greeting
        print(msg)
        return self.say(msg)
    
    def joke(self) -> str:
        return print_and_say(get_joke())

    def wikipedia(self, topic: str = "") -> str:
        return self.print_and_say(wikipedia.summary(topic, sentences=2))


if __name__ == "__main__":
    PDA()
