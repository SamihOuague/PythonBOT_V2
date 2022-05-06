from datetime import datetime
from time import sleep, time
from lib.Analysis import Analysis
from lib.OrderManager import OrderManager
from lib.Binance.BinanceAPI import BinanceAPI
import requests

class Prototype:
    def __init__(self, symbol, priceActionBuy, priceActionSell, takeProfit = 0.01, stopLoss = 0.01):
        self.api = BinanceAPI()
        self.candles = [[float(x) for x in t] for t in self.api.getCandles(symbol, "1m", str(round(time() - (60 * 100)) * 1000))]
        self.analysis = Analysis(self.candles)
        self.priceActionBuy = priceActionBuy
        self.priceActionSell = priceActionSell
        self.manager = OrderManager(symbol)
        self.takeProfit = takeProfit
        self.stopLoss = stopLoss
        self.limit = 0
        self.stopLimit = 0
        self.sellPosition = False
        self.buyPosition = False

    def updateCandles(self, candle):
        try:
            if float(candle[0]) != self.candles[-1][0]:
                self.candles.pop(0)
                self.candles.append([float(x) for x in candle])
                self.analysis.setCandles(self.candles)
                return True
            else:
                return False
        except:
            return False

    def takeProfitFn(self, price):
        if self.sellPosition and self.limit >= price:
            self.sellPosition = False
            self.manager.orderBuy()
            return requests.post("http://localhost:3001/log", json={"log": "WIN={}".format(price), "orderedAt": str(datetime.fromtimestamp(self.candles[-1][0]/1000))})
        elif self.buyPosition and self.limit <= price:
            self.buyPosition = False
            return 2 
        return 0

    def stopLossFn(self, price):
        if self.sellPosition and self.stopLimit <= price:
            self.manager.orderBuy()
            self.sellPosition = False
            self.manager.orderBuy()
            return requests.post("http://localhost:3001/log", json={"log": "LOSS={}".format(price), "orderedAt": str(datetime.fromtimestamp(self.candles[-1][0]/1000))})
        elif self.buyPosition and self.stopLimit >= price:
            self.buyPosition = False
            return 2 
        return 0

    def makeDecision(self, price):
        if not (self.buyPosition or self.sellPosition):
            if (self.priceActionSell and self.priceActionSell(self.candles, self.analysis)):
                self.sellPosition = True
                self.stopLimit = price + (price * self.stopLoss)
                self.limit = price - (price * self.takeProfit)
                self.manager.orderSell()
                return requests.post("http://localhost:3001/log", json={"log": "SELL={}".format(price), "orderedAt": str(datetime.fromtimestamp(self.candles[-1][0]/1000))})
            elif (self.priceActionBuy and self.priceActionBuy()):
                self.buyPosition = True
                self.stopLimit = price - (price * self.stopLoss)
                self.limit = price + (price * self.takeProfit)
                return self.manager.orderBuy()
            else:
                return 0
        else:
            self.takeProfitFn(price)
            self.stopLossFn(price)
        return 0

    def run(self):
        while True:
            try:
                if ((self.candles[-1][0]/1000) + 60) < time():
                    candle = self.api.getCandles("CHZUSDT", "1m", str(round(time() - 61) * 1000))
                    if len(candle) > 0:
                        self.updateCandles(candle[0])
                        print("\033[33m{} New Candle - {}".format(datetime.fromtimestamp(round(time())), self.candles[-1][1]))
                price = float(self.candles[-1][1])
                if self.sellPosition or self.buyPosition:
                    price = float(self.api.ticker("CHZUSDT")["price"])
                if self.makeDecision(price):
                    print("\033[32m{} New position".format(datetime.fromtimestamp(round(time()))))
            except:
                print("\033[31m{} Error".format(datetime.fromtimestamp(round(time()))))
            sleep(10)
