# unixnu-build2

Build workspace for **sheng** (Xiaomi Pad 6S Pro), iPadOS 27, **persistent boot**.

Follows the official flow from unixnu.com: `scripts/package.sh` (`unixnu release`).

Differences from a plain upstream build, all required:

| Change | Why |
|---|---|
| `patches/0065-ios-read-pages-and-mapped-writable.patch` applied to the AdrenoMetal bridge | `metal2vulkan-runtime` declares `read_pages`/`mapped_writable` only under `target_os="macos"`; ios27 fails with `E0425` |
| `--kernel-arg uefi-watchdog=1` | The firmware (`SHENG_BOOT_GUARD`) arms a 30 s Gunyah watchdog; without the kernel taking it over the device resets ~30 s after handoff, so the image could only be run with `fastboot boot` |
| `--init-data` | First installation: build the Data seed |
| boot.img size check against 192 MiB `boot_b` | `fastboot flash boot_b` requires it to fit |

Required secret: `UNIXNU_UNIQUE_CHIP_ID` (8 hex digits, platform seed).

Dispatch **build sheng iPadOS 27 (persistent boot, latest fixes)**.
