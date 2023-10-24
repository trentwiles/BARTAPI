import subprocess
import json

def cacheMissHit():
    try:
        api = json.loads(subprocess.check_output("varnishstat --json", shell=True, text=True))
    except:
        return {"cacheHits": 0, "cacheMiss": 0, "hitRatio": 0, "backendFetches": 0, "backendFailures": 0, "backendFailRatio": 0}
    hit = api["counters"]["MAIN.cache_hit"]["value"]
    miss = api["counters"]["MAIN.cache_miss"]["value"]

    backendFetch = api["counters"]["MAIN.backend_req"]["value"]
    backendFails = api["counters"]["MAIN.backend_fail"]["value"]

    
    ratio = hit / (miss + hit)

    if backendFails == 0 or backendFetch == 0:
        backendFailRatio = 0
    else:
        backendFailRatio = backendFails / (backendFails + backendFetch)
    return {"cacheHits": hit, "cacheMiss": miss, "hitRatio": round(ratio, 3), "backendFetches": backendFetch, "backendFailures": backendFails, "backendFailRatio": round(backendFailRatio, 3)}

def space():
    try:
        api = json.loads(subprocess.check_output("varnishstat --json", shell=True, text=True))
    except:
        return {"memoryUsedInBytes": 0}
        
    # Experimental, not sure if I'm understanding the Varnish API correctly
    memUsed = api["counters"]["MAIN.s_resp_bodybytes"]["value"] + api["counters"]["MAIN.s_resp_hdrbytes"]["value"]
    return {"memoryUsedInBytes": memUsed}

print(cacheMissHit())