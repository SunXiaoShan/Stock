import datetime

from pathlib import Path

import numpy

import pandas as pd

import os

from StockListService import getStockList

import json
import requests

import time

import enum

# MARK: -

class StockApiKey:
    StockId = 0
    StockName = 1
    StockValue = 2
    NumberOfTransactions = 3
    DealPrice = 4
    StockStartPrice = 5
    StockHigh = 6
    StockLow = 7
    StockLastPrice = 8
    StockSpread = 10
    StockEPS = 15

class StockDataKey:
    TimeDate = "日期"
    StockId = "證券代號"
    StockName = "證券名稱"
    StockValue = "成交股數"
    NumberOfTransactions = "成交筆數"
    DealPrice = "成交金額"
    StockStartPrice = "開盤價"
    StockHigh = "最高價"
    StockLow = "最低價"
    StockLastPrice = "收盤價"
    StockSpread = "漲跌價差"
    StockEPS = "本益比"

# MARK: -

class StockMarketIndexApiKey:
    StockMarketIndexValue = 0
    CloseIndex = 1
    DiffIndex = 2
    DiffRatio = 3
    DiffPercent = 4

class StockMarketIndexKey:
    TimeDate = "日期"
    StockMarketIndexValue = '指數'
    CloseIndex = '收盤指數'
    DiffIndex = '漲跌(+/-)'
    DiffRatio = '漲跌點數'
    DiffPercent = '漲跌百分比(%)'

# MARK: -

def getMaxDateCount():
    return 100

def getMaxBackupDateCount():
    return 365

def getRequestStockDataApiSleepTime():
    return 30

# MARK: -

# current to past
def getDateTimeList(timedelta=getMaxDateCount()):
    dateList = []

    # for i in range(timedelta, -1, -1):
    for i in range(timedelta):
        time = datetime.datetime.now() - datetime.timedelta(days=i)
        strTime = time.strftime("%Y%m%d")
        dateList.append(strTime)

    return dateList

# past to current
def getReversedDateTimeList(timedelta=getMaxDateCount()):
    timeList = getDateTimeList(timedelta)
    return reversed(timeList)

# MARK: -

def getStockFilePath(stockId):
    return './StockData/' + 'tw_' + str(stockId) + '.csv'

def isStockCsvFileExist(stockId):
    stockFilePath = getStockFilePath(stockId)
    return isCsvFileExist(stockFilePath)

def isCsvFileExist(path):
    my_file = Path(path)
    return my_file.is_file()

def getStockDataFolderPath():
    return './StockData'

def isStockFolderExist():
    path = getStockDataFolderPath()
    return os.path.isdir(path)

def createStockFolder():
    path = getStockDataFolderPath()
    os.mkdir(path)

# MARK: -

def getStockMarketIndexFilePath(stockId):
    return './StockMarketIndexData/' + 'tw_' + str(stockId) + '.csv'

def isStockMarketIndexCsvFileExist(stockId):
    stockFilePath = getStockMarketIndexFilePath(stockId)
    return isCsvFileExist(stockFilePath)

def getStockMarketIndexFolderPath():
    return './StockMarketIndexData'

def isStockMarketIndexFolderExist():
    path = getStockMarketIndexFolderPath()
    return os.path.isdir(path)

def createStockMarketIndexFolder():
    path = getStockMarketIndexFolderPath()
    os.mkdir(path)

# MARK: -

