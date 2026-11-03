"""Verify a downloaded bundle: python scripts/verify_package.py [path/to/ZIP]."""
from pathlib import Path
import hashlib,json,sys,zipfile,re
ROOT=Path(__file__).resolve().parents[1]
p=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'downloads/SlideSite_Starter.zip'
def sha(b): return hashlib.sha256(b).hexdigest()
expected=(ROOT/'downloads/SHA256SUMS').read_text().split()[0]
assert sha(p.read_bytes())==expected,'ZIP SHA256 differs from published checksum'
with zipfile.ZipFile(p) as z:
 assert z.testzip() is None,'Corrupt ZIP member'
 names=z.namelist();assert len(names)==len(set(names)),'Duplicate ZIP paths'
 assert all(not n.startswith('/') and '..' not in Path(n).parts for n in names),'Unsafe archive path'
 manifest=json.loads(z.read('manifest.json'))
 assert set(names)==set(manifest['files'])|{'manifest.json'},'Unexpected or missing ZIP members'
 for name,digest in manifest['files'].items():
  assert sha(z.read(name))==digest,f'Checksum mismatch: {name}'
 assert z.read('starter.html')==(ROOT/'starter.html').read_bytes(),'Starter differs from repository'
 assert len(z.read('starter.html'))==2125306,'Canonical size drift'
 assert sha(z.read('starter.html'))=='bbaa0ce7c29e306a54bf35962a1ebf15381689b13982502761eb24105e208d36','Canonical hash drift'
 for name in names:
  if name.endswith('.md'):
   for target in re.findall(r'\]\(([^)]+)\)',z.read(name).decode()):
    if '://' in target or target.startswith('#'): continue
    import posixpath
    resolved=posixpath.normpath(posixpath.join(posixpath.dirname(name),target.split('#')[0]))
    # Evidence lives in the repository, not inside the instruction bundle.
    assert resolved in names or resolved.startswith('docs/evidence/'),f'Broken local link in {name}: {target}'
print(json.dumps({'status':'PASS','bytes':p.stat().st_size,'sha256':sha(p.read_bytes()),'members':len(names),'scope':'archive, member checksums, canonical equality and documentation links; not rendering or AI acceptance'}))
