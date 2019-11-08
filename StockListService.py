import requests
import pandas as pd

from pathlib import Path

# MARK: - public get stock data list

# string type
def getStockList():
    if isStockCsvFileExist():
        return loadStockCsvFile()

    stockListData = requestStockIdList()
    storeStockIdListToCsvFile(stockListData)
    return stockListData

# MARK: - TODO

def getWhiteStockList():
    stockIdList = [
    ]
    stockNameList = [
    ] 

    data = { 'id' : stockIdList, 'name' : stockNameList }
    return

def getBlackStockIdList():
    stockIdList = [
    ]
    return stockIdList

def getHighLightStockIdList():
    stockIdList = [
    ]
    return stockIdList

# MARK: -

def getStockNumListUrl():
    # strMode=2 就是上市，而 strMode=4 就是上櫃
    return 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=2'

def requestStockIdList(url=getStockNumListUrl()):
    res = requests.get(url)
    # get the first table
    df = pd.read_html(res.text)[0]

    # 讓 column 的數量 -1，只留內容
    df.columns = df.iloc[0]

    # 刪除第一行
    df = df.iloc[1:]

    # 先移除row，再移除column，超過三個NaN則移除
    df = df.dropna(thresh=3, axis=0).dropna(thresh=3, axis=1)

    stockData = df['有價證券代號及名稱'].str.split('\u3000')
    stockIdList = []
    stockNameList = []
    for stock in stockData:
        if len(stock) < 2:
            continue
        stockIdList.append(stock[0])
        stockNameList.append(stock[1])

        if '9958' == stock[0]:
            break

    data = { 'id' : stockIdList, 'name' : stockNameList }
    return data

def getStockListCsvFilePath():
    return './stock_list.csv'

def storeStockIdListToCsvFile(stockIdDataList, path=getStockListCsvFilePath()):
    df = pd.DataFrame(stockIdDataList)
    df.to_csv(path, encoding='utf-8')

def isStockCsvFileExist(path=getStockListCsvFilePath()):
    my_file = Path(path)
    return my_file.is_file()

def loadStockCsvFile(path=getStockListCsvFilePath()):
    df = pd.read_csv(path)
    strIdList = list(map(str, df['id'].values))
    data = { 'id' : strIdList, 'name' : df['name'].values }
    return data

# MARK: -

def getStockMaxCount():
    return 150

def getStockUrlList(stockIdList=getStockList()['id'], maxCount=getStockMaxCount()):
    stockInfoUrlList = []
    index = 0
    basicUrl = 'http://mis.twse.com.tw/stock/api/getStockInfo.jsp' + '?ex_ch='
    for stockId in stockIdList:
        urlArrayIndex = int(index / maxCount)
        if (index % maxCount) == 0:
            firstData = 'tse_' + str(stockId) + '.tw'
            stockInfoUrlList.append(basicUrl + firstData)
        else:
            url = stockInfoUrlList[urlArrayIndex]
            url = url + '|' + 'tse_' + str(stockId) + '.tw'
            stockInfoUrlList[urlArrayIndex] = url
    
        index += 1

    return stockInfoUrlList

# MARK: -