def addNewStockData(timeDate, 
                    stockId, 
                    stockName,
                    stockValue,
                    numberOfTransactions,
                    dealPrice,
                    startPrice, 
                    stockHigh,
                    stockLow,
                    stockLastPrice,
                    stockSpread,
                    stockEps):

    if isStockFolderExist() == False:
        createStockFolder()

    stockCsvFilePath = getStockFilePath(stockId)

    if isStockCsvFileExist(stockId) == False:
        # Create a new csv file
        stockData = {
            StockDataKey.TimeDate : [timeDate],
            StockDataKey.StockId : [stockId],
            StockDataKey.StockName : [stockName],
            StockDataKey.StockValue : [stockValue],
            StockDataKey.NumberOfTransactions : [numberOfTransactions],
            StockDataKey.DealPrice : [dealPrice],
            StockDataKey.StockStartPrice : [startPrice],
            StockDataKey.StockHigh : [stockHigh],
            StockDataKey.StockLow : [stockLow],
            StockDataKey.StockLastPrice : [stockLastPrice],
            StockDataKey.StockSpread : [stockSpread],
            StockDataKey.StockEPS : [stockEps]
            }
        df = pd.DataFrame(stockData)
        df.to_csv(stockCsvFilePath , encoding='utf-8')
        return

    # Load the csv file
    df = pd.read_csv(stockCsvFilePath)
    topDate = df[StockDataKey.TimeDate].values[0]
    timeDate = numpy.int64(timeDate)

    # Detect the data is exist, isn't it?
    if timeDate <= topDate:
        return

    # insert to the top row
    top_row = pd.DataFrame({
            StockDataKey.TimeDate : [timeDate],
            StockDataKey.StockId : [stockId],
            StockDataKey.StockName : [stockName],
            StockDataKey.StockValue : [stockValue],
            StockDataKey.NumberOfTransactions : [numberOfTransactions],
            StockDataKey.DealPrice : [dealPrice],
            StockDataKey.StockStartPrice : [startPrice],
            StockDataKey.StockHigh : [stockHigh],
            StockDataKey.StockLow : [stockLow],
            StockDataKey.StockLastPrice : [stockLastPrice],
            StockDataKey.StockSpread : [stockSpread],
            StockDataKey.StockEPS : [stockEps]
            })
    df = pd.concat([top_row, df], sort=True).reset_index(drop=True)
    df = df.drop(columns='Unnamed: 0')

    # Remove the last data when count is bigger than max
    if len(df) > getMaxBackupDateCount():
        df = df.drop(df.index[len(df)-1])

    # Store the csv file
    df.to_csv(stockCsvFilePath , encoding='utf-8')
    
# MARK: -

def getStockIdSet():
    whiteStockList = getStockList()
    whiteStockIdList = whiteStockList['id']
    _list = []
    whiteStockIdSet = set(_list)
    return whiteStockIdSet

# MARK: -

def requestAllStockDatasWithTimeList(dateTimeList=getReversedDateTimeList(), stockIdSet=getStockIdSet()):
    sleepTime = getRequestStockDataApiSleepTime()

    print("Power - requestAllStockDatasWithTimeList start")
    for dataTime in dateTimeList:
        if isStockCsvFileExist(1101) == False:
            requestAllStockDatas(dataTime)

            print("Power - %s done" % str(dataTime))
            time.sleep(sleepTime)
            continue
        
        stockCsvFilePath = getStockFilePath(1101)
        df = pd.read_csv(stockCsvFilePath)
        topDate = numpy.int64(df[StockDataKey.TimeDate].values[0])
        dataTime = numpy.int64(dataTime)

        if dataTime <= topDate:
            print("Power - %s pass" % str(dataTime))
            continue

        requestAllStockDatas(dataTime, stockIdSet)
        print("Power - %s done" % str(dataTime))
        time.sleep(sleepTime)

    print("Power - requestAllStockDatasWithTimeList end")

def requestAllStockDatas(dateTime, stockIdSet=getStockIdSet()):
    url = 'https://www.twse.com.tw/exchangeReport/MI_INDEX'
    url += '?'
    url += 'date=' + str(dateTime)
    url += '&response=json'
    url += '&type=ALLBUT0999'

    res = requests.get(url)
    json_data = json.loads(res.text)

    if json_data['stat'] == '很抱歉，沒有符合條件的資料!':
        print("Power - %s 沒有符合條件的資料" % str(dateTime))
        return

    stockDataList = json_data['data9']

    for stockData in stockDataList:
        stockId = stockData[StockApiKey.StockId]
        stockName = stockData[StockApiKey.StockName]
        stockValue = stockData[StockApiKey.StockValue]
        numberOfTransactions = stockData[StockApiKey.NumberOfTransactions]
        dealPrice = stockData[StockApiKey.DealPrice]
        startPrice = stockData[StockApiKey.StockStartPrice]
        stockHigh = stockData[StockApiKey.StockHigh]
        stockLow = stockData[StockApiKey.StockLow]
        stockLastPrice = stockData[StockApiKey.StockLastPrice]
        stockSpread = stockData[StockApiKey.StockSpread]
        stockEps = stockData[StockApiKey.StockEPS]

        # Remove the stock filter
        # isVailedStockData = str(stockId) in stockIdSet
        # if isVailedStockData == False:
        #     continue

        addNewStockData( 
                         str(dateTime), 
                         stockId, 
                         stockName,
                         stockValue,
                         numberOfTransactions,
                         dealPrice,
                         startPrice,
                         stockHigh,
                         stockLow,
                         stockLastPrice,
                         stockSpread,
                         stockEps
                        )

