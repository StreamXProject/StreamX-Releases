<div align="center">

# StreamX downloads

APKs for [StreamX](https://github.com/StreamXProject/StreamX), its plugins and skins.

[Website](https://streamxproject.github.io/StreamX-Releases/) ·
[Latest app](https://github.com/StreamXProject/StreamX-Releases/releases/latest) ·
[Source](https://github.com/StreamXProject/StreamX)

</div>

## Install

Download `StreamX.apk` from the [latest release](https://github.com/StreamXProject/StreamX-Releases/releases/latest). Requires an ARM64 device with Android 8.0 or later.

Plugins and skins are installed from **Settings → Sources** in the app.

Each release includes `SHA256SUMS.txt`:

```sh
sha256sum -c SHA256SUMS.txt --ignore-missing
```

## Releases

| Tag | Contents |
| --- | --- |
| `v…` | App |
| `extensions-v…` | Plugins and skins |
| `automix-N` | Automix engine |

## Website

The site in `docs/` is served by GitHub Pages. To preview it locally:

```sh
python3 -m http.server 8000 --directory docs
```

The extension list is at [`extensions/index.json`](https://streamxproject.github.io/StreamX-Releases/extensions/index.json).

Screenshots for the hero and the skins tour go in `docs/assets/screens/` (file names are in the README there). A skin joins the picker once `skins/<id>/home.webp` exists. Plugin and skin logos in `docs/assets/logos/` are converted from the Android vector drawables with `scripts/vector-to-svg.py <drawable.xml> <out.svg>`.
