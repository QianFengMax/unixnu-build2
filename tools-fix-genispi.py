#!/usr/bin/env python3
"""Add QcomGeniSpi to the iPadOS 27 component list in board.toml.

package/TouchProbe.cpp includes "GeniSpi.h", which the QcomGeniSpi component
ships. The iPadOS 17, 26 and macOS lists in board.toml all select it; the
iPadOS 27 [components] list does not, so a clean iPadOS 27 build stops with

    device/package/TouchProbe.cpp:23:10: fatal error: 'GeniSpi.h' file not found

Upstream PR/issue UniXNU/UniXNU-sheng#138 records this fix (still open). We take
only this change from that PR, not its CONFIG_XNU_OPTIMIZE_FOR_SIZE=y, which
changes the kernel optimisation level and breaks the archive bootstrap pass.
"""
import pathlib
import sys

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
board = root / 'board.toml'

if not board.is_file():
    print(f'{board} not found; nothing to do')
    sys.exit(0)

text = board.read_text(encoding='utf-8')
old = '"include" = ["ArmDTPlatform", "ArmCpu", "XnuPrelink", "DarwinBoot", "ShengPreflight", "ShengUfs", "RamBlock", '
new = '"include" = ["ArmDTPlatform", "ArmCpu", "XnuPrelink", "DarwinBoot", "ShengPreflight", "ShengUfs", "QcomGeniSpi", "RamBlock", '

if '"ShengUfs", "QcomGeniSpi", "RamBlock"' in text:
    print('board.toml already selects QcomGeniSpi in the iPadOS 27 list')
    sys.exit(0)

if text.count(old) != 1:
    print(f'expected exactly one iPadOS 27 include line, found {text.count(old)}; leaving it unchanged')
    sys.exit(0)

board.write_text(text.replace(old, new, 1), encoding='utf-8')
print('added QcomGeniSpi to the iPadOS 27 component list')
