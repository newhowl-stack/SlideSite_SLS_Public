"""Rebuild the public starter bundle without modifying its canonical editor."""
from pathlib import Path
import hashlib,json,zipfile
ROOT=Path(__file__).resolve().parents[1]
CANONICAL='bbaa0ce7c29e306a54bf35962a1ebf15381689b13982502761eb24105e208d36'
def sha(b): return hashlib.sha256(b).hexdigest()
assert sha((ROOT/'starter.html').read_bytes())==CANONICAL,'Canonical source mismatch: stop and review the release pin.'
paths=sorted(p for p in ROOT.rglob('*') if p.is_file() and '.git' not in p.parts and p.relative_to(ROOT).parts[0] not in ('downloads','scripts','docs') and p.name!='manifest.json')
m=json.loads((ROOT/'manifest.json').read_text());m['packageVersion']='1.25.0-guide.1';m['files']={str(p.relative_to(ROOT)):sha(p.read_bytes()) for p in paths}
(ROOT/'manifest.json').write_text(json.dumps(m,indent=2)+'\n')
paths.append(ROOT/'manifest.json')
zip_path=ROOT/'downloads/SlideSite_Starter-1.25.0-guide.1.zip'
with zipfile.ZipFile(zip_path,'w',zipfile.ZIP_DEFLATED,compresslevel=9) as z:
 for p in sorted(paths):
  info=zipfile.ZipInfo(str(p.relative_to(ROOT)),(2026,11,3,0,0,0));info.compress_type=zipfile.ZIP_DEFLATED;info.external_attr=0o100644<<16
  z.writestr(info,p.read_bytes(),compresslevel=9)
(ROOT/'downloads/SlideSite_Starter.zip').write_bytes(zip_path.read_bytes())
(ROOT/'downloads/SHA256SUMS').write_text(''.join(sha(zip_path.read_bytes())+'  '+name+'\n' for name in ['SlideSite_Starter-1.25.0-guide.1.zip','SlideSite_Starter.zip']))
print(json.dumps({'zipBytes':zip_path.stat().st_size,'zipSha256':sha(zip_path.read_bytes()),'members':len(paths),'canonicalSha256':CANONICAL}))
