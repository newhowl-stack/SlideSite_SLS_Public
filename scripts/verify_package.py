"""Verify the final downloaded distribution; no AI-consumer acceptance is implied."""
from pathlib import Path
import hashlib, json, sys, zipfile, re, posixpath
ROOT = Path(__file__).resolve().parents[1]
p = Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'downloads/SlideSite_Starter.zip'
sha = lambda b: hashlib.sha256(b).hexdigest()
checksums = {line.split()[1]:line.split()[0] for line in (ROOT/'downloads/SHA256SUMS').read_text().splitlines() if line.strip()}
assert sha(p.read_bytes()) == checksums[p.name], 'ZIP SHA256 mismatch'
with zipfile.ZipFile(p) as z:
 assert z.testzip() is None
 names=z.namelist()
 assert len(names)==len(set(names)) and sum(i.file_size for i in z.infolist())<5_000_000
 assert all(not n.startswith('/') and '..' not in Path(n).parts for n in names)
 manifest=json.loads(z.read('manifest.json'))
 assert set(names)==set(manifest['files'])|{'manifest.json','PACKAGE_MANIFEST.json'}
 for name,digest in manifest['files'].items(): assert sha(z.read(name))==digest,name
 inventory=json.loads(z.read('PACKAGE_MANIFEST.json'))['files']
 assert set(inventory)==set(names)-{'PACKAGE_MANIFEST.json'}
 for name,info in inventory.items():
  b=z.read(name);assert len(b)==info['bytes'] and sha(b)==info['sha256'],name
 assert z.read('starter.html')==(ROOT/'starter.html').read_bytes()
 assert len(z.read('starter.html'))==1644069
 assert sha(z.read('starter.html'))=='e1352267beeeca5d2a5dd18960caf847701295744be3250462b428d4f7920c22'
 for name in ['LICENSE','LICENSING.md','THIRD_PARTY_NOTICES.md']: assert len(z.read(name))>500
 for name in names:
  if name.endswith('.md'):
   for target in re.findall(r'\]\(([^)]+)\)',z.read(name).decode()):
    if '://' in target or target.startswith('#'): continue
    resolved=posixpath.normpath(posixpath.join(posixpath.dirname(name),target.split('#')[0]))
    assert resolved in names or resolved.startswith('docs/evidence/'),(name,target)
 for name in ['guides/CHATGPT.md','guides/CLAUDE.md']:
  assert b'SlideSite_Starter-1.27.0-guide.2.zip' in z.read(name)
  assert b'SlideSite_Starter-1.25.0' not in z.read(name)
print(json.dumps({'status':'PASS','bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),'members':len(names),'scope':'Archive, all member identities, rights-clean starter equality and documentation links; AI-consumer acceptance remains separate.'}))
