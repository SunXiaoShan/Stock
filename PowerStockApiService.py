import datetime

def getDateTimeList(timedelta=100):
    dateList = []

    for i in range(timedelta, 0, -1):
        time = datetime.datetime.now() - datetime.timedelta(days=i)
        strTime = time.strftime("%Y%m%d")
        stockIdList.append(strTime)

    return stockIdList
