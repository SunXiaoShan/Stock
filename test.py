# import pandas as pd

# data = {'name': ['1102　台泥2', '1103　台泥3', '1104　台泥4', '1105　台泥5', '1106　台泥6'], 
#         'year': [2012, 2012, 2013, 2014, 2014], 
#         'reports': [4, 24, 31, 2, 3]}
# df = pd.DataFrame(data, index = ['Cochice', 'Pima', 'Santa Cruz', 'Maricopa', 'Yuma'])

# tt = df['name'].str.split('\u3000')
# idList = []
# nameList = []
# for i in tt:
#     idList.append(i[0])
#     nameList.append(i[1])

# data['id'] = idList
# data['nn'] = nameList

# df = pd.DataFrame(data, index = ['Cochice', 'Pima', 'Santa Cruz', 'Maricopa', 'Yuma'])


# print(df)

# exit()

# import requests
# import pandas as pd

# # strMode=2 就是上市，而 strMode=4 就是上櫃
# res = requests.get("http://isin.twse.com.tw/isin/C_public.jsp?strMode=2")
# df = pd.read_html(res.text)[0]

# # 讓 column 的數量 -1，只留內容
# df.columns = df.iloc[0]

# # 刪除第一行
# df = df.iloc[1:]

# # 先移除row，再移除column，超過三個NaN則移除
# df = df.dropna(thresh=3, axis=0).dropna(thresh=3, axis=1)

# stockData = df['有價證券代號及名稱'].str.split('\u3000')
# stockIdList = []
# stockNameList = []
# for stock in stockData:
#     if len(stock) < 2:
#         continue
#     stockIdList.append(stock[0])
#     stockNameList.append(stock[1])

# data = { 'id' : stockIdList, 'name' : stockNameList }
# df = pd.DataFrame(data)

# df.to_csv(r'~/Desktop/StockPython/test.csv', encoding='utf-8')

# exit()

# litttt = ['None'] * 1000
# print(len(litttt))

# exit()


# import math
# rate = 1 + 0.03
# year = 30
# valuePerMonth = 3000
# valuePerYear = valuePerMonth * 12
# total = 0
# for i in range(year, 1, -1):
#     value = valuePerYear * math.pow( rate, i )
#     total += value

# print(total)

# exit()

# from PowerStockApiService import addNewStockData
# from PowerStockApiService import getReversedDateTimeList
# dateList = getReversedDateTimeList()

# for time in dateList:
#     addNewStockData(time, 2201, 11, 22)
# exit()

# import pandas as pd
# import datetime
# import numpy


# df = pd.read_csv('./tw_1101.csv')
# top_row = pd.DataFrame({'date':[111],'price':[2],'value':[2]})
# df = pd.concat([top_row, df]).reset_index(drop=True)
# df = df.drop(columns='Unnamed: 0')
# df = df.drop(df.index[len(df)-1])
# # print(df)
# df.to_csv('./tw_1101.csv' , encoding='utf-8')
# exit()



# mylist = ["a", "b", "a", "c", "c", 1, 1, 2, 3, 4, 4]
# mylist = list(dict.fromkeys(mylist))
# print(mylist)

# exit()


# import os
# path = './StockData'
# if os.path.isdir(path):
#     print("hello")
# else:
#     print("world")
#     os.mkdir(path)


# exit()

# import enum

# class StockInfo:
#     AA = 21


# print(str(StockInfo.AA))

# exit()

from PowerStockApiService import requestAllStockMarketIndexWithTimeList
requestAllStockMarketIndexWithTimeList()

from PowerStockApiService import requestAllStockDatasWithTimeList
requestAllStockDatasWithTimeList()

from PickStockService import createReadmeFile
from PickStockService import removeReadmeFile
from PickStockService import getVailedStockIdList

removeReadmeFile()
createReadmeFile()
print(getVailedStockIdList())

exit()


import pandas as pd
from PowerStockApiService import getStockFilePath

import numpy

stockCsvFilePath = getStockFilePath(1101)
print(stockCsvFilePath)

# check file
df = pd.read_csv(stockCsvFilePath)

topDate = numpy.int64(df['date'].values[0])
print(topDate)
timeDate = numpy.int64(timeDate)


exit()

from PowerStockApiService import getReversedDateTimeList
dateList = getReversedDateTimeList()

from StockListService import getStockList

whiteStockList = getStockList()
whiteStockIdList = whiteStockList['id']
whiteStockIdSet = set(whiteStockIdList)


import json
import requests
from PowerStockApiService import addNewStockData

url = 'https://www.twse.com.tw/exchangeReport/MI_INDEX'
url += '?'
url += 'date=20191109'
url += '&response=json'
url += '&type=ALL'

# {'stat': '很抱歉，沒有符合條件的資料!'}
res = requests.get(url)
json_data = json.loads(res.text)
print(json_data)

if json_data['stat'] == '很抱歉，沒有符合條件的資料!':
    print("hello")
else:
    print("world")

stockDataList = json_data['data9']



exit()

index = 0
for stockData in stockDataList:

    stockId = stockData[0]
    stockValue = stockData[2]
    stockPrice = stockData[4]

    isVailedStockData = str(stockId) in whiteStockIdSet
    if isVailedStockData == False:
        continue

    addNewStockData( 20191108, stockId, stockPrice, stockValue)




exit()

import yfinance as yf
import datetime
import pandas_datareader.data as web

yf.pdr_override()

start = datetime.datetime.now() - datetime.timedelta(days=1)
end = datetime.date.today()

dd = web.get_data_yahoo(['3008.TW', '1101.TW', '2330.TW'],start, end)
print(dd.tail(1))

exit()

import datetime
from pandas_datareader import data
import pandas as pd

sid = '0050'

start = datetime.datetime.now() - datetime.timedelta(days=180)
end = datetime.date.today()
pd.core.common.is_list_like = pd.api.types.is_list_like
stock_dr = data.get_data_yahoo(sid+'.TW', start, end)
stock_dr.tail(10)
print(stock_dr)



exit()

url='http://mis.twse.com.tw/stock/api/getStockInfo.jsp?ex_ch=tse_1101.tw'

import requests
res = requests.get(url)
stockJson = res.json()

print(stockJson['msgArray'][0]['nf'])


exit()

from twstock import Stock
import time

stockInfoUrlList = []
count = 150
index = 0
basicUrl = 'http://mis.twse.com.tw/stock/api/getStockInfo.jsp' + '?ex_ch='
for stockId in stockIdList:
    urlArrayIndex = int(index / count)
    if (index % count) == 0:
        firstData = 'tse_' + str(stockId) + '.tw'
        stockInfoUrlList.append(basicUrl + firstData)
    else:
        url = stockInfoUrlList[urlArrayIndex]
        url = url + '|' + 'tse_' + str(stockId) + '.tw'
        stockInfoUrlList[urlArrayIndex] = url
    
    index += 1

for stockId in stockInfoUrlList:
    print(stockId)
    

exit()


stock = Stock('2330')                             # 擷取台積電股價
ma_p = stock.moving_average(stock.price, 5)       # 計算五日均價
ma_c = stock.moving_average(stock.capacity, 1)    # 計算五日均量
ma_p_cont = stock.continuous(ma_p)                # 計算五日均價持續天數
ma_br = stock.ma_bias_ratio(5, 10)                # 計算五日、十日乖離值

# print(stock.data[-1])
print(ma_c)

exit()

from testHello import sample_func
sample_func()

exit()