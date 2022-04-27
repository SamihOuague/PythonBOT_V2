from lib.Binance.BinanceAPI import BinanceAPI
from lib.Simulation import SimulationV5
from lib.CryptoBot_V2 import CryptoBotV2

#api = BinanceAPI()
#
#candles = [[float(x) for x in c] for c in json.loads(open("dataset1M.json").read())]
#simulation = SimulationV5(candles[0:6], 0, 100)
#
#for i in range(5, len(candles)):
#    simulation.makeDecision(candles[i])
#print("TAUX DE REUSSITE {}%".format(int(round(simulation.win / (simulation.win + simulation.loss), 2) * 100)))
#print("NOMBRE DE TRADE = {}".format(simulation.win + simulation.loss))
#print(round(simulation.walletA, 2), round(simulation.walletB, 2))

bot = CryptoBotV2()
bot.run()
print("STARTED")
