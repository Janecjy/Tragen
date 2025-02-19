import sys
import json
import math
import numpy as np

# multiple is the multiple of request rate
def genConf(trace1, trace2, rate, multiple):
    with open("FOOTPRINT_DESCRIPTORS/available_fds.txt", "r") as infile:
        for l in infile:
            l = l.strip().split(",")
            if trace1 == l[1]:
                t1_orig_req_rate = float(l[4])
            if trace2 == l[1]:
                t2_orig_req_rate = float(l[4])
    
    # req_rate_1 = rate
    # req_rate_2 = 100-rate
    
    req_rate_1 = (1000-rate)/10
    req_rate_2 = rate/10

    data = {}
    data["Trace_length"] = "10000000"
    data["Hitrate_type"] = "rhr"
    data["Input_unit"] = "reqs/s"
    data["Traffic_classes"] = []
    if req_rate_1 > 0:
        data["Traffic_classes"].append({
            "traffic_class": trace1,
            "traffic_volume": str(math.floor(t1_orig_req_rate*req_rate_1*multiple))
        })
    if req_rate_2 > 0:
        data["Traffic_classes"].append({
            "traffic_class": trace2,
            "traffic_volume": str(math.floor(t2_orig_req_rate*req_rate_2*multiple))
        })

    with open('config/tc-0-1-'+str(math.floor(req_rate_1*multiple))+':'+str(math.floor(req_rate_2*multiple))+'.config', 'w') as outfile:
        json.dump(data, outfile, indent=4)

# generate 200 TC-0 & TC-1 traffic mixtures, x is the multiplier ratio of TC-0 and TC-1
for x in np.logspace(1, 3, 200):
    genConf("tc-0", "tc-1", x, 5)
