"""Non-executing, non-overlapping UTF-8 size accounting for SLS HTML."""
import base64,hashlib,re
from urllib.parse import unquote_to_bytes
DATA=re.compile(r'data:([^,\s"\x27<>`]*),([^\s"\x27<>`\\)]*)')
def report(doc,baseline=None):
    raw=doc.raw; b,c,_=doc.payload()
    regions=[(b,c,'deckJson')]+[(s,e,'runtime') for a,s,e in doc.scripts if a.get('id')!='deck-source']
    totals={'deckJson':0,'runtime':0,'otherHtml':0,'fonts':0,'images':0,'otherAssets':0}
    assets=[];seen={};warnings=[]
    matches=list(DATA.finditer(raw))
    def category(pos):
        return next((k for s,e,k in regions if s<=pos<e),'otherHtml')
    for s,e,k in regions:totals[k]+=len(raw[s:e].encode())
    totals['otherHtml']=len(raw.encode())-totals['deckJson']-totals['runtime']
    for m in matches:
        mime=m[1].split(';')[0].lower();kind='fonts' if ('font' in mime or 'woff' in mime) else 'images' if mime.startswith('image/') else 'otherAssets'
        encoded=len(m[0].encode());container=category(m.start());totals[container]-=encoded;totals[kind]+=encoded
        try:
            data=base64.b64decode(m[2],validate=True) if ';base64' in m[1] else unquote_to_bytes(m[2])
            digest=hashlib.sha256(data).hexdigest();decoded=len(data)
            seen.setdefault(digest,[]).append(len(assets))
        except Exception:decoded=None;digest=None;warnings.append('Could not decode embedded asset at character '+str(m.start()))
        assets.append({'kind':kind,'container':container,'embeddedTextBytes':encoded,'decodedBytes':decoded,'sha256':digest})
    duplicates=[{'sha256':h,'occurrences':len(v),'duplicatedDecodedBytes':sum(assets[i]['decodedBytes'] for i in v[1:])} for h,v in seen.items() if len(v)>1]
    if duplicates:warnings.append('Repeated embedded assets detected; inspect whether duplication is intentional.')
    total=len(raw.encode());assert sum(totals.values())==total
    if baseline:
        expected=baseline.get('approvedStarterBytes');allowance=baseline.get('growthAllowanceBytes',0)
        if expected and total>expected+allowance:warnings.append('Above approved starter budget; explain growth. User decks are not rejected.')
    return {'totalHtmlBytes':total,'exclusiveEmbeddedTextBytes':totals,'runtimeIncludesNonDeckScriptData':True,'assets':assets,'duplicateAssets':duplicates,'warnings':warnings,'budgetStatus':'pending-optimized-starter' if not baseline or not baseline.get('approvedStarterBytes') else 'measured','note':'Exclusive categories sum to total. Data URIs inside script bodies are deducted from runtime. Decoded bytes are informational and are not added to HTML bytes. Escaped/dynamically constructed non-data-URI assets are not decoded.'}

