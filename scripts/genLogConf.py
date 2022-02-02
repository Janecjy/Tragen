import sys
import json
import math
import numpy as np

for x in np.logspace(2, 5, num=10):
    x = math.floor(x/100)*100
    print(x)

    data = {}
    data["Trace_length"] = "10000000"
    data["Hitrate_type"] = "rhr"
    data["Input_unit"] = "reqs/s"
    data["Traffic_classes"] = []
    data["Traffic_classes"].append({
        "traffic_class": "tc-0",
        "traffic_volume": str(x*100)
    })
    data["Traffic_classes"].append({
        "traffic_class": "tc-1",
        "traffic_volume": 100
    })

    with open('config/tc-0-1-'+str(x)+':1.config', 'w') as outfile:
        json.dump(data, outfile, indent=4)