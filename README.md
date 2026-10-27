<div align="center">

# StreamX downloads

Official APKs for [StreamX](https://github.com/StreamXProject/StreamX), its plugins and skins,
and the optional Automix engine.

[Website](https://streamxproject.github.io/StreamX-Releases/) ·
[Latest app](https://github.com/StreamXProject/StreamX-Releases/releases/latest) ·
[All releases](https://github.com/StreamXProject/StreamX-Releases/releases) ·
[Source](https://github.com/StreamXProject/StreamX)

</div>

## Install

Download `StreamX.apk` from the [latest release](https://github.com/StreamXProject/StreamX-Releases/releases/latest)
and open it on your phone. It runs on ARM64 devices with Android 8.0 or later.
After that, StreamX offers updates itself.

Plugins and skins install from inside the app, under **Settings → Sources**.
The Advanced Automix engine is a separate download, offered in Settings.

To check a download, compare it with the release's `SHA256SUMS.txt`:

```sh
sha256sum -c SHA256SUMS.txt --ignore-missing
```

## What is published here

| Release | Tag | Contents |
| --- | --- | --- |
| App | `v1.8`, `v1.8-preview.…` | `StreamX.apk`, per-architecture APKs, `SHA256SUMS.txt` |
| Plugins and skins | `extensions-v…` | One APK per extension, `SHA256SUMS.txt` |
| Automix engine | `automix-N` | One ZIP per architecture, a manifest, `SHA256SUMS.txt` |

Only app releases are marked latest. Extension and Automix releases never
appear as app updates.

## Source

| Repository | Visibility | What it holds |
| --- | --- | --- |
| [StreamX](https://github.com/StreamXProject/StreamX) | Public, GPL-3.0 | The app |
| [Skins](https://github.com/StreamXProject/Skins) | Public, GPL-3.0 | Skins |
| Plugins | Private | Plugins; publishes the extension APKs mirrored here |
| StreamX-Releases | Public | This website and the published binaries |

## For maintainers

**Website.** GitHub Pages serves `docs/` from `main`. Release details come from
GitHub's public API, and plain download links work without JavaScript. Preview
locally with:

```sh
python3 -m http.server 8000 --directory docs
```

**Skin gallery.** `docs/skins.json` drives the eight interactive Home, Library
and Player previews. They are HTML and CSS layouts, not screenshots, with
colours taken from each skin's `skin.json` in the Skins repository. Update it
when a skin release changes how a skin looks.

**Extension manifest.** The app and the website both read
[`extensions/index.json`](https://streamxproject.github.io/StreamX-Releases/extensions/index.json),
which lists plugins and skins together. Every `apkUrl` points at an asset in
this repository, so nobody needs a GitHub account or token to install. The
Plugins repository's publish workflow mirrors only verified, signed APKs and
the manifest; no publishing credential reaches this repository or its visitors.
