import json, urllib.request, time, sys
from concurrent.futures import ThreadPoolExecutor
H={"User-Agent":"Mozilla/5.0"}
def get(u):
    for i in range(3):
        try: return json.load(urllib.request.urlopen(urllib.request.Request(u,headers=H),timeout=20))
        except Exception as e: time.sleep(1)
    return None
jobs=[];off=0
while True:
    d=get(f"https://www.wanted.co.kr/api/v4/jobs?country=kr&tag_type_ids=658&tag_type_ids=672&job_sort=job.popularity_order&locations=all&years=-1&limit=100&offset={off}")
    if not d or not d["data"]: break
    jobs+=d["data"]; off+=100
    if not d["links"].get("next"): break
print("list",len(jobs),file=sys.stderr)
def det(j):
    d=get(f"https://www.wanted.co.kr/api/v4/jobs/{j['id']}")
    return d.get("job") if d else None
with ThreadPoolExecutor(8) as ex: dets=list(ex.map(det,jobs))
json.dump({"list":jobs,"detail":dets},open("raw.json","w",encoding="utf-8"),ensure_ascii=False)
print("done",sum(1 for x in dets if x),file=sys.stderr)
