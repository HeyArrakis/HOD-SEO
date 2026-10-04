import sys,os,re,importlib.util
spec=importlib.util.spec_from_file_location('a',os.path.join(os.path.dirname(os.path.abspath(__file__)),'analyze_round2.py'))
src=open(spec.origin).read().split('rows, paa_rows, urls')[0]
g={'__file__':spec.origin}; exec(src,g)
for m in g['manifest']:
    s=g['load'](m['tag'])
    print('='*6, m['tag'][-3:], m['keyword'], '| types:', ','.join(t for t in s['item_types'] if t!='organic'))
    for rg,d,u,t in s['organic'][:10]:
        print(f"   {rg:>2} {g['page_type'](u,d,t)[:14]:14} {(d or '')[:30]:30} {(t or '')[:70]}")
    h=re.findall(r'^#{2,4}\s*(.+)$', s['aio_md'], flags=re.M)
    lines=[l for l in re.sub(r'!\[[^\]]*\]\([^)]*\)','',s['aio_md']).split('\n') if l.strip() and not l.startswith('#')]
    lead=re.sub(r'\[\[\d+\]\]\([^)]*\)','',lines[0]) if lines else ''
    print('   AIO:', s['aio_present'], '| lead:', lead[:170])
    print('   AIO H:', ' | '.join(h[:7]))
    print('   PAA:', ' | '.join(q for q,_ in s['paa']))
    print('   REL:', ' | '.join(s['related'][:8]))
