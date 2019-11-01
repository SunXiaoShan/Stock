import requests
import pandas as pd

def getStockNumListUrl():
    # strMode=2 就是上市，而 strMode=4 就是上櫃
    return 'http://isin.twse.com.tw/isin/C_public.jsp?strMode=2'

def getStockIdList():
    res = requests.get(getStockNumListUrl())
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

    data = { 'id' : stockIdList, 'name' : stockNameList }
    return data

def storeStockIdListToCsvFile(stockIdDataList, path):
    df = pd.DataFrame(stockIdDataList)
    df.to_csv(path, encoding='utf-8')