import json,glob,csv,re,collections
# group keywords whose monthly search series are identical (DataForSEO/Google Ads volume groups = same demand)
sig={}
for f in sorted(glob.glob('dataforseo/raw/blog_calendar/revision/R1_*.json')):
    r=json.load(open(f))['tasks'][0]['result'][0]
    items=list(r['items'])+([r['seed_keyword_data']] if r.get('seed_keyword_data') else [])
    for it in items:
        ki=it.get('keyword_info') or {}
        ms=tuple((m['year'],m['month'],m['search_volume']) for m in (ki.get('monthly_searches') or [])[:12])
        sig[it['keyword'].lower().strip()]=ms
rows=list(csv.DictReader(open('content-strategy/blog-calendar/revision/round1_merged_raw_keywords.csv')))
groups=collections.defaultdict(list)
for r in rows:
    s=sig.get(r['keyword'])
    key=s if s and any(x[2] for x in s) else ('solo',r['keyword'])
    groups[key].append(r)
out=[]
for i,(k,members) in enumerate(sorted(groups.items(),key=lambda kv:-int(kv[1][0]['search_volume'] or 0)),1):
    members.sort(key=lambda r:(len(r['keyword']),r['keyword']))
    rep=members[0]
    for m in members:
        m['demand_group']=f'DG-{i:04d}'; m['group_representative']=rep['keyword']; m['group_size']=len(members)
        out.append(m)
cols=list(out[0].keys())
w=csv.DictWriter(open('content-strategy/blog-calendar/revision/round1_merged_raw_keywords.csv','w',newline=''),fieldnames=cols); w.writeheader(); w.writerows(out)
print('keywords',len(out),'demand groups',len(groups))
