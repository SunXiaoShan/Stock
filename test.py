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

from StockFunction import getStockList
stockIdList = getStockList()['id']

from StockFunction import getStockUrlList
urlList = getStockUrlList()
print(urlList[0])

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