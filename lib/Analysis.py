class Analysis:
    def __init__(self, candles):
        self.candles = candles

    def getCandle(self, pos):
        return self.candles[pos]

    def setCandles(self, candles):
        self.candles = candles

    def mobileAverage(self, period = 7):
        candles = self.candles[(len(self.candles) - period):len(self.candles)]
        sum = 0
        for c in candles:
            sum += float(c[4])
        return round(sum/(period), 4)
    
    def candleData(self, pos):
        return [float(x) for x in self.candles[pos][1:6]]

    def trendRate(self, period = 14):
        candles = self.candles
        diffCandles = [(x[4] * 10000) - (x[1] * 10000) for x in candles[-1 * (period):]]
        return sum(diffCandles)
    
    def invertedHammer(self, candle):
        lastCandle = candle
        highLowDiff = lastCandle[2] - lastCandle[3]
        openCloseDiff = lastCandle[4] - lastCandle[1]
        if (openCloseDiff < 0):
            openCloseDiff = -1 * openCloseDiff
        if ((lastCandle[4] == lastCandle[2] or lastCandle[1] == lastCandle[2] ) \
            and ((openCloseDiff * 4) <= highLowDiff and openCloseDiff > 0)):
            return True
        return False

    def hammer(self, candle):
        lastCandle = candle
        highLowDiff = lastCandle[2] - lastCandle[3]
        openCloseDiff = lastCandle[4] - lastCandle[1]
        if (openCloseDiff < 0):
            openCloseDiff = -1 * openCloseDiff
        if ((lastCandle[4] == lastCandle[3] or lastCandle[1] == lastCandle[3]) \
            and ((openCloseDiff * 4) <= highLowDiff and openCloseDiff > 0)):
            return True
        return False