from lib.Binance.BinanceAPI import BinanceAPI
from os import system
from time import sleep, time
import json

api = BinanceAPI()
dataset = []
start = round(time() - (60 * 500)) * 1000
nbIter = 100
for i in range(0, nbIter):
    dataset = api.getCandles("CHZUSDT", "1m", start) + dataset
    start = round(((start/1000) - (60 * 500)) * 1000)
    system("clear")
    print("download... {}%".format(round((i/nbIter) * 100)))
    sleep(1)

f = open("dataset1M.json", "w")
f.write(json.dumps(dataset))
f.close()