def requestAllStockMarketIndexWithTimeList(dateTimeList=getReversedDateTimeList()):
    sleepTime = getRequestStockDataApiSleepTime()

    print("Power market index - requestAllStockMarketIndexWithTimeList start")
    for dataTime in dateTimeList:
        if isStockMarketIndexCsvFileExist('發行量加權股價指數') == False:
            requestStockMarketIndex(dataTime)

            print("Power market index - %s done" % str(dataTime))
            time.sleep(sleepTime)
            continue
        
        stockCsvFilePath = getStockMarketIndexFilePath('發行量加權股價指數')
        df = pd.read_csv(stockCsvFilePath)
        topDate = numpy.int64(df[StockMarketIndexKey.TimeDate].values[0])
        dataTime = numpy.int64(dataTime)

        if dataTime <= topDate:
            print("Power market index - %s pass" % str(dataTime))
            continue

        requestStockMarketIndex(dataTime)
        print("Power market index - %s done" % str(dataTime))
        time.sleep(sleepTime)

    print("Power market index - requestAllStockMarketIndexWithTimeList end")

def requestStockMarketIndex(dateTime):
    url = 'https://www.twse.com.tw/exchangeReport/MI_INDEX'
    url += '?'
    url += 'date=' + str(dateTime)
    url += '&response=json'
    url += '&type=IND'

    res = requests.get(url)
    json_data = json.loads(res.text)

    if json_data['stat'] == '很抱歉，沒有符合條件的資料!':
        print("Power - %s 沒有符合條件的資料" % str(dateTime))
        return

    stockMarketIndexList = json_data['data1']

    for stockMarketIndexData in stockMarketIndexList:
        stockMarketIndex = stockMarketIndexData[StockMarketIndexApiKey.StockMarketIndexValue]
        closeIndex = stockMarketIndexData[StockMarketIndexApiKey.CloseIndex]
        diffIndex = stockMarketIndexData[StockMarketIndexApiKey.DiffIndex]
        diffRatio = stockMarketIndexData[StockMarketIndexApiKey.DiffRatio]
        diffPercent = stockMarketIndexData[StockMarketIndexApiKey.DiffPercent]

        addNewStockMarketIndexData(
            str(dateTime),
            stockMarketIndex,
            closeIndex,
            diffIndex,
            diffRatio,
            diffPercent
        )


def addNewStockMarketIndexData(timeDate, 
                               stockMarketIndex, 
                               closeIndex,
                               diffIndex,
                               diffRatio,
                               diffPercent):

    if isStockMarketIndexFolderExist() == False:
        createStockMarketIndexFolder()

    stockCsvFilePath = getStockMarketIndexFilePath(stockMarketIndex)

    if isStockMarketIndexCsvFileExist(stockMarketIndex) == False:
        # Create a new csv file
        stockData = {
            StockMarketIndexKey.TimeDate : [timeDate],
            StockMarketIndexKey.StockMarketIndexValue : [stockMarketIndex],
            StockMarketIndexKey.CloseIndex : [closeIndex],
            StockMarketIndexKey.DiffIndex : [diffIndex],
            StockMarketIndexKey.DiffRatio : [diffRatio],
            StockMarketIndexKey.DiffPercent : [diffPercent]
            }
        df = pd.DataFrame(stockData)
        df.to_csv(stockCsvFilePath , encoding='utf-8')
        return

    # Load the csv file
    df = pd.read_csv(stockCsvFilePath)
    topDate = df[StockMarketIndexKey.TimeDate].values[0]
    timeDate = numpy.int64(timeDate)

    # Detect the data is exist, isn't it?
    if timeDate <= topDate:
        return

    # insert to the top row
    top_row = pd.DataFrame({
            StockMarketIndexKey.TimeDate : [timeDate],
            StockMarketIndexKey.StockMarketIndexValue : [stockMarketIndex],
            StockMarketIndexKey.CloseIndex : [closeIndex],
            StockMarketIndexKey.DiffIndex : [diffIndex],
            StockMarketIndexKey.DiffRatio : [diffRatio],
            StockMarketIndexKey.DiffPercent : [diffPercent]
            })
    df = pd.concat([top_row, df], sort=True).reset_index(drop=True)
    df = df.drop(columns='Unnamed: 0')

    # Remove the last data when count is bigger than max
    if len(df) > getMaxBackupDateCount():
        df = df.drop(df.index[len(df)-1])

    # Store the csv file
    df.to_csv(stockCsvFilePath , encoding='utf-8')