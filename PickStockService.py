import numpy

import pandas as pd

import os

def translateEmptyStringToZero(value):
    if type(value) != str:
        return value
    
    if value == '--':
        return '0'
    
    return value.replace(',', '')

def getDay20Ma(priceList):
    DAYS = 20
    sum = 0.0
    for i in range(DAYS):
        if i >= len(priceList):
            continue
        strprice = translateEmptyStringToZero(priceList[i])
        sum += float(strprice)
    result = sum / DAYS
    return result

def getDay100Ma(priceList):
    DAYS = 100
    sum = 0.0
    for i in range(DAYS):
        if i >= len(priceList):
            continue
        strprice = translateEmptyStringToZero(priceList[i])
        sum += float(strprice)
    result = sum / DAYS
    return result

def getLastWeekValue(valueList):
    DAYS = 5
    sum = 0.0
    for i in range(DAYS):
        strvalue = translateEmptyStringToZero(str(valueList[i]))
        sum += float(strvalue)
    result = sum / DAYS
    return result

def getPreviousWeekValue(valueList):
    DAYS = 5
    sum = 0.0
    for i in range(DAYS, 2 * DAYS):
        if i + DAYS >= len(valueList):
            continue
        strvalue = translateEmptyStringToZero(str(valueList[i]))
        sum += float(strvalue)
    result = sum / DAYS
    return result

def debugTool(topDate, stockId, stockName, lastPrice, lastStockHigh, lastStockLow,
lastStockValue, lastWeekVaule, previousStockHigh, previousStockLow, previousStockValue,
day20ma, day100ma, previousWeekValue, rate):
    message = '{ ' + '\n'
    message = message + '\t' + '最後一天日期 : ' + str(topDate) + '\n' 
    message = message + '\t' + '股票 : ' + str(stockId) + '\n'
    message = message + '\t' + '股票名稱 : ' + str(stockName) + '\n'
    message = message + '\t' + '收盤價 : ' + str(lastPrice) + '\n'
    message = message + '\t' + '高點 : ' + str(lastStockHigh) + '\n'
    message = message + '\t' + '低點 : ' + str(lastStockLow) + '\n'
    message = message + '\t' + '交易量 : ' + str(lastStockValue) + '\n'
    message = message + '\t' + '周交易量 : ' + str(lastWeekVaule) + '\n'
    message = message + '\t' + '前一日高 : ' + str(previousStockHigh) + '\n'
    message = message + '\t' + '前一日低 : ' + str(previousStockLow) + '\n'
    message = message + '\t' + '前一日交易量 : ' + str(previousStockValue) + '\n'
    message = message + '\t' + '日 20 ma : ' + str(day20ma) + '\n'
    message = message + '\t' + '週 20 ma(日 100 ma) : ' + str(day100ma) + '\n'
    message = message + '\t' + '前一週交易量 : ' + str(previousWeekValue) + '\n'
    message = message + '\t' + '交易量比 : ' + str(rate) + '\n'
    message = message + '}' + '\n'

    print(message)


def isVailedStock(csvFileName):
    from PowerStockApiService import StockDataKey
    
    path = './StockData/' + csvFileName
    df = pd.read_csv(path)

    # current data
    topDate = numpy.int64(df[StockDataKey.TimeDate].values[0])
    
    stockId = df[StockDataKey.StockId].values[0]
    stockName = df[StockDataKey.StockName].values[0]
    
    strLastPrice = translateEmptyStringToZero(str(df[StockDataKey.StockLastPrice].values[0]))
    lastPrice = float(strLastPrice)

    strlastStockHigh = translateEmptyStringToZero(df[StockDataKey.StockHigh].values[0])
    lastStockHigh = float(strlastStockHigh)

    strlastStockLow = translateEmptyStringToZero(df[StockDataKey.StockLow].values[0])
    lastStockLow = float(strlastStockLow)

    strlastStockValue = translateEmptyStringToZero(str(df[StockDataKey.StockValue].values[0]))
    lastStockValue = float(strlastStockValue)

    lastWeekVaule = getLastWeekValue(df[StockDataKey.StockValue].values)

    # previous data
    strpreviousStockHigh = translateEmptyStringToZero(df[StockDataKey.StockHigh].values[1])
    previousStockHigh = float(strpreviousStockHigh)

    strpreviousStockLow = translateEmptyStringToZero(df[StockDataKey.StockLow].values[1])
    previousStockLow = float(strpreviousStockLow)

    strpreviousStockValue = translateEmptyStringToZero(str(df[StockDataKey.StockValue].values[1]))
    previousStockValue = float(strpreviousStockValue)

    # ma data
    day20ma = getDay20Ma(df[StockDataKey.StockLastPrice].values)
    day100ma = getDay100Ma(df[StockDataKey.StockLastPrice].values)
    previousWeekValue = getPreviousWeekValue(df[StockDataKey.StockValue].values)

    if lastStockHigh <= lastStockLow:
        return ''
    
    if lastStockHigh <= day100ma:
        return ''

    if lastStockLow <= day100ma:
        return ''

    if previousStockHigh > day100ma and previousStockLow > day100ma:
        return ''
    
    #TODO: check the stock file
    if previousStockValue == 0:
        return ''

    rate = float(lastStockValue) / float(previousStockValue)
    if rate < 1:
        return ''

    debugTool(topDate, stockId, stockName, lastPrice, lastStockHigh, lastStockLow,
lastStockValue, lastWeekVaule, previousStockHigh, previousStockLow, previousStockValue,
day20ma, day100ma, previousWeekValue, rate)
    
    return stockId

def getVailedStockIdList():
    csvFileNameList = [x for x in os.listdir('./StockData') if x.endswith(".csv")]

    result = []
    for fileName in csvFileNameList:
        stockId = isVailedStock(fileName)
        if stockId == '':
            continue

        result.append(stockId)
    return result



print(getVailedStockIdList())
    












