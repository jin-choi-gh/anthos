import argparse
import sys
from pathlib import Path

from formats import FORMATS
from models import Format, Representation, Substrate, SynthesisError

def load(path: Path, formats: tuple[Format, ...] = FORMATS) -> Representation:
    raise NotImplementedError

def choose_base(representations: tuple[Representation, ...]) -> Representation:
    raise NotImplementedError

def make_substrate(base: Representation) -> Substrate:
    raise NotImplementedError

def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Create a textual complex.")
    ap.add_argument("files", nargs="+", type=Path,
                    help="The representations of one text")
    args = ap.parse_args(argv)

    try:
        representations = tuple(load(path) for path in args.files)
        base = choose_base(representations)
        substrate = make_substrate(base)

        for line in substrate.lines:
            print(f"{line.id:>4} {line.text}")


    except SynthesisError as e:
        sys.exit(f"error: {e}")


if __name__ == "__main__":
    main()