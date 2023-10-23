import subprocess
import json

def cacheMissHit():
    api = json.loads(subprocess.check_output("varnishstat --json", shell=True, text=True))
    hit = api["counters"]["MAIN.cache_hit"]["value"]
    miss = api["counters"]["MAIN.cache_miss"]["value"]
    ratio = hit / (miss + hit)
    return {"cacheHits": hit, "cacheMiss": miss, "hitRatio": ratio}

print(cacheMissHit())