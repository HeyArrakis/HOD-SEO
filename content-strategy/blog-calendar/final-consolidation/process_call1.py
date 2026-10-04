import json,csv
d=json.load(open('dataforseo/raw/final_calendar/01_gap_call1_keyword_overview_raw.json'))
grp={r['keyword']:r['group'] for r in csv.DictReader(open('content-strategy/blog-calendar/final-consolidation/gap_candidates.csv'))}
items=d['tasks'][0]['result'][0]['items']
out=[];got=set()
for it in items:
    k=it['keyword'];got.add(k)
    ki=it.get('keyword_info') or {}
    ms=ki.get('monthly_searches') or []
    mm={(m['year'],m['month']):m['search_volume'] for m in ms}
    vals=[v for v in mm.values() if v is not None]
    avg=sum(vals)/len(vals) if vals else 0
    def idx(y,m):
        v=mm.get((y,m)); return round(v/avg,2) if v and avg else ''
    peak=max(mm.items(),key=lambda x:x[1] or 0)[0] if mm else ''
    kp=it.get('keyword_properties') or {}
    si=it.get('search_intent_info') or {}
    serp=it.get('serp_info') or {}
    out.append({'group':grp.get(k,''),'keyword':k,'search_volume':ki.get('search_volume'),'keyword_difficulty':kp.get('keyword_difficulty'),
     'cpc':ki.get('cpc'),'paid_competition':ki.get('competition_level'),'dfs_main_intent':si.get('main_intent'),
     'peak_month':f'{peak[1]:02d}/{peak[0]}' if peak else '','oct_index':idx(2025,10),'nov_index':idx(2025,11),'dec_index':idx(2025,12),'jan_index':idx(2026,1),'feb_index':idx(2026,2),'mar_index':idx(2026,3),'may_index':idx(2026,5),
     'serp_item_types':';'.join(serp.get('serp_item_types') or []),'se_results_count':serp.get('se_results_count')})
for k,g in grp.items():
    if k not in got: out.append({'group':g,'keyword':k,'search_volume':'NOT_IN_DATAFORSEO_DB'})
out.sort(key=lambda x:(x['group'],-(x['search_volume'] if isinstance(x['search_volume'],int) else -1)))
f=list(out[0].keys())
w=csv.DictWriter(open('content-strategy/blog-calendar/final-consolidation/call1_processed.csv','w',newline=''),fieldnames=f);w.writeheader();w.writerows(out)
for x in out:
    print(x['group'][:6],'|',x['keyword'],'|',x['search_volume'],'|KD',x.get('keyword_difficulty'),'|',x.get('dfs_main_intent'),'|pk',x.get('peak_month'),'|dec',x.get('dec_index'),'jan',x.get('jan_index'),'|',(x.get('serp_item_types') or '')[:90])
