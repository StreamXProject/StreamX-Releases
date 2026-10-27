# StreamX downloads

Official Android APKs and optional Advanced Automix engine/model packages.

- **[Download website](https://streamxproject.github.io/StreamX-Releases/)**
- **[App releases and checksums](https://github.com/StreamXProject/StreamX-Releases/releases)**
- **[Advanced Automix package 1](https://github.com/StreamXProject/StreamX-Releases/releases/tag/automix-1)**

The main APK download targets ARM64 devices running Android 8.0 or later. Other architectures are offered when available. Advanced Automix is installed from Settings in supported app builds; it is distributed separately from the APK.

This repository contains the public download website and intentionally published binaries. App development and build configuration are maintained separately.

## Website

GitHub Pages serves `docs/` from `main`. Release details are read from GitHub's public API; ordinary download links also work without JavaScript or API access. To preview locally, run `python3 -m http.server 8000 --directory docs`.

App versions use `v1.8` or `v1.8-preview.…` tags. Model packages use `automix-N` tags and must never be marked as the latest app release. Stable app releases include `StreamX.apk`, architecture-specific APKs and `SHA256SUMS.txt`. Automix releases include a checksum manifest, one ZIP per supported architecture and `SHA256SUMS.txt`.
