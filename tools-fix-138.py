#!/usr/bin/env python3
"""Apply upstream issue #138's fix to sheng-startup-failure-log.patch in place.

The patch anchors on a "#else ... #endif" pair that only exists in the macOS
owner-data variant, so a clean iPadOS 27 kernel build stops with
    error: bsd/kern/kern_exec.c: patch does not apply
at bsd/kern/kern_exec.c:10118.

Upstream issue/PR UniXNU/UniXNU-sheng#138 (still open) records the fix: drop
those two context lines and re-anchor the hunk on the shared
native_owner_data_prepare call.

We apply only this one fix instead of checking out the PR head, because that
head also adds CONFIG_XNU_OPTIMIZE_FOR_SIZE=y, which changes the kernel
optimisation level and makes the archive bootstrap pass fail to link.
"""
import pathlib
import sys

root = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
patch = root / 'patches' / 'xnu-12377' / 'sheng-startup-failure-log.patch'

if not patch.is_file():
    print(f'{patch} not found; nothing to do')
    sys.exit(0)

text = patch.read_text()
marker = '+@@ -10119,4 +10119,6 @@'

if marker in text:
    print('startup-failure-log patch already carries the #138 fix')
    sys.exit(0)

if '@@ -10118,6 +10118,8 @@' not in text:
    print('unexpected startup-failure-log patch shape; leaving it unchanged')
    sys.exit(0)

# 去掉 macOS-only 的 #else / #endif 上下文，重锚到共享调用
fixed = text.replace(
    '@@ -10118,6 +10118,8 @@\n #else\n \tint data_error = native_owner_data_prepare(p, (user_addr_t)scratch_addr);\n #endif\n',
    '@@ -10119,4 +10119,6 @@\n \tint data_error = native_owner_data_prepare(p, (user_addr_t)scratch_addr);\n',
)

if fixed == text:
    print('context lines did not match the expected layout; leaving it unchanged')
    sys.exit(0)

patch.write_text(fixed)
print(f'applied issue #138 context fix to {patch.relative_to(root)}')
