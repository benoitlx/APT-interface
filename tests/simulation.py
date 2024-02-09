from apt_interface.scan import Scan, ScanConfig
import json
import matplotlib.pyplot as plt
from time import sleep

#print(json.dumps(ScanConfig.model_json_schema()))

def mesure(x, y):
    sleep(1)

    return 1

s = Scan((None, None), config_file="tests/scan.yaml")

print(s.conf)
print(s.conf.zoi.ref_point.Z)
print(s.coords)

s.visualize()
s.scan()