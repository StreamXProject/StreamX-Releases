# StreamX downloads

Official Android APKs and optional Advanced Automix engine/model packages.

- **[Download website](https://streamxproject.github.io/StreamX-Releases/)**
- **[App releases and checksums](https://github.com/StreamXProject/StreamX-Releases/releases)**
- **[Advanced Automix package 1](https://github.com/StreamXProject/StreamX-Releases/releases/tag/automix-1)**

The main APK download targets ARM64 devices running Android 8.0 or later. Other architectures are offered when available. Advanced Automix is installed from Settings in supported app builds; it is distributed separately from the APK.

This repository contains the public download website and intentionally published binaries. App source is intended to be public in `StreamXProject/StreamX`; its visibility migration is pending separation of historical plugin code. Plugin implementations stay private in `StreamXProject/Plugins`. Skins are public in `StreamXProject/Skins`.

## Website

GitHub Pages serves `docs/` from `main`. Release details are read from GitHub's public API; ordinary download links also work without JavaScript or API access. To preview locally, run `python3 -m http.server 8000 --directory docs`.

App versions use `v1.8` or `v1.8-preview.…` tags. Model packages use `automix-N` tags and must never be marked as the latest app release. Stable app releases include `StreamX.apk`, architecture-specific APKs and `SHA256SUMS.txt`. Automix releases include a checksum manifest, one ZIP per supported architecture and `SHA256SUMS.txt`.

## Skin gallery

The website includes eight released skins with interactive Home, Library and Player previews in light and dark mode. These are illustrative HTML/CSS layouts, not Android screenshots. Colours and layout settings in `docs/skins.json` come from the public skin manifests. Each skin links to its matching public APK and its existing public skin source directory. Current APK links come from the shared public manifest; bundled links are fallbacks.

Update `skins.json` when skin releases change; keep APK links on `github.com/StreamXProject/Skins/releases/download/`. Source manifests live in `StreamXProject/Skins/extensions/skins/<id>/app/src/main/assets/streamx/skin.json`.

## Shared extension manifest

Public URL: https://streamxproject.github.io/StreamX-Releases/extensions/index.json

This v1 manifest serves **plugins and skins together**. Each `apkUrl` points to a public release asset in this repository, so visitors and app users need no GitHub account or token. The `extensions-v…` releases are separate from app releases and never become the latest app update.

The plugin/skin source and signing configuration remain private in `StreamXProject/Plugins`. Its publishing service mirrors only verified APKs, checksums and the public manifest. The website loads the same manifest to show plugin downloads, all available skins and current gallery download links. No publisher credential is sent to visitors.
