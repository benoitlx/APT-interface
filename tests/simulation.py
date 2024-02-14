from apt_interface.scan import Scan, ScanConfig
import json
from time import sleep

#print(json.dumps(ScanConfig.model_json_schema()))

def mesure(*args, **kwargs):
    sleep(.1)

    return 1

s = Scan((None, None), config_file="tests/scan.yaml")

print(s.conf)
print(s.coords)

s.visualize()