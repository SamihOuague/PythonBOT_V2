from datetime import datetime
from os import system
from lib.Binance.BinanceAPI import BinanceAPI
from lib.Analysis import Analysis
from time import sleep, time
from lib.Chart import *

class CryptoBotV2:
    def __init__(self):
        self.api = BinanceAPI()
        sleep(1)
        self.candles =  [[float(x) for x in c] for c in self.api.getCandles("CHZUSDT", "1m", round(time() - (60 * 15)) * 1000)]
        self.walletA = {"free": float(self.api.getAccount("CHZ")["free"]), "quote": 0}
        self.walletB = {"free": float(self.api.getAccount("USDT")["free"]), "quote": 0}
        self.analysis = Analysis(self.candles)
        self.buyPosition = False
        self.sellPosition = False
        self.stopLossSell = 0
        self.takeProfitSell = 0
        self.stopLossBuy = 0
        self.takeProfitBuy = 0
        self.logs = []
        self.lastScore = {"buy": 0, "sell": 0}
        sleep(1)

    def updateCandles(self):
        start = round(time() - (60 * 100)) * 1000
        self.candles = [[float(x) for x in c] for c in self.api.getCandles("CHZUSDT", "1m", start)]
        self.analysis.setCandles(self.candles)

    def orderBuy(self):
        order = self.api.createOrder("buy", (self.walletB["free"]), "CHZUSDT")
        sleep(1)
        newBalanceB = float(self.api.getAccount("USDT")["free"])
        sleep(1)
        newBalanceA = float(self.api.getAccount("CHZ")["free"])
        self.takeProfitBuy = self.candles[-1][4] + (self.candles[-1][4] * 0.01)
        self.stopLossBuy = self.candles[-1][4] - (self.candles[-1][4] * 0.01)
        self.logs.append("{} \033[33m BUY => {} \033[39m".format(datetime.fromtimestamp(self.candles[-1][0]/1000), self.candles[-1][4]))
        self.walletA["quote"] = newBalanceA if self.sellPosition else newBalanceA - self.walletA["free"]
        self.walletB["free"] = newBalanceB
        self.buyPosition = True
        return order

    def orderSell(self):    
        order = self.api.createOrder("sell", self.walletA["free"], "CHZUSDT")
        sleep(1)
        newBalanceB = float(self.api.getAccount("USDT")["free"])
        sleep(1)
        newBalanceA = float(self.api.getAccount("CHZ")["free"])
        self.takeProfitSell = self.candles[-1][4] - (self.candles[-1][4] * 0.01)
        self.stopLossSell = self.candles[-1][4] + (self.candles[-1][4] * 0.01)
        self.logs.append("{} \033[33m SELL => {} \033[39m".format(datetime.fromtimestamp(self.candles[-1][0]/1000), self.candles[-1][4]))
        self.walletB["quote"] = newBalanceB if self.buyPosition else newBalanceB - self.walletB["free"]
        self.walletA["free"] = newBalanceA
        self.sellPosition = True
        return order

    def takeProfitFunction(self, price):
        if self.buyPosition and price >= self.takeProfitBuy:
            self.logs.append("{} \033[32m WIN => {} \033[39m".format(datetime.fromtimestamp(self.candles[-1][0]/1000), price))
            self.closePositionB()
            
        elif self.sellPosition and price <= self.takeProfitSell:
            self.logs.append("{} \033[32m WIN => {} \033[39m".format(datetime.fromtimestamp(self.candles[-1][0]/1000), price))
            self.closePositionA()

    def stopLossFunction(self, price):
        if self.buyPosition and price <= self.stopLossBuy:
            self.logs.append("{} \033[31m LOSS => {} \033[39m".format(datetime.fromtimestamp(self.candles[-1][0]/1000), price))
            self.closePositionB()
        elif self.sellPosition and price >= self.stopLossSell:
            self.logs.append("{} \033[31m LOSS => {} \033[39m".format(datetime.fromtimestamp(self.candles[-1][0]/1000), price))
            self.closePositionA()

    def closePositionB(self):
        order = self.api.createOrder("sell", self.walletA["quote"], "CHZUSDT")
        sleep(1)
        newBalanceB = float(self.api.getAccount("USDT")["free"])
        sleep(1)
        newBalanceA = float(self.api.getAccount("CHZ")["free"])
        self.walletB["free"] = newBalanceB
        self.walletA = {"free": newBalanceA, "quote": 0}
        self.buyPosition = False
        return order

    def closePositionA(self):
        order = self.api.createOrder("buy", self.walletB["quote"], "CHZUSDT")
        sleep(1)
        newBalanceB = float(self.api.getAccount("USDT")["free"])
        sleep(1)
        newBalanceA = float(self.api.getAccount("CHZ")["free"])
        self.walletB = {"free": newBalanceB, "quote": 0}
        self.walletA["free"] = newBalanceA
        self.sellPosition = False
        return order

    def priceActionBuy(self):
        score = 0
        candle = self.candles[-1]
        if (self.analysis.invertedHammer(candle) or self.analysis.hammer(candle)) and self.analysis.trendRate(3) < -10:
            score += 2
        if (self.analysis.mobileAverage(99) > candle[1]):
            score += 1
        if (self.analysis.mobileAverage(25) < self.analysis.mobileAverage(99)):
            score += 1
        lastVolume = candle
        volumeScore = 0
        for i in range(2, 10):
            c = self.candles[0-i]
            if (lastVolume[5] < c[5] and lastVolume[4] > c[4]):
                lastVolume = c
                volumeScore += 1
            else:
                break
        
        if (volumeScore >= 3):
            score += 3

        self.lastScore["buy"] = score

        if score >= 4:
            return True
        return False

    def priceActionSell(self):
        score = 0
        candle = self.candles[-1]
        if (self.analysis.invertedHammer(candle) or self.analysis.hammer(candle)):
            score += 1
        if (self.analysis.mobileAverage(99) < candle[1]):
            score += 1
        if (self.analysis.mobileAverage(25) < self.analysis.mobileAverage(99)):
            score += 1
        lastVolume = candle
        volumeScore = 0
        for i in range(2, 10):
            c = self.candles[0-i]
            if (lastVolume[5] > c[5] and lastVolume[4] < c[4]):
                lastVolume = c
                volumeScore += 1
            else:
                break
        
        if (volumeScore >= 3):
            score += 2

        self.lastScore["sell"] = score

        if score >= 3:
            return True
        return False

    def run(self):
        while True:
            try:
                if (time() > (self.candles[-1][0]/1000) + 60):
                    self.updateCandles()
                sleep(1)
                price = float(self.api.ticker("CHZUSDT")["price"])
                if self.priceActionSell() and not self.sellPosition:
                    self.orderSell()
                if self.buyPosition or self.sellPosition:
                    self.takeProfitFunction(price)
                    self.stopLossFunction(price)
                    sleep(5)
                for l in self.logs():
                    print(l)
            except:
                sleep(5)
                continue