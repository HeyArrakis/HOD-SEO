#!/usr/bin/env python3
"""Recover verbatim DataForSEO MCP responses for Stage 18.5.

The DataForSEO MCP returns responses to the session (credentials stay in the MCP config), so the
exact JSON text of each response is recovered, unmodified, from:
  1. the local Claude session transcript (responses returned inline), and
  2. the tool-results files the client wrote for large responses.
Only responses whose task tag is 'hod_stage18_5' are saved. Each file = one task_get/advanced
response (free endpoint); 00_task_post_response.json = the single paid task_post response."""
import glob, json, os
SESS = os.path.expanduser('~/.claude/projects/-Users-manavdesai-Desktop-HOD-SEO-Research/3a3face9-5a2b-4c22-97b9-7c70b8a2e7f6')
OUT = os.path.dirname(os.path.abspath(__file__))
found, post = {}, None

def consider(t, src):
    global post
    t = t.strip()
    if not t.startswith('{'):
        return
    try:
        d = json.loads(t)
    except Exception:
        return
    for task in d.get('tasks') or []:
        data = task.get('data') or {}
        if data.get('tag') != 'hod_stage18_5':
            continue
        if data.get('function') == 'task_get':
            found.setdefault(task['id'], (t, src))
        elif data.get('function') == 'task_post' and len(d.get('tasks')) == 17:
            post = (t, src)

def texts(c):
    if isinstance(c, str):
        yield c
    elif isinstance(c, list):
        for x in c:
            if isinstance(x, dict) and x.get('type') == 'text':
                yield x.get('text', '')

for line in open(SESS + '.jsonl', encoding='utf-8'):
    try:
        rec = json.loads(line)
    except Exception:
        continue
    content = (rec.get('message') or {}).get('content')
    if isinstance(content, list):
        for part in content:
            if isinstance(part, dict) and part.get('type') == 'tool_result':
                for t in texts(part.get('content')):
                    consider(t, 'session_transcript')
for f in glob.glob(os.path.join(SESS, 'tool-results', '*')):
    raw = open(f, encoding='utf-8').read()
    try:
        arr = json.loads(raw)
        if isinstance(arr, list):
            for x in arr:
                if isinstance(x, dict) and x.get('type') == 'text':
                    consider(x['text'], os.path.basename(f))
            continue
    except Exception:
        pass
    consider(raw, os.path.basename(f))

for tid, (t, src) in found.items():
    open(os.path.join(OUT, f'{tid}.json'), 'w', encoding='utf-8').write(t)
if post:
    open(os.path.join(OUT, '00_task_post_response.json'), 'w', encoding='utf-8').write(post[0])
json.dump({tid: src for tid, (t, src) in found.items()} | ({'task_post': post[1]} if post else {}),
          open(os.path.join(OUT, '_raw_sources.json'), 'w'), indent=1)
print(len(found), 'task_get responses;', 'task_post verbatim' if post else 'task_post NOT found')
