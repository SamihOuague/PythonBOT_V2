import json
from lib.Prototype import Prototype

dataset = [[float(x) for x in d] for d in json.loads(open("dataset1M.json").read())[0:100]]
for c in dataset:
    print(c)
proto = Prototype("CHZUSDT", dataset, False, False, 0.01, 0.01)

proto.makeDecision(float(dataset[0][4]))