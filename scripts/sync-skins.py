"""Refresh public skin links without copying their APKs or artwork."""
import argparse
import base64
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import urlparse

SIGNER = 'f0d96c1f8f886ba0c4049fdfeaddf3f945e06ac5c623f734f7a88d28edff10f2'
CATALOGUE = 'docs/extensions/index.json'
REPO = 'StreamXProject/StreamX-Releases'


def merge(current, source):
    if current.get('schemaVersion') != 1 or source.get('schemaVersion') != 1:
        raise ValueError('Unsupported catalogue schema')
    skins = source['extensions']
    if not 1 <= len(skins) <= 500:
        raise ValueError('Invalid skin count')
    for entry in skins:
        url = urlparse(entry['apkUrl'])
        if (entry['type'] != 'skin' or not entry['packageName'].startswith('com.music.streamx.skins.')
                or entry['certificateSha256'] != SIGNER or entry['versionCode'] <= 0
                or not re.fullmatch(r'[a-f0-9]{64}', entry['sha256'])
                or not 0 < entry['size'] <= 200 * 1024 * 1024
                or url.scheme != 'https' or url.netloc != 'github.com' or url.query or url.fragment
                or not url.path.startswith('/StreamXProject/Skins/releases/download/') or not url.path.endswith('.apk')):
            raise ValueError('Untrusted skin release')
        if entry.get('iconUrl'):
            icon = urlparse(entry['iconUrl'])
            if (icon.scheme != 'https' or icon.netloc != 'github.com' or icon.query or icon.fragment
                    or icon.path.rsplit('/', 1)[0] != url.path.rsplit('/', 1)[0]
                    or not icon.path.endswith('.svg')):
                raise ValueError('Untrusted skin artwork')
    existing = [e for e in current['extensions'] if e['type'] == 'skin']
    versions = {e['packageName']: e['versionCode'] for e in skins}
    if any(versions.get(e['packageName'], -1) < e['versionCode'] for e in existing):
        raise ValueError('Refusing to remove or downgrade an existing skin')
    return {**current, 'extensions': [e for e in current['extensions'] if e['type'] != 'skin'] + skins}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('source')
    parser.add_argument('--local', action='store_true')
    args = parser.parse_args()
    source = json.loads(Path(args.source).read_text())
    if args.local:
        path = Path(CATALOGUE)
        path.write_text(json.dumps(merge(json.loads(path.read_text()), source), indent=2) + '\n')
        return
    # Read the latest file for every attempt, retaining plugin updates that race this job.
    for attempt in range(3):
        remote = json.loads(subprocess.check_output(['gh', 'api', f'repos/{REPO}/contents/{CATALOGUE}']))
        current = json.loads(base64.b64decode(remote['content']))
        updated = merge(current, source)
        if current == updated:
            print('Skin links already current')
            return
        payload = {'message': 'Refresh direct Skins release links', 'branch': 'main', 'sha': remote['sha'],
                   'content': base64.b64encode((json.dumps(updated, indent=2) + '\n').encode()).decode()}
        result = subprocess.run(['gh', 'api', '--method', 'PUT', f'repos/{REPO}/contents/{CATALOGUE}', '--input', '-'],
                                input=json.dumps(payload), text=True, capture_output=True)
        if result.returncode == 0:
            # Commits made by GITHUB_TOKEN do not start a Pages build automatically.
            subprocess.run(['gh', 'api', '--method', 'POST', f'repos/{REPO}/pages/builds'], check=True, capture_output=True)
            print('Updated direct skin links and requested Pages deployment')
            return
        if '409' not in result.stderr or attempt == 2:
            raise RuntimeError(result.stderr)


if __name__ == '__main__':
    main()
