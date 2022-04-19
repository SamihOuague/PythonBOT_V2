def drawSquare(width, height):
    borderBottomLeft = chr(9565)
    borderWidth = chr(9552)
    borderheight = chr(9567)
    width = width * 2
    finalTable = []
    for h in range(height):
        line = ""
        for w in range(width):
            if h == height - 1:
                if w == width - 1:
                    line += borderBottomLeft
                else:
                    line += borderWidth
            else:
                if w == width - 1:
                    line += borderheight
                else:
                    line += " "

        finalTable.append(line)
    return finalTable


def getLimits(candles):
    higher = round(candles[0][2], 4)
    lower = round(candles[0][3], 4)
    for c in candles:
        if c[2] > higher:
            higher = c[2]
        elif c[3] < lower:
            lower = c[3]

    lower = round(lower * 10000)
    higher = round(higher * 10000)
    while (lower % 5 != 0 or higher % 5 != 0):
        if (lower % 5):
            lower -= 1
        elif (higher % 5):
            higher += 1
    return [round(higher), round(lower)]

def getIntervalBlock(candle):
    high = candle[2]
    low =  candle[3]
    output = []
    if (candle[1] >= candle[4]):
        output = [candle[1], candle[4]]
    else:
        output = [candle[4], candle[1]]
    output.append(high)
    output.append(low)
    return output

def drawChart(candles):
    lenC = len(candles)
    candles = [[float(x) for x in c[0:6]] for c in candles]

    limits = getLimits(candles)
    emptyTable = drawSquare(lenC, (limits[0] - limits[1]))

    monoStickBottom = chr(9589)
    monoStickTop = chr(9591)
    doubleStick = chr(9474)

    doubleBlock = chr(9608)
    topBlock = chr(9604)
    bottomBlock = chr(9600)
    noneBlock = chr(9472)


    noneBlockStick = chr(9532)
    noneBlockStickBottom = chr(9524)
    noneBlockStickTop = chr(9516)

    for i in range(limits[1], limits[0]):
        pos = limits[1] - (i - limits[1]) + (limits[0] - limits[1] - 1)
        printable = False
        if i != (limits[0] - 1):
            printable = True
        i = i - limits[1]
        nbr = " " + str(pos)
        emptyTable[i] = emptyTable[i] + nbr
        if printable:
            char = "          "
            for c in range(0, len(emptyTable[i])):
                lenTable = len(emptyTable[i]) - 6
                linePrice = int(pos)/10000
                if c < lenTable and c % 2 == 0:
                    if candles[round(c/2)][2] >= linePrice and candles[round(c/2)][3] <= linePrice:
                        intvl = getIntervalBlock(candles[round(c/2)])
                        high = intvl[2]
                        low =  intvl[3]
                        if (candles[round(c/2)][1] <= candles[round(c/2)][4]):
                            char += "\033[32m"
                        else:
                            char += "\033[31m"
                        if candles[round(c/2)][1] == candles[round(c/2)][4] and linePrice <= intvl[0] and linePrice >= intvl[1]:
                            if (high - low) == 0:
                                char += noneBlock
                            elif low == candles[round(c/2)][1]:
                                char += noneBlockStickBottom
                            elif high == candles[round(c/2)][1]:
                                char += noneBlockStickTop
                            else:
                                char += noneBlockStick
                        else:
                            if linePrice == high:
                                if linePrice <= intvl[0] and linePrice >= intvl[1] and linePrice % 2 != 0:
                                    char += topBlock
                                else:
                                    char += monoStickTop
                            elif linePrice == low:
                                if linePrice <= intvl[0] and linePrice >= intvl[1] and linePrice % 2 != 0:
                                    char += bottomBlock
                                else:
                                    char += monoStickBottom
                            else:
                                if linePrice <= intvl[0] and linePrice >= intvl[1]:
                                    char += doubleBlock
                                else:
                                    char += doubleStick
                    else:
                        char += emptyTable[i][c]
                    char += "\033[39m"
                else:
                    char += emptyTable[i][c]
            #print((int(char[-4:])/10000))
            print(char)
        else:
            print("         ", emptyTable[i])


