import json
import mef

with open("modelo1.json") as file:
    data = json.load(file)

coords = data["coords"]
connect = data["connect"]
forces = data["forces"]
restrs = data["restrs"]
props = data["props"]

D, S = mef.analise(coords, connect, forces, restrs, props)
print(D)
print(S)
