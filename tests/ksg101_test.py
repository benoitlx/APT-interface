from apt_interface.KSG101 import KSG101, KSG101Config
import json
from time import sleep

#print(json.dumps(KSG101Config.model_json_schema()))

with KSG101(config_file="config_KSG.yaml") as ksg:
    print(ksg.conf)

    ksg.identify()

    print(ksg.get_max_travel())

    while True:
        print(ksg.get_reading()) 
        sleep(1)