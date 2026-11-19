#!/usr/bin/env python3
"""Add the ios27 page-permission patch to the AdrenoMetal bridge patch list."""
from pathlib import Path
import sys

p = Path('UniXNU/scripts/build-adreno-metal-bridge.py')
if not p.is_file():
    print('build-adreno-metal-bridge.py not found; nothing to do')
    sys.exit(0)

text = p.read_text()
old = "'0064-copies-leave-unreachable-pages-alone.patch']]"
new = ("'0064-copies-leave-unreachable-pages-alone.patch',\n"
       "    '0065-ios-read-pages-and-mapped-writable.patch']]")

if '0065-ios-read-pages-and-mapped-writable.patch' in text:
    print('0065 already in the patch list')
elif old in text:
    p.write_text(text.replace(old, new, 1))
    print('metal bridge patch list updated')
else:
    print('anchor not found; leaving unchanged')
