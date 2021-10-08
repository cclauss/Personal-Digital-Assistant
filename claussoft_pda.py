#!/usr/bin/env python3

from __future__ import annotations

import platform
from datetime import datetime
from getpass import getuser

import pyttsx3
import speech_recognition as sr
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
    
    def say(self, msg: str="") -> None:
        msg = msg or self.greeting
        self.text_to_speech_engine.say(msg)
        self.text_to_speech_engine.runAndWait()
    
    def print_and_say(self, msg: str="") -> None:
        msg = msg or self.greeting
        print(msg)
        self.say(msg)


if __name__ == "__main__":
    PDA()
