import copy
import importlib.util
from pathlib import Path
import unittest

spec = importlib.util.spec_from_file_location('sync', Path(__file__).with_name('sync-skins.py'))
sync = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sync)

class MergeTests(unittest.TestCase):
    def setUp(self):
        self.skin = dict(type='skin', packageName='com.music.streamx.skins.demo', versionCode=2,
                         certificateSha256=sync.SIGNER, sha256='a'*64, size=100,
                         apkUrl='https://github.com/StreamXProject/Skins/releases/download/v1/demo.apk',
                         iconUrl='https://github.com/StreamXProject/Skins/releases/download/v1/icon.svg')
        self.plugin = dict(type='plugin', packageName='com.music.streamx.plugin', versionCode=5)
        self.current = dict(schemaVersion=1, extensions=[self.plugin, {**self.skin, 'versionCode':1}])
        self.source = dict(schemaVersion=1, extensions=[self.skin])
    def test_preserves_plugins_and_uses_direct_skin_links(self):
        result=sync.merge(self.current,self.source)
        self.assertEqual([self.plugin,self.skin],result['extensions'])
    def test_rejects_downgrade_or_removal(self):
        for entries in ([],[{**self.skin,'versionCode':0}]):
            with self.assertRaises(ValueError):sync.merge(self.current,dict(schemaVersion=1,extensions=entries))
    def test_rejects_foreign_apks_artwork_and_signers(self):
        for field,value in [('apkUrl','https://example.com/demo.apk'),('iconUrl','https://example.com/logo.svg'),('certificateSha256','b'*64)]:
            source=copy.deepcopy(self.source);source['extensions'][0][field]=value
            with self.assertRaises(ValueError):sync.merge(self.current,source)
if __name__=='__main__':unittest.main()
