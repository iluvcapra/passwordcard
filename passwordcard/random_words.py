from . import LOWERCASE
from typing import Generator
import secrets

VOWELS = set("aeiou")
CONSONTANTS = set(LOWERCASE).difference(VOWELS)


def word_generator() -> Generator[str, None, None]:
    with open("/usr/share/dict/words") as file:
        words = [word.strip() for word in file if len(word) in [3, 4]]
        
        for _ in range(4):
            print(secrets.choice(words))
