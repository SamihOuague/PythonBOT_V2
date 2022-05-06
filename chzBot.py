from lib.Prototype import Prototype

def priceActionSell(candles, analysis):
    candle = candles[-1]
    lastVolume = candle
    volumeScore = 0
    for i in range(2, 10):
        c = candles[0-i]
        if (lastVolume[5] > c[5] and lastVolume[4] < c[4]):
            lastVolume = c
            volumeScore += 1
        else:
            break
    
    if (volumeScore >= 2 and analysis.mobileAverage(7) < c[4] and analysis.mobileAverage(99) > c[4]):
        return True
    return False

proto = Prototype("CHZUSDT", False, priceActionSell, 0.01, 0.01)
print(proto.manager.wallet)
proto.run()