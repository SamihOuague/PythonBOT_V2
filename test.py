import json
from lib.Prototype import Prototype

def priceActionSell(candles, analysis):
    score = 0
    candle = candles[-1]
    if (analysis.invertedHammer(candle) or analysis.hammer(candle)):
        score += 1
    if (analysis.mobileAverage(99) < candle[1]):
        score += 1
    if (analysis.mobileAverage(25) < analysis.mobileAverage(99)):
        score += 1
    lastVolume = candle
    volumeScore = 0
    for i in range(2, 10):
        c = candles[0-i]
        if (lastVolume[5] > c[5] and lastVolume[4] < c[4]):
            lastVolume = c
            volumeScore += 1
        else:
            break
    
    if (volumeScore >= 3):
        score += 2

    if score >= 3:
        return True
    return False


dataset = [[float(x) for x in d] for d in json.loads(open("dataset1M.json").read())]

proto = Prototype("CHZUSDT", dataset[0:100], False, priceActionSell, 0.01, 0.01)


for i in range(100, len(dataset)):
    proto.run(dataset[i])

print((proto.win + proto.loss))
print("TAUX DE REUSSITE {}%".format(round((proto.win / (proto.win + proto.loss)) * 100)))
print("{} CHZ, {} USDT".format(round(proto.baseAsset, 2), round(proto.quoteAsset, 2)))