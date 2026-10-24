"""Read-only live verification of prospect / source pages (GET only, no forms).
Usage: python3 verify_pages.py <urls.txt> <out.json>
For each URL: HTTP status, final URL, <title>, outbound links to tracked competitor domains
(href, anchor, rel), any link to / text mention of House of Diams, and public mailto: addresses.
Uses curl (Python urllib fails TLS verification on this Mac, per project tooling notes)."""
import sys, json, subprocess, re, datetime
from html.parser import HTMLParser
from concurrent.futures import ThreadPoolExecutor
COMP = ['brilliantearth.com','bluenile.com','ritani.com','vrai.com','cleanorigin.com','withclarity.com','miadonna.com',
        'grownbrilliance.com','whiteflash.com','jamesallen.com','kay.com','zales.com','jared.com','tiffany.com','rarecarat.com',
        'diamondnexus.com','frankdarling.com','kinnstudio.com','catbirdnyc.com','mejuri.com','lightboxjewelry.com','stonealgo.com']
UA = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/129.0 Safari/537.36'
class P(HTMLParser):
    def __init__(s):
        super().__init__(); s.links=[]; s.cur=None; s.title=''; s.intitle=False
    def handle_starttag(s, t, a):
        a=dict(a)
        if t=='a' and a.get('href'): s.cur={'href':a['href'],'rel':a.get('rel') or '','text':''}
        if t=='title': s.intitle=True
    def handle_endtag(s, t):
        if t=='a' and s.cur: s.cur['text']=re.sub(r'\s+',' ',s.cur['text']).strip()[:120]; s.links.append(s.cur); s.cur=None
        if t=='title': s.intitle=False
    def handle_data(s, d):
        if s.cur is not None: s.cur['text']+=d
        if s.intitle and not s.title.strip(): s.title=d.strip()
def check(url):
    out={'url':url,'checked_utc':datetime.datetime.now(datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')}
    try:
        r=subprocess.run(['curl','-sL','--max-time','30','-A',UA,'-H','Accept-Language: en-US,en;q=0.9','-w','\n__META__%{http_code} %{url_effective}',url],capture_output=True,timeout=40)
        body=r.stdout.decode('utf-8','replace'); body,_,meta=body.rpartition('\n__META__')
        code,_,final=meta.partition(' ')
        out.update(status=int(code or 0), final_url=final)
        p=P()
        try: p.feed(body)
        except Exception: pass
        out['title']=p.title[:200]
        comp=[]
        for l in p.links:
            h=l['href'].lower()
            for c in COMP:
                if re.search(r'(^|//|\.)'+re.escape(c), h): comp.append({'domain':c,'href':l['href'][:250],'anchor':l['text'],'rel':l['rel']})
        out['competitor_links']=comp
        out['competitor_domains']=sorted({c['domain'] for c in comp})
        out['hod_link']=[l['href'] for l in p.links if 'houseofdiams' in l['href'].lower()][:5]
        out['hod_text_mention']=bool(re.search(r'house\s+of\s+diams', body, re.I))
        out['mailto']=sorted({l['href'][7:].split('?')[0] for l in p.links if l['href'].lower().startswith('mailto:')})[:10]
        out['bytes']=len(body)
        low=body.lower()
        out['signals']=[k for k in ['write for us','contribute','submission','submit','advertis','sponsored','affiliate','press','contact','pitch','guest post','media kit'] if k in low]
    except Exception as e:
        out['error']=str(e)[:200]
    return out
urls=[u.strip() for u in open(sys.argv[1]) if u.strip() and not u.startswith('#')]
with ThreadPoolExecutor(6) as ex: res=list(ex.map(check, urls))
json.dump(res, open(sys.argv[2],'w'), indent=1)
for x in res:
    print(x.get('status'), len(x.get('competitor_links',[])), ','.join(x.get('competitor_domains',[]))[:70], 'HOD' if x.get('hod_link') else '-', '|', (x.get('title') or x.get('error',''))[:60], '|', x['url'][:90])
