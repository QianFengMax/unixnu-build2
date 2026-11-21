#!/usr/bin/env python3
"""Stage the freebsd source for Ath12kWifi.

fetch-sources.py clones linux/supplicant but expects the freebsd checkout to
exist already; it is fetched by commit, not by branch, with a sparse checkout.

See UniXNU-sheng's own package workflow ("prepare device sources and firmware").

This script runs with the device repository as the working directory, but it
lives in the workflow repository, so the device root is passed in explicitly
(or taken from the current directory).
"""
import json
import pathlib
import subprocess
import sys

device = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
root = device / 'drivers' / 'Ath12kWifi'
lock = json.loads((root / 'tools' / 'source-lock.json').read_text(encoding='utf-8'))
src = lock['freebsd']
dst = root / 'deps' / 'freebsd'

if dst.exists():
    print(f'{dst} already present')
    sys.exit(0)

dst.mkdir(parents=True, exist_ok=True)


def git(*args):
    subprocess.run(['git', '-C', str(dst), *args], check=True)


git('init')
git('remote', 'add', 'origin', src['url'])
git('sparse-checkout', 'init')
git('fetch', '--depth', '1', '--filter=blob:none', 'origin', src['commit'])
git('checkout', 'FETCH_HEAD')
print(f'freebsd staged at {src["commit"]} -> {dst}')
