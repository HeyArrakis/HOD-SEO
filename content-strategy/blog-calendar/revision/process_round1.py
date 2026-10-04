import json,glob,csv,re
S15={r['normalized_keyword']:r for r in csv.DictReader(open('architecture/15_keyword_url_map.csv'))}
C1={r['keyword']:r for r in csv.DictReader(open('content-strategy/blog-calendar/working/call1_processed.csv'))}
M=[(2025,9),(2025,10),(2025,11),(2025,12),(2026,1),(2026,2),(2026,3),(2026,4),(2026,5),(2026,6),(2026,7),(2026,8)]
MON=['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
rows={}
for f in sorted(glob.glob('dataforseo/raw/blog_calendar/revision/R1_*.json')):
    call=f.split('/')[-1].split('_')[1]
    r=json.load(open(f))['tasks'][0]['result'][0]
    items=list(r['items'])
    if r.get('seed_keyword_data'): items.append(r['seed_keyword_data'])
    for it in items:
        k=it['keyword'].lower().strip(); ki=it.get('keyword_info') or {}
        if k in rows: rows[k]['source_calls']+=';'+call; continue
        ms={(m['year'],m['month']):m['search_volume'] for m in (ki.get('monthly_searches') or []) if m.get('search_volume') is not None}
        vals=[ms.get(x) for x in M if ms.get(x) is not None]; avg=sum(vals)/len(vals) if vals else None
        pk=max(((ms[x],x) for x in M if x in ms),default=(None,None))
        si=it.get('serp_info') or {}; types=si.get('serp_item_types') or []
        kp=it.get('keyword_properties') or {}; si2=it.get('search_intent_info') or {}
        rows[k]={'keyword':k,'search_volume':ki.get('search_volume'),'peak_month':f"{MON[pk[1][1]]} {pk[1][0]}" if pk[1] else '','peak_volume':pk[0],
          'nov_idx':round(ms.get((2025,11),0)/avg,2) if avg else '','dec_idx':round(ms.get((2025,12),0)/avg,2) if avg else '','feb_idx':round(ms.get((2026,2),0)/avg,2) if avg else '',
          'kd':kp.get('keyword_difficulty'),'cpc':ki.get('cpc'),'dfs_intent':si2.get('main_intent'),
          'serp_types':';'.join(types),'aio':'ai_overview' in types,'paa':'people_also_ask' in types,
          'product_led':any(t in types for t in ('popular_products','shopping','refine_products','explore_brands','product_considerations','commercial_units')),
          'forums':any(t in types for t in ('discussions_and_forums','perspectives')),'video':any(t in types for t in ('video','short_videos')),'local':'local_pack' in types,
          'source_calls':call,'in_stage7_master':k in S15,'stage15_disposition':S15[k]['mapping_disposition'] if k in S15 else '','stage15_owner':S15[k]['target_id'] if k in S15 else '',
          'in_call1':k in C1}
JEW=r"\b(ring|rings|jewel|jewelry|jewellery|diamond|diamonds|earring|earrings|necklace|necklaces|bracelet|bracelets|pendant|pendants|band|bands|stud|studs|hoop|hoops|huggie|huggies|chain|chains|bridal|engagement|engaged|propos\w*|anniversary|push present|charm|tennis|solitaire|eternity|bangle|anklet|gold|platinum|carat|wedding)\b"
out=[]
for k,r in rows.items():
    r['jewellery_related']=bool(re.search(JEW,k))
    out.append(r)
cols=list(out[0].keys())
w=csv.DictWriter(open('content-strategy/blog-calendar/revision/round1_merged_raw_keywords.csv','w',newline=''),fieldnames=cols); w.writeheader(); w.writerows(sorted(out,key=lambda r:-(r['search_volume'] or 0)))
print('unique',len(out),'jewellery-related',sum(r['jewellery_related'] for r in out),'in master',sum(r['in_stage7_master'] for r in out),'in call1',sum(r['in_call1'] for r in out))
