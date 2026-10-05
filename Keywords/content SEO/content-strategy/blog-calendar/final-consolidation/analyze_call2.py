import json,glob,csv,re
COMM=re.compile(r'shop|product|collection|/p/|/rings/|/products/|category|bracelets/|necklaces/|engagement-rings/|wedding-bands/|wedding-rings/|/jewelry/|catalog')
rows=[]
for f in sorted(glob.glob('dataforseo/raw/final_calendar/R2_serp/*.json')):
    d=json.load(open(f))
    if 'tasks' in d:
        r=d['tasks'][0]['result'][0]; items=r['items']
        it=r['item_types']; aio=[x for x in items if x['type']=='ai_overview']
        heads=[e.get('title') for a in aio for e in (a.get('items') or []) if e.get('title')]
        paa=[e['title'] for x in items if x['type']=='people_also_ask' for e in x['items']]
        org=[x for x in items if x['type']=='organic']
        rel=[s for x in items if x['type']=='related_searches' for s in x['items']]
        comm=sum(1 for x in org if COMM.search(x['url'].lower()))
        rows.append({'keyword':r['keyword'],'task_cost':d['tasks'][0]['cost'],'retrieval':'FULL_RAW','ai_overview':'PRESENT' if aio else 'ABSENT','aio_headings':' | '.join(heads),
            'paa_count':len(paa),'paa_questions':' | '.join(paa),'serp_features':';'.join(it),'organic_count':len(org),'commercial_like_urls':comm,
            'top_organic':' | '.join(f"{x['domain']}: {x['title'][:60]}" for x in org[:10]),'related_searches':' | '.join(rel)})
    else:
        rows.append({'keyword':d['keyword'],'task_cost':d['cost'],'retrieval':'CONDENSED','ai_overview':'PRESENT' if d['ai_overview'] else 'ABSENT','aio_headings':' | '.join(d.get('aio_section_headings',[])),
            'paa_count':len(d['paa']),'paa_questions':' | '.join(d['paa']),'serp_features':';'.join(d['item_types']),'organic_count':len(d['organic_top']),'commercial_like_urls':'n/a',
            'top_organic':' | '.join(d['organic_top']),'related_searches':' | '.join(d.get('related_searches',[])),'note':d.get('note','')})
f=['keyword','task_cost','retrieval','ai_overview','aio_headings','paa_count','paa_questions','serp_features','organic_count','commercial_like_urls','top_organic','related_searches','note']
w=csv.DictWriter(open('content-strategy/blog-calendar/final-consolidation/call2_serp_analysis.csv','w',newline=''),fieldnames=f);w.writeheader();w.writerows(rows)
print('total cost',round(sum(float(r['task_cost']) for r in rows),5))
for r in rows:
    if r['retrieval']=='FULL_RAW':
        print('\n==',r['keyword'],'| AIO',r['ai_overview'],'| comm',r['commercial_like_urls'],'/',r['organic_count'],'|',r['serp_features'])
        print('  H:',r['aio_headings'][:200]); print('  PAA:',r['paa_questions'][:400]); print('  TOP:',r['top_organic'][:700])
