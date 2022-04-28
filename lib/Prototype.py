from datetime import datetime
from time import time
from lib.Binance.BinanceAPI import BinanceAPI
from lib.Analysis import Analysis

class Prototype:
    def __init__(self, symbol, candles, priceActionBuy, priceActionSell, takeProfit, stopLoss):
        self.api = BinanceAPI()
        self.candles = candles
        self.analysis = Analysis(self.candles)
        self.priceActionBuy = priceActionBuy
        self.priceActionSell = priceActionSell
        self.takeProfit = takeProfit
        self.stopLoss = stopLoss
        self.limit = 0
        self.stopLimit = 0
        self.symbol = symbol
        self.quoteAsset = 0
        self.baseAsset = 100
        self.sellPosition = False
        self.buyPosition = False
        self.win = 0
        self.loss = 0

    def updateCandles(self, candle):
        try:
            self.candles.pop(0)
            self.candles.append([float(x) for x in candle])
            self.analysis.setCandles(self.candles)
            return True
        except:
            return False

    def getAccount(self):
        try:
            accounts = self.api.getAccounts("isolated", self.symbol)["assets"][0]
            self.baseAsset = float(accounts["baseAsset"]["free"])
            self.quoteAsset = float(accounts["quoteAsset"]["free"])
            return {"base": self.baseAsset, "quote": self.quoteAsset}
        except:
            return False

    def takeProfitFn(self, price):
        if self.sellPosition and self.limit >= price:
            print("{} \033[32m WIN => {} \033[39m".format(datetime.fromtimestamp(self.candles[-1][0]/1000), price))
            self.sellPosition = False
            self.buy(price)
            self.win += 1
            return 1
        elif self.buyPosition and self.limit <= price:
            self.buyPosition = False
            self.sell(price)
            self.win += 1 
            return 2 
        return 0

    def stopLossFn(self, price):
        if self.sellPosition and self.stopLimit <= price:
            print("{} \033[31m LOSS => {} \033[39m".format(datetime.fromtimestamp(self.candles[-1][0]/1000), price))
            self.sellPosition = False
            self.buy(price)
            self.loss += 1
            return 1
        elif self.buyPosition and self.stopLimit >= price:
            self.buyPosition = False
            self.sell(price)
            self.loss += 1
            return 2 
        return 0

    def buy(self, price):
        if self.quoteAsset > 0:
            self.baseAsset = self.quoteAsset / price
            self.quoteAsset = 0
            return True
        else:
            return False
    
    def sell(self, price):
        if self.baseAsset > 0:
            self.quoteAsset = self.baseAsset * price
            self.baseAsset = 0
            return True
        else:
            return False

    def makeDecision(self, price):
        if not (self.buyPosition or self.sellPosition):
            if (self.priceActionSell and self.priceActionSell(self.candles, self.analysis)):
                self.sellPosition = True
                self.stopLimit = price + (price * 0.01)
                self.limit = price - (price * 0.01)
                print("{} \033[33m SELL => {} \033[39m".format(datetime.fromtimestamp(self.candles[-1][0]/1000), price))
                self.sell(price)
                return 2
            elif (self.priceActionBuy and self.priceActionBuy()):
                self.buyPosition = True
                self.stopLimit = price - (price * 0.01)
                self.limit = price + (price * 0.01)
                self.buy(price)
                return 1
            else:
                return 0
        else:
            self.takeProfitFn(price)
            self.stopLossFn(price)

    def run(self, candle):
        price = float(candle[1])
        if candle:
            self.updateCandles(candle)
        self.makeDecision(price)
        


        