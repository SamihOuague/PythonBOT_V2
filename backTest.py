from lib.Simulation import SimulationV5
import json
from lib.Binance.BinanceAPI import BinanceAPI
candles = [[float(x) for x in c] for c in json.loads(open("dataset1M.json").read())]

simulation = SimulationV5(candles[0:99])

for i in range(5, len(candles)):
    simulation.makeDecision(candles[i])

if (simulation.walletB["quote"] > 0):
    simulation.walletA["free"] = simulation.walletB["quote"] / candles[-1][4]
    simulation.walletB["quote"] = 0
print("TAUX DE REUSSITE {}%".format(int(round(simulation.win / (simulation.win + simulation.loss), 2) * 100)))
print("NOMBRE DE TRADE = {}".format(simulation.win + simulation.loss))
print(simulation.walletA, simulation.walletB)