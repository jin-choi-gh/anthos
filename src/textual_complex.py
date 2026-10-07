from pathlib import Path

from formats import FORMATS
from models import Format, Representation

def load(path: Path, formats: tuple[Format, ...] = FORMATS) -> Representation:
    raise NotImplementedError

def main():
    raise NotImplementedError

if __name__ == "__main__":
    main()