from lib.Prototype import Prototype

class Launcher:
    def __init__(self, symbol, initialCandles, takeProfit, stopLoss, priceActionSell=False, priceActionBuy=False):
        self.prototype = Prototype(symbol, initialCandles, priceActionBuy, priceActionSell, takeProfit, stopLoss)