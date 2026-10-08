import argparse
import sys
from pathlib import Path

from formats import FORMATS
from models import Format, Representation, Substrate, SynthesisError


def load(path: Path, formats: tuple[Format, ...] = FORMATS) -> Representation:
    if not path.is_file():
        raise SynthesisError(f"{path}: no such file")

    matches = [f for f in formats if path.name.lower().endswith(f.suffix)]

    if not matches:
        known = ", ".join(f.suffix for f in formats) or "none yet"
        raise SynthesisError(
            f"{path}: no format for this file (known suffixes: {known})"
        )
    chosen = max(matches, key=lambda f: len(f.suffix))

    source = path.read_text(encoding="utf-8-sig")

    rest = path.name[: -len(chosen.suffix)]
    _, _, qualifier = rest.partition(".")
    name = f"{chosen.name}-{qualifier}" if qualifier else chosen.name

    return Representation(path=path, format=chosen, source=source, name=name)


def choose_base(representations: tuple[Representation, ...]) -> Representation:
    candidates = [r for r in representations if r.format.can_be_base]

    if len(candidates) == 1:
        return candidates[0]

    if not candidates:
        raise SynthesisError("none of the provided files can be the base")

    paths = ", ".join(str(r.path) for r in candidates)
    raise SynthesisError(f"several files could be the base: {paths}")


def make_substrate(base: Representation) -> Substrate:
    try:
        return base.format.transcribe(base.format.read(base))
    except SynthesisError as error:
        raise SynthesisError(f"{base.path}: {error}") from error


def main(argv=None):
    sys.stdout.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Create a textual complex.")
    ap.add_argument(
        "files", nargs="+", type=Path, help="The representations of one text"
    )
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
