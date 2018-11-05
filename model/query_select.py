# #coding=utf-8
# '''
# http server v2.0
# 1.面向对象
# 2.可以请求简单的数据
# 3.能进行简单的请求解析
# 4.结构使用类进行封装
# '''

import re,random,requests,time,json


# 参数说明
# from_station:出发地 to_station:目的地  querydate:查询日期
def Query(from_station, to_station, querydate,t1):
    try:
        f_s = t1.stations[from_station]
        t_s = t1.stations[to_station]
        print(querydate,f_s,t_s)


        url = (
            "https://kyfw.12306.cn/otn/leftTicket/query?leftTicketDTO.train_date={}&leftTicketDTO.from_station={}&leftTicketDTO.to_station={}&purpose_codes=ADULT").format(
            querydate, f_s, t_s)
        # 主要是获取user-agent，伪装成浏览器，其它的可要，可不要

        header = [
        {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/68.0.3440.106 Safari/537.36"},
        {"User-Agent": "Mozilla/5.0 (X11; U; Linux x86_64; zh-CN; rv:1.9.2.10) Gecko/20100922 Ubuntu/10.10 (maverick) Firefox/3.6.10"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/534.57.2 (KHTML, like Gecko) Version/5.1.7 Safari/534.57.2"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; Trident/7.0; rv:11.0) like Gecko"},
        {"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/21.0.1180.71 Safari/537.1 LBBROWSER"}
        ]

        h_random = random.choice(header)
        web_data = requests.get(url, headers=h_random, verify=False, timeout=1)  # verify=False表示不判断证书
        web_data.encoding = "utf-8"

        traindatas = web_data.json()["data"]["result"]  # 返回的结果，转化成json格式，取出data中的result方便后面解析列车信息用
        global title
        title = web_data.json()["data"]["map"] # 返回的结果，转化为json格式，取出data中的flag方便后面解析列车信息用

        return traindatas
    except KeyError as err:
        return "None"

def data_analysis(traindatas):
    list1 = []
    try:
        for onedata in traindatas:
            onedata = onedata.split("|")  # 获取一条数据所有信息，以列表形式保存
            list1.append(onedata)
    except:
        pass


    try:
        for onedata in list1:
            onedata[6] = title[onedata[6]]#出发的转换为中文
            onedata[7] = title[onedata[7]]#到达地转换为中文
    except:
        pass

    return list1
