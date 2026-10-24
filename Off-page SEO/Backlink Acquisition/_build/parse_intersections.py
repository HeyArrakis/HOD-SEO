"""Flatten DataForSEO page_intersection raw JSON into one row per (referring page, competitor target).
Usage: python3 parse_intersections.py <raw.json> <out.csv> <call_id>
Read-only on the raw file; writes only the processed CSV."""
import json, csv, sys
raw, out, call = sys.argv[1], sys.argv[2], sys.argv[3]
d = json.load(open(raw))
r = d['tasks'][0]['result'][0]
targets = r['targets']
cols = ['call_id','url_from','domain_from','page_from_title','domain_from_country','domain_from_platform_type',
        'domain_from_rank','page_from_rank','backlink_spam_score','page_from_external_links',
        'competitor_target','url_to','anchor','item_type','dofollow','attributes','semantic_location',
        'first_seen','last_seen','is_lost','is_broken','url_to_status_code']
rows = []
for item in r['items']:
    for k, links in item['page_intersection'].items():
        for it in (links or []):
            rows.append({'call_id': call, 'url_from': it['url_from'], 'domain_from': it['domain_from'],
                'page_from_title': (it.get('page_from_title') or '').strip(), 'domain_from_country': it.get('domain_from_country'),
                'domain_from_platform_type': '|'.join(it.get('domain_from_platform_type') or []),
                'domain_from_rank': it.get('domain_from_rank'), 'page_from_rank': it.get('page_from_rank'),
                'backlink_spam_score': it.get('backlink_spam_score'), 'page_from_external_links': it.get('page_from_external_links'),
                'competitor_target': targets[k], 'url_to': it.get('url_to'), 'anchor': (it.get('anchor') or '').strip(),
                'item_type': it.get('item_type'), 'dofollow': it.get('dofollow'), 'attributes': '|'.join(it.get('attributes') or []),
                'semantic_location': it.get('semantic_location'), 'first_seen': (it.get('first_seen') or '')[:10],
                'last_seen': (it.get('last_seen') or '')[:10], 'is_lost': it.get('is_lost'), 'is_broken': it.get('is_broken'),
                'url_to_status_code': it.get('url_to_status_code')})
with open(out, 'w', newline='', encoding='utf-8') as f:
    w = csv.DictWriter(f, fieldnames=cols); w.writeheader(); w.writerows(rows)
print(call, 'pages', len(r['items']), 'link rows', len(rows), 'total_count', r['total_count'])
