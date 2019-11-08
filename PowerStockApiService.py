import datetime

from pathlib import Path

import numpy

import pandas as pd

def getMaxDateCount():
    return 100

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

def getStockFilePath(stockId):
    return './' + 'tw_' + str(stockId) + '.csv'

def isStockCsvFileExist(stockId):
    stockFilePath = getStockFilePath(stockId)
    return isCsvFileExist(stockFilePath)

def isCsvFileExist(path):
    my_file = Path(path)
    return my_file.is_file()

def addNewStockData(timeDate, stockId, price, value):
    stockCsvFilePath = getStockFilePath(stockId)

    if isStockCsvFileExist(stockId) == False:
        # Create a new csv file
        stockData = {'date' : timeDate, 'price': [price], 'value' : [value] }
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
    top_row = pd.DataFrame({'date':[timeDate],'price':[price],'value':[value]})
    df = pd.concat([top_row, df], sort=True).reset_index(drop=True)
    df = df.drop(columns='Unnamed: 0')

    # Remove the last data when count is bigger than max
    if len(df) > getMaxDateCount():
        df = df.drop(df.index[len(df)-1])

    # Store the csv file
    df.to_csv(stockCsvFilePath , encoding='utf-8')
    
