from datetime import datetime
from lib.Analysis import Analysis

class SimulationV5:
    def __init__(self, dataset):
        self.dataset = [[float(x) for x in d] for d in dataset]
        self.walletA = {"free": 100, "quote": 0}
        self.walletB = {"free": 0, "quote": 0}
        self.analysis = Analysis(self.dataset)
        self.buyPosition = False
        self.sellPosition = False
        self.stopTrade = False
        self.stopLossSell = 0
        self.takeProfitSell = 0
        self.stopLossBuy = self.dataset[-1][4]
        self.takeProfitBuy = self.dataset[-1][4]
        self.win = 0
        self.loss = 0
        self.lossSucc = 0

    def updateDataset(self, lastCandle):
        self.dataset.pop(0)
        self.dataset.append([float(x) for x in lastCandle])
        self.analysis.setCandles(self.dataset)

    def priceActionBuy(self):
        score = 0
        candle = self.dataset[-1]
        lastVolume = candle
        volumeScore = 0
        for i in range(2, 5):
            c = self.dataset[0-i]
            if (lastVolume[5] < c[5] and lastVolume[4] < c[4]):
                lastVolume = c
                volumeScore += 1
            else:
                break

        if volumeScore >= 3 and candle[4] > c:
            return True
        return False

    def priceActionSell(self):
        candle = self.dataset[-1]
        lastVolume = candle
        volumeScore = 0
        
        for i in range(2, 5):
            c = self.dataset[0-i]
            if (lastVolume[5] > c[5] and c[1] > c[4] and c[4] > lastVolume[4]):
                lastVolume = c
                volumeScore += 1
            else:
                break
            
        
        ecart = round(self.analysis.mobileAverage(99) / self.analysis.mobileAverage(25) * 100, 4)
        if ecart > 100:
            ecart = round(100 - ecart, 2)
            pass
        elif ecart < 100:
            ecart = round(100 - ecart, 2)
            pass
        else:
            ecart = 0
        if (volumeScore >= 2 and self.analysis.getRSI(7) > 20):
            return True
        return False

    def orderBuy(self, price):
        print("{} \033[33m BUY => {} \033[39m".format(datetime.fromtimestamp(self.dataset[-1][0]/1000), price))
        self.takeProfitBuy = price + (price * 0.01)
        self.stopLossBuy = price - (price * 0.01)
        self.buyPosition = True
        self.walletA["quote"] = self.walletB["free"] / price
        self.walletB["free"] = 0
        return True

    def orderSell(self, price):
        print("{} \033[33m SELL => {} \033[39m".format(datetime.fromtimestamp(self.dataset[-1][0]/1000), price))
        self.takeProfitSell = price - (price * 0.01)
        self.stopLossSell = price + (price * 0.01)
        self.sellPosition = True
        self.walletB["quote"] = self.walletA["free"] * price
        self.walletA["free"] = 0
        return True

    def takeProfitFunction(self, price):
        if self.buyPosition and price >= self.takeProfitBuy:
            self.buyPosition = False
            print("{} \033[32m WIN => {} \033[39m".format(datetime.fromtimestamp(self.dataset[-1][0]/1000), price))
            self.win += 1
            self.walletB["free"] = self.walletA["quote"] * price
            self.walletA["quote"] = 0
            return True
        elif self.sellPosition and price <= self.takeProfitSell:
            self.sellPosition = False
            print("{} \033[32m WIN => {} \033[39m".format(datetime.fromtimestamp(self.dataset[-1][0]/1000), price))
            self.win += 1
            self.walletA["free"] = self.walletB["quote"] / price
            self.walletB["quote"] = 0
            return True

    def stopLossFunction(self, price):
        if self.buyPosition and price <= self.stopLossBuy:
            print("{} \033[31m LOSS => {} \033[39m".format(datetime.fromtimestamp(self.dataset[-1][0]/1000), price))
            self.buyPosition = False
            self.loss += 1
            self.walletB["free"] = self.walletA["quote"] * price
            self.walletA["quote"] = 0
            self.lossSucc += 1
            return True
        elif self.sellPosition and price >= self.stopLossSell:
            print("{} \033[31m LOSS => {} \033[39m".format(datetime.fromtimestamp(self.dataset[-1][0]/1000), price))
            self.sellPosition = False
            self.loss += 1
            self.walletA["free"] = self.walletB["quote"] / price
            self.walletB["quote"] = 0
            self.lossSucc += 1
            return True

    def makeDecision(self, candle):
        self.updateDataset(candle)
        price = float(candle[4])
        #if self.priceActionBuy() and not self.buyPosition:
        #    self.orderBuy(price)
        if self.priceActionSell() and not self.sellPosition:
            self.orderSell(price)
        self.takeProfitFunction(price)
        self.stopLossFunction(price)
