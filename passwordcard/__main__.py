from . import PasswordCard
from itertools import zip_longest


def grouper(iterable, n, *, fillvalue=None):
    "Collect data into non-overlapping fixed-length chunks or blocks"
    args = [iter(iterable)] * n
    return zip_longest(*args, fillvalue=fillvalue)
    

if __name__ == "__main__":

    from . import create_pdf
    
    create_pdf("test.pdf")
    
    # import sys

    # a = PasswordCard()
    # indicies = a.indicies
    # grid = a.grid

    # sys.stdout.write("    " + " ".join(indicies))
    # sys.stdout.write("\n")
    # # sys.stdout.write("   " + " ".join(indicies[-12:] + indicies[:-12]))
    # sys.stdout.write("\n")

    # for n, _ in enumerate(grid):
    #     sys.stdout.write(f"{n:>2}. ")
    #     sys.stdout.write(" ".join(grouper(grid[n], 4)) + "\n")

    # sys.stdout.write("\n" + a.seed_str + "\n")
    