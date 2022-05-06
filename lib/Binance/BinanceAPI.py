import hashlib
import hmac
import json
import requests
from time import time

class BinanceAPI:
    def __init__(self):
        self.config = json.loads(open("./BinanceConfig.json", "r").read())
        self.url = "https://api.binance.com/api/v3"
        self.urlV1 = "https://api.binance.com/sapi/v1"

    def getCandles(self, symbol, period = "1m", start = ""):
        url = self.url + "/klines?symbol={}&interval={}".format(symbol, period)
        if start != "":
            url = url + "&startTime={}".format(start)
        return requests.get(url).json()

    def getAccounts(self, accountType = "spot", symbols = "CHZUSDT"):
        if (accountType == "spot"):
            url = self.url + "/account"
        elif (accountType == "margin"):
            url = self.urlV1 + "/margin/account"
        elif (accountType == "isolated"):
            url = self.urlV1 + "/margin/isolated/account"
        else:
            return False
        if accountType == "isolated":
            sign = "timestamp=" + str(round((time() - 1) * 1000)) + "&symbols=" + symbols
        else:
            sign = "timestamp=" + str(round((time() - 1) * 1000))
        h = self.genHmacKey(sign)
        url = url + "?" + sign + "&signature=" + h
        return requests.get(url, headers={"X-MBX-APIKEY": self.config["key"]}).json()

    def getAccount(self, symbol, accountType = "spot"):
        if (accountType == "spot"):
            accounts = self.getAccounts()["balances"]
        elif (accountType == "margin"):
            accounts = self.getAccounts("margin")["userAssets"]
        try:
            for account in accounts:
                if account["asset"] == symbol:
                    return account
        except:
            return 0
        return 0

    def createOrder(self, side, size, symbol = "CHZUSDT"):
        url = self.url + "/order?"
        sign = "timestamp=" + str(round((time() - 1) * 1000)) + "&symbol=" + symbol + "&type=market&side=" + side
        if (side == "buy"):
            sign = sign + "&quoteOrderQty="+ str(round(size - 1))
        else:
            sign = sign + "&quantity=" + str(round(size - 1))
        h = self.genHmacKey(sign)
        url = url+sign+"&signature="+h
        return requests.post(url, headers={"X-MBX-APIKEY": self.config["key"]}).json()

    def createMarginOrder(self, side, size, symbol = "CHZUSDT"):
        url = self.urlV1 + "/margin/order?"
        sign = "isIsolated=TRUE&timestamp=" + str(round((time() - 1) * 1000)) + "&symbol=" + symbol + "&type=MARKET&side=" + side
        if (side == "BUY"):
            sign = sign + "&quoteOrderQty="+ str(round(size))
        else:
            sign = sign + "&quantity=" + str(round(size))
        h = self.genHmacKey(sign)
        url = url+sign+"&signature="+h
        return requests.post(url, headers={"X-MBX-APIKEY": self.config["key"]}).json()

    def genHmacKey(self, sign):
        return hmac.new(bytes(self.config["secret"], "utf-8"), bytes(sign, "utf-8"), hashlib.sha256).hexdigest()

    def ticker(self, symbol = "CHZUSDT"):
        return requests.get(self.url + "/ticker/price?symbol="+symbol).json()