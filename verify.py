#!/usr/bin/env python3
"""Poster checker for the news-image-20261123 entry.

Checks the gate rules the kit states, locally:
- entry.png is a whole PNG, 1024x1024, at most 1 MiB
- gen_image.py is deterministic: two runs write identical bytes
- main.ts copies entry.png byte-identically to the output dir
Usage: python3 verify.py  (run from the repo directory)
Exit 0 when every check passes, 1 otherwise.
"""
import hashlib
import os
import subprocess
import sys
import tempfile

from PIL import Image

HERE = os.path.dirname(os.path.abspath(__file__))
ENTRY = os.path.join(HERE, "entry.png")
GEN = os.path.join(HERE, "gen_image.py")
MAIN = os.path.join(HERE, "main.ts")


def sha256(path):
    return hashlib.sha256(open(path, "rb").read()).hexdigest()


def fail(msg):
    print("FAIL:", msg)
    return False


def main():
    ok = True

    if not os.path.exists(ENTRY):
        print(fail("entry.png is missing"))
        return 1
    size = os.path.getsize(ENTRY)
    if size > 1048576:
        ok = fail(f"entry.png is {size} bytes, over the 1 MiB cap") and ok
    else:
        print(f"OK: entry.png is {size} bytes (cap 1 MiB)")
    with Image.open(ENTRY) as im:
        if im.format != "PNG":
            ok = fail(f"entry.png format is {im.format}, expected PNG") and ok
        else:
            print("OK: entry.png is a PNG")
        if im.size != (1024, 1024):
            ok = fail(f"entry.png is {im.size}, expected 1024x1024") and ok
        else:
            print("OK: entry.png is 1024x1024")
        im.load()  # whole image: every chunk decodes

    # determinism: regenerate twice, compare hashes
    first = sha256(ENTRY)
    subprocess.run([sys.executable, GEN], check=True, capture_output=True)
    second = sha256(ENTRY)
    if first != second:
        ok = fail("gen_image.py is not deterministic across runs") and ok
    else:
        print(f"OK: gen_image.py deterministic (sha256 {first[:16]}...)")

    # main.ts: the grader runs it twice, so run it twice here into two
    # different temp dirs and require both outputs byte-identical to entry.png
    expected = sha256(ENTRY)
    with tempfile.TemporaryDirectory() as tmp1, tempfile.TemporaryDirectory() as tmp2:
        for label, tmp in (("first", tmp1), ("second", tmp2)):
            env = dict(os.environ, MAKEFUN_OUTPUT_DIR=tmp)
            r = subprocess.run(["node", MAIN], env=env, capture_output=True,
                               text=True)
            if r.returncode != 0:
                ok = fail(f"node main.ts ({label} run) exited {r.returncode}: {r.stderr.strip()}") and ok
                break
            copied = os.path.join(tmp, "entry.png")
            if not os.path.exists(copied):
                ok = fail(f"main.ts ({label} run) wrote no entry.png") and ok
                break
            elif sha256(copied) != expected:
                ok = fail(f"main.ts ({label} run) output differs from entry.png") and ok
                break
        else:
            print("OK: main.ts run twice, both outputs byte-identical to entry.png")

    print("ALL CHECKS PASSED" if ok else "CHECKS FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
