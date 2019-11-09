import datetime

from pathlib import Path

import numpy

import pandas as pd

import os

from StockListService import getStockList

import json
import requests

import time

# MARK: -

def getMaxDateCount():
    return 100

def getMaxBackupDateCount():
    return 365

def getRequestStockDataApiSleepTime():
    return 10

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

# MARK: -

def getStockDataFolderPath():
    return './StockData'

def isStockFolderExist():
    path = getStockDataFolderPath()
    return os.path.isdir(path)

def createStockFolder():
    path = getStockDataFolderPath()
    os.mkdir(path)

# MARK: -

def addNewStockData(timeDate, stockId, price, value, highPrice=-1, lowPrice=-1, numberOfTransactions=-1):
    
    if isStockFolderExist() == False:
        createStockFolder()
    
    stockCsvFilePath = getStockFilePath(stockId)

    if isStockCsvFileExist(stockId) == False:
        # Create a new csv file
        stockData = {
            'date' : timeDate, 
            'price': [price], 
            'value' : [value],
            'numberOfTransactions' : [numberOfTransactions],
            'highPrice' : [highPrice],
            'lowPrice' : [lowPrice]
            }
        df = pd.DataFrame(stockData)
        df.to_csv(stockCsvFilePath , encoding='utf-8')
        return

    # Load the csv file
    df = pd.read_csv(stockCsvFilePath)
    topDate = df['date'].values[0]
    timeDate = numpy.int64(timeDate)

    # Detect the data is exist, isn't it?
    if timeDate <= topDate:
        return

    # insert to the top row
    top_row = pd.DataFrame({
        'date':[timeDate],
        'price':[price],
        'value':[value],
        'numberOfTransactions' : [numberOfTransactions],
        'highPrice' : [highPrice],
        'lowPrice' : [lowPrice]
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
    whiteStockIdSet = set(whiteStockIdList)
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
        topDate = numpy.int64(df['date'].values[0])
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
    url += '&type=ALL'

    res = requests.get(url)
    json_data = json.loads(res.text)

    if json_data['stat'] == '很抱歉，沒有符合條件的資料!':
        print("Power - %s 沒有符合條件的資料" % str(dateTime))
        return

    stockDataList = json_data['data9']

    for stockData in stockDataList:

        stockId = stockData[0]
        stockValue = stockData[2]
        stockPrice = stockData[8]
        numberOfTransactions = stockData[3]
        stockHigh = stockData[6]
        stockLow = stockData[7]

        isVailedStockData = str(stockId) in stockIdSet
        if isVailedStockData == False:
            continue

        addNewStockData( 
                         str(dateTime), 
                         stockId, 
                         stockPrice, 
                         stockValue, 
                         stockHigh, 
                         stockLow, 
                         numberOfTransactions
                        )