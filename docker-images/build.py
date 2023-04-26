#!/usr/bin/env python3

from pathlib import Path
import subprocess


def build(dir: Path):
    tag = str(dir).replace("/", ":")
    if ":" not in tag:
        tag += ":v1"

    subprocess.run(["docker", "build", str(dir), "-t", tag])


for dir in filter(lambda p: p.is_dir, Path.cwd().glob("**")):
    if dir.joinpath("Dockerfile").exists():
        build(dir.relative_to(Path.cwd()))
