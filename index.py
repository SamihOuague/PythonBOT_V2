from lib.Prototype import Prototype
from lib.Binance.BinanceAPI import BinanceAPI
from time import time
import numpy as np
from random import randint
api = BinanceAPI()
dataset = [[float(x) for x in d] for d in api.getCandles("BNBUSDT", "1m",  str(round(time() - (60*100)) * 1000))]


def sell(candles):
    ma100 = np.average([x[4] for x in candles])
    ma50 = np.average([x[4] for x in candles[-50:-1]])
    ecartMA100 = ((candles[-2][4] - ma100)/candles[-2][4])*100
    ecartMA50 = ((candles[-2][4] - ma50)/candles[-2][4])*100
    takePos = randint(0,1)
    print(ecartMA50, ecartMA100, takePos)
    if randint(0,1) and -4 < ecartMA50 < 0 and ecartMA100 < 0:
        return True
    else:
        return False


bnbBot = Prototype(dataset, "BNBUSDT", priceActionSell=sell)
bnbBot.run()