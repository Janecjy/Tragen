import sys
import json
import math
import numpy as np

def genConf(trace1, trace2, rate):
    with open("FOOTPRINT_DESCRIPTORS/available_fds.txt", "r") as infile:
        for l in infile:
            l = l.strip().split(",")
            if trace1 == l[1]:
                t1_orig_req_rate = float(l[4])
            if trace2 == l[1]:
                t2_orig_req_rate = float(l[4])
    
    req_rate_1 = 100*rate
    req_rate_2 = 100*(1-rate)

    data = {}
    data["Trace_length"] = "10000000"
    data["Hitrate_type"] = "rhr"
    data["Input_unit"] = "reqs/s"
    data["Traffic_classes"] = []
    data["Traffic_classes"].append({
        "traffic_class": trace1,
        "traffic_volume": str(math.floor(t1_orig_req_rate*req_rate_1))
    })
    data["Traffic_classes"].append({
        "traffic_class": trace2,
        "traffic_volume": str(math.floor(t2_orig_req_rate*req_rate_2))
    })

    with open('config/tc-0-1-'+str(math.floor(req_rate_1*10)/10)+':'+str(math.floor(req_rate_2*10)/10)+'.config', 'w') as outfile:
        json.dump(data, outfile, indent=4)

# generate 100 TC-0 & TC-1 traffic mixtures
for x in np.linspace(0, 1, 1000):
    genConf("tc-0", "tc-1", x)

    