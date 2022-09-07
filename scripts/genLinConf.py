import sys
import json
import math
import numpy as np

def genConf(trace1, trace2, t1_rate, scale):
    with open("FOOTPRINT_DESCRIPTORS/available_fds.txt", "r") as infile:
        for l in infile:
            l = l.strip().split(",")
            if trace1 == l[1]:
                t1_orig_req_rate = float(l[4])
            if trace2 == l[1]:
                t2_orig_req_rate = float(l[4])
    
    tot_req_rate = (t1_orig_req_rate + t2_orig_req_rate)*scale
    req_rate_1 = tot_req_rate*t1_rate
    req_rate_2 = tot_req_rate*(1-t1_rate)

    data = {}
    data["Trace_length"] = "100000000"
    data["Hitrate_type"] = "rhr"
    data["Input_unit"] = "reqs/s"
    data["Traffic_classes"] = []
    if math.floor(req_rate_1) > 0:
        data["Traffic_classes"].append({
            "traffic_class": trace1,
            "traffic_volume": str(math.floor(req_rate_1))
        })
    if math.floor(req_rate_2) > 0:
        data["Traffic_classes"].append({
            "traffic_class": trace2,
            "traffic_volume": str(math.floor(req_rate_2))
        })

    with open('config/tc-0-1-'+str(math.floor(req_rate_1))+':'+str(math.floor(req_rate_2))+'.config', 'w') as outfile:
        json.dump(data, outfile, indent=4)

# generate 100 TC-0 & TC-1 traffic mixtures
for x in np.linspace(0, 1, 200):
    genConf("tc-0", "tc-1", x, 2)
