"""
PasswordCard generator
"""

from ast import Pass
from typing import List, Set, Tuple, Generator
from random import randint, sample, seed
from secrets import randbits

NUMBERS = "0123456789"
SYMBOLS = "/?~.;[]!@#$*=+"
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
                this_char = sample(list(charset), 1)[0]

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

    def code_generator(self) -> Generator[int, None, None]:
        return self.generate_code(self.seed)

    def codes(self, length) -> str:
        g = self.generate_code(self.seed)
        retval  = ""
        for _ in range(length):
            retval += str(next(g))

        return retval


    @property
    def grid(self) -> List[str]:
        return self.make_grid(self.seed)[1]


from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.platypus.tables import Table, TableStyle
from reportlab.platypus.paragraph import Paragraph
from reportlab.pdfbase import pdfmetrics

def create_pdf(filename, page_size = letter):
    CARD_SIZE = (3.375 * 72. , 2.125 * 72.)
    CARD_PITCH = (3.5 * 72., 2.25 * 72.)
    ORIGIN = (0.5 * 72., 0.5 * 72.)
    CONTENT_INSET = (12., 12.)

    def pointsrange(start, stop, step):
        while start < stop:
            yield start
            start = start + step

    def draw_all_crosshairs(c, x, y, radius):
        c.setLineWidth(0.25)
        draw_crosshairs(c, x, y, radius)
        draw_crosshairs(c, CARD_SIZE[0] + x, y, radius)
        draw_crosshairs(c, x, CARD_SIZE[1] + y, radius)
        draw_crosshairs(c, x + CARD_SIZE[0], y + CARD_SIZE[1], radius)

    def draw_crosshairs(c, x, y, radius):
        c.line(x - radius, y, x + radius, y)
        c.line(x, y - radius, x, y + radius)

    c = canvas.Canvas(filename, pagesize=page_size, bottomup = 0)

    c.setFont("Courier", 9.)

    for y in pointsrange(ORIGIN[1], page_size[1], CARD_PITCH[1]):
        p = PasswordCard()
        codes = p.codes(300)
        for x in pointsrange(ORIGIN[0], page_size[0], CARD_PITCH[0]):
        
            draw_all_crosshairs(c, x, y, 6.)
            
            data = [["","A-D","E-J","K-N","O-S","T-W","X-Z"]]
            for n in range(10):
                row = [f"{n}"]
                for i in range(6):
                    group = ""
                    for _ in range(5):
                        group = codes[n * 30 + i * 5:n * 30 + i * 5 + 5]
                    row.append(group)
                data.append(row)

            t = Table(data = list(reversed(data)), colWidths=[16,34.], rowHeights=12.)

            table_styles = [
                ('FONTNAME',(0,0),(-1,-1),"Courier"),
                ('FONTSIZE',(0,0),(0,-1), 8.),
                ('VALIGN',(0,0),(0,-1), "MIDDLE"), 
            ]

            for n in range(1,10,2):
                table_styles.append(('BACKGROUND',(0,n),(-1,n), (.9,.9,.9)))

            t.setStyle(TableStyle(table_styles))

            _, _ = t.wrap(CARD_SIZE[0] - CONTENT_INSET[0] * 2, CARD_SIZE[1] - CONTENT_INSET[1] * 2)
            t.drawOn(c, x + CONTENT_INSET[0], y + CONTENT_INSET[1])

            # id = Paragraph(p.seed_str)
            # _, _ = id.wrap(CARD_SIZE[0] - CONTENT_INSET[0] * 2, 12.)
            # id.drawOn(c, x, y)

            
            
    c.showPage()
    c.save()


