import requests

def requestStockInfoData(url):
    res = requests.get(url)
    stockJson = res.json()
    #TODO: handle error
    return stockJson

def getStockNumber(stockJsonData):
    # 股票代號
    return stockJsonData['c']

def getStockName(stockJsonData):
    # 公司全名
    return stockJsonData['nf']

def getStockCurrentPrice(stockJsonData):
    # 當盤成交價
    return stockJsonData['z']

def getStockCurrentTransactionCount(stockJsonData):
    # 當盤成交量
    return stockJsonData['tv']

def getStockTransactionCount(stockJsonData):
    # 累積成交量
    return stockJsonData['v']

def getStockStartPrice(stockJsonData):
    # 開盤
    return stockJsonData['o']

def getStockCurrentHighPrice(stockJsonData):
    # 最高
    return stockJsonData['h']

def getStockCurrentLowPrice(stockJsonData):
    # 最低
    return stockJsonData['l']

def getStockYesterdayPrice(stockJsonData):
    # 昨收
    return stockJsonData['y']

