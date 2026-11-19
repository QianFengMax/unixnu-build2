# unixnu-build2

Build workspace for **sheng** (Xiaomi Pad 6S Pro) iPadOS 27 images.

Replicates the configuration that produced `images-27` successfully on
2026-11-19: `scripts/package.sh` (i.e. `unixnu release`) with the UniXNU core
pinned to `563595ab`, which is the verified combination.

Dispatch **build sheng iPadOS 27 (verified path, images to Release)** from the
Actions tab.

Required secret: `UNIXNU_UNIQUE_CHIP_ID` (8 hex digits, platform seed).
