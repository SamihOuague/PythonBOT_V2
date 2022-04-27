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
        self.quoteAsset = {}
        self.baseAsset = {}
        self.sellPosition = False
        self.buyPosition = False
        self.win = 0
        self.loss = 0
        self.getAccount()

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
            self.walletA = float(accounts["baseAsset"]["free"])
            self.walletB = float(accounts["quoteAsset"]["free"])
            return {"base": self.walletA, "quote": self.walletB}
        except:
            return False

    def takeProfitFn(self, price):
        if self.sellPosition and self.limit > price:
            return 1
        elif self.buyPosition and self.limit < price:
            return 2 
        return 0

    def stopLossFn(self, price):
        if self.sellPosition and self.stopLimit <= price:
            return 1
        elif self.buyPosition and self.stopLimit >= price:
            return 2 
        return 0

    def makeDecision(self, price):
        if not (self.buyPosition and self.sellPosition):
            if (self.priceActionSell and self.priceActionSell()):
                return 2
            elif (self.priceActionBuy and self.priceActionBuy()):
                return 1
            else:
                return 0
        else:
            self.takeProfitFn(price)
            self.stopLossFn(price)

    def run(self, candle):
        price = float(candle[4])
        self.updateCandles(candle)
        self.makeDecision(price)
        


        