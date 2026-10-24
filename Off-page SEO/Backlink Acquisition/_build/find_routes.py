"""Read-only scan of a site's homepage for public contact / submission / press / membership routes.
Usage: python3 find_routes.py <domains.txt> <out.json>. GET only; records links found, never guesses addresses."""
import sys, json, subprocess, re, datetime
from html.parser import HTMLParser
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor
UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36'
KW=re.compile(r'contact|submi|write for|contribut|press|media|editorial|advertis|partner|vendor|member|join|list your|pitch|tips|about|pro\b|for business|wholesale|directory|find a', re.I)
class P(HTMLParser):
    def __init__(s): super().__init__(); s.links=[]; s.cur=None; s.title=''; s.t=False
    def handle_starttag(s,t,a):
        a=dict(a)
        if t=='a' and a.get('href'): s.cur=[a['href'],'']
        if t=='title': s.t=True
    def handle_endtag(s,t):
        if t=='a' and s.cur: s.links.append((s.cur[0], re.sub(r'\s+',' ',s.cur[1]).strip()[:80])); s.cur=None
        if t=='title': s.t=False
    def handle_data(s,d):
        if s.cur is not None: s.cur[1]+=d
        if s.t and not s.title.strip(): s.title=d.strip()
def scan(url):
    o={'url':url,'checked_utc':datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')}
    try:
        r=subprocess.run(['curl','-sL','--max-time','30','-A',UA,'-w','\n__META__%{http_code} %{url_effective}',url],capture_output=True,timeout=40)
        b=r.stdout.decode('utf-8','replace'); b,_,m=b.rpartition('\n__META__'); c,_,f=m.partition(' ')
        o.update(status=int(c or 0), final_url=f)
        p=P()
        try: p.feed(b)
        except Exception: pass
        o['title']=p.title[:150]
        seen=set(); routes=[]
        for h,t in p.links:
            if h.lower().startswith('mailto:'):
                e=h[7:].split('?')[0]
                if e not in seen: seen.add(e); routes.append({'type':'mailto','value':e,'text':t})
            elif KW.search(h) or KW.search(t):
                full=urljoin(f or url,h)
                if full not in seen and full.startswith('http'): seen.add(full); routes.append({'type':'link','value':full,'text':t})
        o['routes']=routes[:40]
    except Exception as e: o['error']=str(e)[:200]
    return o
urls=[u.strip() for u in open(sys.argv[1]) if u.strip() and not u.startswith('#')]
with ThreadPoolExecutor(6) as ex: res=list(ex.map(scan,urls))
json.dump(res,open(sys.argv[2],'w'),indent=1)
for x in res:
    print(x.get('status'), (x.get('title') or x.get('error',''))[:50],'|',x['url'])
    for r in x.get('routes',[])[:40]: print('    ',r['type'],r['value'][:110],'|',r['text'][:40])
