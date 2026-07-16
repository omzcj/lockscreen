#!/usr/bin/env python3
"""Create a reproducible source archive for a GitHub Release."""

import argparse
import gzip
import tarfile
from pathlib import Path


def inputs(paths: list[Path]) -> list[Path]:
    members: list[Path] = []
    for path in paths:
        if path.is_dir():
            members.append(path)
            members.extend(sorted(path.rglob("*")))
        elif path.exists():
            members.append(path)
        else:
            raise FileNotFoundError(path)
    return sorted(set(members), key=lambda item: item.as_posix())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--name", required=True)
    parser.add_argument("--version", required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("paths", nargs="+", type=Path)
    args = parser.parse_args()

    args.output.parent.mkdir(parents=True, exist_ok=True)
    prefix = f"{args.name}-{args.version}"
    with args.output.open("wb") as raw:
        with gzip.GzipFile(fileobj=raw, mode="wb", filename="", mtime=0, compresslevel=0) as compressed:
            with tarfile.open(fileobj=compressed, mode="w", format=tarfile.PAX_FORMAT) as archive:
                for path in inputs(args.paths):
                    info = archive.gettarinfo(path, arcname=f"{prefix}/{path.as_posix()}")
                    info.uid = info.gid = 0
                    info.uname = info.gname = ""
                    info.mtime = 0
                    info.mode = 0o755 if path.is_dir() or info.mode & 0o111 else 0o644
                    if path.is_file():
                        with path.open("rb") as source:
                            archive.addfile(info, source)
                    else:
                        archive.addfile(info)


if __name__ == "__main__":
    main()
