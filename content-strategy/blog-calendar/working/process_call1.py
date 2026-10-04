import json,csv
d=json.load(open('dataforseo/raw/blog_calendar/01_keyword_overview_raw.json'))
items=d['tasks'][0]['result'][0]['items']
grp={r['keyword']:r['candidate_group'] for r in csv.DictReader(open('content-strategy/blog-calendar/working/candidate_keyword_list.csv'))}
MON=['','Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']
out=[];returned=set()
for it in items:
    kw=it['keyword']; returned.add(kw)
    ki=it.get('keyword_info') or {}
    ms={(m['year'],m['month']):m['search_volume'] for m in (ki.get('monthly_searches') or []) if m.get('search_volume') is not None}
    last12=[(y,m) for (y,m) in [(2025,9),(2025,10),(2025,11),(2025,12),(2026,1),(2026,2),(2026,3),(2026,4),(2026,5),(2026,6),(2026,7),(2026,8)]]
    vals=[ms.get(k) for k in last12]
    have=[v for v in vals if v is not None]
    avg=sum(have)/len(have) if have else None
    def idx(k): return round(ms[k]/avg,2) if avg and ms.get(k) is not None else ''
    peak=max(((ms[k],k) for k in last12 if ms.get(k) is not None), default=(None,None))
    si=it.get('serp_info') or {}
    types=si.get('serp_item_types') or []
    kp=it.get('keyword_properties') or {}
    intent=(it.get('search_intent_info') or {})
    out.append({
     'keyword':kw,'candidate_group':grp.get(kw,''),'search_volume':ki.get('search_volume'),
     'avg_last12':round(avg) if avg else '',
     'oct_2025':ms.get((2025,10),''),'nov_2025':ms.get((2025,11),''),'dec_2025':ms.get((2025,12),''),'jan_2026':ms.get((2026,1),''),'feb_2026':ms.get((2026,2),''),
     'nov_index':idx((2025,11)),'dec_index':idx((2025,12)),'feb_index':idx((2026,2)),'oct_index':idx((2025,10)),
     'peak_month_last12':f"{MON[peak[1][1]]} {peak[1][0]}" if peak[1] else '',
     'keyword_difficulty':kp.get('keyword_difficulty'),'cpc':ki.get('cpc'),'paid_competition':ki.get('competition'),'paid_competition_level':ki.get('competition_level'),
     'dfs_main_intent':intent.get('main_intent'),'dfs_foreign_intent':';'.join(intent.get('foreign_intent') or []),
     'serp_item_types':';'.join(types),
     'serp_has_ai_overview':'ai_overview' in types,
     'serp_product_led':any(t in types for t in ('popular_products','shopping','refine_products','explore_brands','product_considerations','commercial_units')),
     'serp_has_forums':any(t in types for t in ('discussions_and_forums','perspectives')),
     'serp_has_video':any(t in types for t in ('video','short_videos')),
     'serp_has_images':'images' in types,'serp_has_paa':'people_also_ask' in types,
     'serp_last_updated':si.get('last_updated_time',''),
     'core_keyword':kp.get('core_keyword'),'keyword_last_updated':ki.get('last_updated_time'),
     'data_source':'NEW_RESEARCH','source_endpoint':'dataforseo_labs/google/keyword_overview/live (2026-09-29)'})
missing=[k for k in grp if k not in returned]
for k in missing:
    out.append({'keyword':k,'candidate_group':grp[k],'search_volume':'NOT_IN_DATAFORSEO_DB','data_source':'NEW_RESEARCH','source_endpoint':'dataforseo_labs/google/keyword_overview/live (2026-09-29) - not returned, not charged'})
cols=list(out[0].keys())
w=csv.DictWriter(open('content-strategy/blog-calendar/working/call1_processed.csv','w',newline=''),fieldnames=cols);w.writeheader();w.writerows(out)
print(len(out),'missing',len(missing),missing)
