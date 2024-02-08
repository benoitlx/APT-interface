from apt_interface.scan import Scan, ScanConfig
import json

print(json.dumps(ScanConfig.model_json_schema()))

s = Scan((None, None), config_file="tests/scan.yaml")

print(s.conf)
print(s.conf.balayage.steps.X)