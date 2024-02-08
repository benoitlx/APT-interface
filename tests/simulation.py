from apt_interface.scan import Scan, ScanConfig
import json
import matplotlib.pyplot as plt

print(json.dumps(ScanConfig.model_json_schema()))

s = Scan((None, None), config_file="tests/scan.yaml")

print(s.conf)
print(s.conf.zoi.ref_point.Z)


fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

x = [c[0] for c in s.coords]
y = [c[1] for c in s.coords]
z = [c[2] for c in s.coords]
ax.plot3D(x, y, z) 

ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
plt.show()