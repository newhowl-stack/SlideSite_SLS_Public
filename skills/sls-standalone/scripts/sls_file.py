#!/usr/bin/env python3
"""Scoped, byte-preserving SLS data edits. Does not execute the input file."""
import argparse, hashlib, html, json, re
from html.parser import HTMLParser
from pathlib import Path

class Document(HTMLParser):
    def __init__(self, raw):
        super().__init__(convert_charrefs=False)
        self.raw=raw; self.lines=raw.splitlines(keepends=True); self.scripts=[]; self.active=None
        self.feed(raw)
    def source_offset(self):
        line,col=self.getpos(); return sum(map(len,self.lines[:line-1]))+col
    def handle_starttag(self,tag,attrs):
        if tag=='script':
            a=dict(attrs); self.active=(a,self.source_offset()+len(self.get_starttag_text()))
    def handle_endtag(self,tag):
        if tag=='script' and self.active:
            a,start=self.active; self.scripts.append((a,start,self.source_offset())); self.active=None
    def payload(self):
        matches=[(a,b,c) for a,b,c in self.scripts if a.get('id')=='deck-source' and a.get('type')=='application/json']
        if len(matches)!=1: raise ValueError('Expected exactly one real deck-source JSON element')
        _,b,c=matches[0]; return b,c,json.loads(self.raw[b:c])
    def runtime(self):
        return {a.get('id',str(i)):hashlib.sha256(self.raw[b:c].encode()).hexdigest() for i,(a,b,c) in enumerate(self.scripts) if a.get('type')!='application/json'}

def read(path):
    return Document(Path(path).read_bytes().decode('utf-8'))

def validate(m):
    if m.get('format')!='SLS' or m.get('schema_version')!='presentation-studio/2': raise ValueError('Unsupported SLS schema')
    if not isinstance(m.get('slides'),list) or not m['slides']: raise ValueError('At least one slide is required')
    ids=[m.get('deck_id')]
    for s in m['slides']:
        ids.append(s.get('id'))
        for o in s.get('objects',[]):
            ids.append(o.get('id'))
            if o.get('type')=='image' and o.get('asset') and o.get('asset') not in m.get('assets',{}): raise ValueError('Missing image asset')
    if not all(isinstance(i,str) and i for i in ids) or len(set(ids))!=len(ids): raise ValueError('Missing or duplicate IDs')
    for key in ['canvas','theme','assets','font_faces','sls_structure','editor_version','format_version']:
        if key not in m: raise ValueError('Missing required field: '+key)

def plain(s): return html.unescape(re.sub('<[^>]*>',' ',str(s)))
def outline(m,offset=0,limit=25):
    return {'title':m.get('title'),'slides':[{'id':s['id'],'name':s.get('name'),'objects':len(s.get('objects',[]))} for s in m['slides'][offset:offset+limit]],'nextOffset':offset+limit if offset+limit<len(m['slides']) else None}

def write(source,model,dest):
    d=read(source); b,c,old=d.payload(); validate(model)
    if model['editor_version']!=old['editor_version'] or model['format_version']!=old['format_version']: raise ValueError('Do not upgrade editor/format during a data edit')
    raw=d.raw[:b]+json.dumps(model,ensure_ascii=False,separators=(',',':')).replace('<','\\u003c')+d.raw[c:]
    # Cached summaries are explicitly stale until native export regenerates the index.
    idx=outline(model); idx.update({'schema':'sls-agent-index/1','stale':True,'note':'Raw-file edit: navigate with this bounded index, read exact deck-source targets; native export refreshes summaries.'})
    raw=re.sub(r'<!-- SLS_AGENT_INDEX\b[\s\S]*?END_SLS_AGENT_INDEX -->',lambda _: '<!-- SLS_AGENT_INDEX\n'+json.dumps(idx,ensure_ascii=True).replace('--','\\u002d\\u002d')+'\nEND_SLS_AGENT_INDEX -->',raw,count=1)
    raw=re.sub(r'<title>[\s\S]*?</title>',lambda _: '<title>'+html.escape(str(model.get('title','Presentation')))+' — SlideSite</title>',raw,count=1)
    new=Document(raw)
    if d.runtime()!=new.runtime(): raise ValueError('Runtime bytes changed')
    def csp(t): return re.findall(r'<meta[^>]+http-equiv="Content-Security-Policy"[^>]*>',t,re.I)
    if csp(d.raw)!=csp(raw): raise ValueError('CSP changed')
    validate(new.payload()[2]); Path(dest).parent.mkdir(parents=True,exist_ok=True); Path(dest).write_bytes(raw.encode())

def diffs(a,b,p=''):
    if type(a)!=type(b): return [p]
    if isinstance(a,dict): return [q for k in sorted(a.keys()|b.keys()) for q in ([p+'/'+k] if k not in a or k not in b else diffs(a[k],b[k],p+'/'+k))]
    if isinstance(a,list):
        if len(a)!=len(b): return [p]
        return [q for i,(x,y) in enumerate(zip(a,b)) for q in diffs(x,y,p+'/'+str(i))]
    return [] if a==b else [p]

def main():
    p=argparse.ArgumentParser(); sub=p.add_subparsers(dest='cmd',required=True)
    for name in ['outline','inspect']:
        x=sub.add_parser(name);x.add_argument('file');x.add_argument('--slide');x.add_argument('--object');x.add_argument('--offset',type=int,default=0);x.add_argument('--limit',type=int,default=25)
    x=sub.add_parser('write');x.add_argument('file');x.add_argument('model');x.add_argument('output')
    x=sub.add_parser('compare');x.add_argument('file');x.add_argument('after')
    x=sub.add_parser('size-report');x.add_argument('file');x.add_argument('--baseline')
    a=p.parse_args(); d=read(a.file)
    if a.cmd=='size-report':
        from size_report import report
        baseline=json.loads(Path(a.baseline).read_text()) if a.baseline else None
        print(json.dumps(report(d,baseline),indent=2));return
    m=d.payload()[2];validate(m)
    if a.cmd=='write': write(a.file,json.loads(Path(a.model).read_text()),a.output); result={'written':a.output,'runtimeUnchanged':True}
    elif a.cmd=='compare':
        n=read(a.after);result={'runtimeUnchanged':d.runtime()==n.runtime(),'changedPaths':diffs(m,n.payload()[2])}
    elif a.cmd=='outline': result=outline(m,max(0,a.offset),min(25,max(1,a.limit)))
    else:
        slides=[s for s in m['slides'] if s['id']==a.slide] if a.slide else m['slides']
        if a.object:
            matches=[o for s in slides for o in s.get('objects',[]) if o['id']==a.object]
            if len(matches)!=1: raise ValueError('Target not unique')
            o=matches[0]; content=str(o.get('html','')); result={k:o[k] for k in ['id','type','role','x','y','w','h','size','family','color','weight','style_bindings'] if k in o};result.update({'html':content[a.offset:a.offset+4000],'nextOffset':a.offset+4000 if a.offset+4000<len(content) else None})
        else:
            if len(slides)!=1: raise ValueError('Select one slide or object')
            s=slides[0];result={'id':s['id'],'name':s.get('name'),'objects':[{'id':o['id'],'type':o.get('type'),'role':o.get('role')} for o in s.get('objects',[])[a.offset:a.offset+25]],'nextOffset':a.offset+25 if a.offset+25<len(s.get('objects',[])) else None}
    print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__': main()

