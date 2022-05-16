from datetime import datetime
from time import sleep, time
from lib.OrderManager import OrderManager
from lib.Binance.BinanceAPI import BinanceAPI
import requests

class Prototype:
    def __init__(self, initialCandle, symbol, priceActionBuy=False, priceActionSell=False, takeProfit = 0.013, stopLoss = 0.013):
        self.api = BinanceAPI()
        self.candles = initialCandle
        self.priceActionBuy = priceActionBuy
        self.priceActionSell = priceActionSell
        self.manager = OrderManager(symbol)
        self.takeProfit = takeProfit
        self.stopLoss = stopLoss
        self.limit = 0
        self.stopLimit = 0
        self.sellPosition = False
        self.buyPosition = False
        self.symbol = symbol

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
            return 1
        elif self.buyPosition and self.limit <= price:
            self.buyPosition = False
            self.manager.orderSell()
            return 2 
        return 0

    def stopLossFn(self, price):
        if self.sellPosition and self.stopLimit <= price:
            self.sellPosition = False
            self.manager.orderBuy()
        elif self.buyPosition and self.stopLimit >= price:
            self.buyPosition = False
            self.manager.orderSell()
            return 2 
        return 0

    def makeDecision(self, price):
        if not (self.buyPosition or self.sellPosition):
            if (self.priceActionSell and self.priceActionSell(self.candles)):
                self.sellPosition = True
                self.stopLimit = price + (price * self.stopLoss)
                self.limit = price - (price * self.takeProfit)
                return self.manager.orderSell()
            elif (self.priceActionBuy and self.priceActionBuy(self.candles)):
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
                    candle = self.api.getCandles(self.symbol, "1m", str(round(time() - 61) * 1000))
                    if len(candle) > 0:
                        self.updateCandles(candle[0])
                        print("\033[33m{} New Candle - {}".format(datetime.fromtimestamp(round(time())), self.candles[-1][4]))
                price = float(self.candles[-1][4])
                if self.makeDecision(price):
                    print("\033[32m{} New position".format(datetime.fromtimestamp(round(time()))))
            except:
                print("\033[31m{} Error".format(datetime.fromtimestamp(round(time()))))
            sleep(10)
