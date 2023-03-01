"""
PasswordCard generator
"""

from typing import List, Set, Tuple, Generator
from random import randint, sample, seed


NUMBERS = "0123456789"
SYMBOLS = "/?~.;[]!@#$%^&*()=+"
UPPERCASE = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
LOWERCASE = "abcdefghijklmnopqrstuvwxyz"


class PasswordCard:
    """
    """
    seed: int
    charset: Set[chr]
    
    @staticmethod
    def decode_seed_str(seed_str: str) -> int:
        int(seed_str[0:16], 16)

    @staticmethod
    def generate_code(seed_val: int) -> Generator[int, None, None]:
        seed(seed_val)

        charset = set()
        charset.update(UPPERCASE)
        charset.update(LOWERCASE)
        charset.update(NUMBERS)
        charset.update(SYMBOLS)

        since_num = 0
        since_sym = 0
        since_upper = 0
        since_lower = 0

        while True:
            if since_num > 10:
                this_char = sample(NUMBERS, 1)[0]
            elif since_sym > 10:
                this_char = sample(SYMBOLS, 1)[0]
            elif since_upper > 10:
                this_char = sample(UPPERCASE, 1)[0]
            elif since_lower > 10:
                this_char = sample(LOWERCASE, 1)[0]
            else:
                this_char = sample(charset, 1)[0]

            since_num += 1
            since_sym += 1
            since_upper += 1
            since_lower += 1

            if this_char in UPPERCASE:
                since_upper = 0
            elif this_char in LOWERCASE:
                since_lower = 0
            elif this_char in NUMBERS:
                since_num = 0
            elif this_char in SYMBOLS:
                since_sym = 0

            yield this_char
                
    @staticmethod
    def make_grid(seed_val: int) -> Tuple[str, List[str]]:
        
        indicies = UPPERCASE

        gen = PasswordCard.generate_code(seed_val)

        lines = []
        for _ in range(12):
            c = []
            for _ in indicies:
                c.append(next(gen))
            lines.append("".join(c))

        return (indicies, lines)

    def __init__(self,
                 seed: int | str | None = None) -> None:
    
        if isinstance(seed, str):
            self.seed = self.decode_seed_str(seed)
        elif isinstance(seed, int):
            self.seed = seed
        else:
            self.seed = randint(0, 2**64 - 1)

    @property
    def seed_str(self):
        return "{:0>16x}".format(self.seed)

    @property
    def indicies(self) -> str:
        return self.make_grid(self.seed)[0]

    @property
    def grid(self) -> List[str]:
        return self.make_grid(self.seed)[1]

