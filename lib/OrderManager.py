from lib.Binance.BinanceAPI import BinanceAPI
class OrderManager:
    def __init__(self, symbol = "CHZUSDT"):
        self.api = BinanceAPI()
        self.symbol = symbol
        self.wallet = {"base": 0, "quote": 0}
        self.updateWallet()

    def updateWallet(self):
        try:
            account = self.api.getAccounts("isolated", self.symbol)["assets"][0]
            wB = account["baseAsset"]["free"].split(".")
            wQ = account["quoteAsset"]["free"].split(".")
            wB[1] = wB[1][:3]
            wQ[1] = wQ[1][:2]
            self.wallet["base"] = ".".join(wB)
            self.wallet["quote"] = ".".join(wQ)
            return self.wallet
        except:
            return False

    def orderBuy(self):
        try:
            orderId = self.api.createMarginOrder("BUY", self.wallet["quote"], self.symbol)["orderId"]
            self.updateWallet()
            return orderId
        except:
            return False

    def orderSell(self):
        try:
            orderId = self.api.createMarginOrder("SELL", self.wallet["base"], self.symbol)["orderId"]
            self.updateWallet()
            return orderId
        except:
            return False
    

#{
#    'symbol': 'CHZUSDT', 
#    'orderId': 1072744675, 
#    'clientOrderId': 'beDWvw4lQcDH7UWB3rIyRq', 
#    'transactTime': 1651683718736, 
#    'price': '0', 
#    'origQty': '99', 
#    'executedQty': '99', 
#    'cummulativeQuoteQty': '18.612', 
#    'status': 'FILLED', 
#    'timeInForce': 'GTC', 
#    'type': 'MARKET', 
#    'side': 'SELL', 
#    'fills': [{'price': '0.188', 'qty': '99', 'commission': '0.018612', 'commissionAsset': 'USDT'}], 
#    'isIsolated': True
#}