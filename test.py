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

# from StockFunction import getStockList
# import pandas as pd
# data = getStockList()
# stockNumberList =  data['id']
# print(type(stockNumberList[3]))

# exit()

# from StockFunction import getStockList
# stockIdList = getStockList()['id']

# from StockFunction import getStockUrlList
# urlList = getStockUrlList()
# print(urlList[0])

# exit()

#TODO: 
https://www.twse.com.tw/exchangeReport/MI_INDEX?date=20191101&response=json&type=ALL
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