import json
import mef

with open("elementosfinitos/barra/modelo1.json") as file:
    data = json.load(file)

coords = data["coords"]
connect = data["connect"]
forces = data["forces"]
restrs = data["restrs"]
props = data["props"]

D = mef.analise(coords, connect, forces, restrs, props)
