'''
Author: Whatever it takes
Date: 2023-07-06 16:16:09
LastEditTime: 2023-07-06 17:59:45
Description: 
一份伏特加，加一点青柠，姜汁，啤酒，最重要的是，还有一点爱
'''
from datetime import datetime, date, timedelta
import math
from wechatpy import WeChatClient
from wechatpy.client.api import WeChatMessage, WeChatTemplate
import requests
from requests import get, post
import os
import random
import cityinfo
from time import time, localtime

today = datetime.now()

start_date = os.environ.get('START_DATE', '2023-5-23')
province = os.environ.get('PROVINCE', '陕西')
city = os.environ.get('CITY', '西安')
birthday = os.environ.get('BIRTHDAY', '03-21')
app_id = os.environ.get("APP_ID", "wx6619e83a010dffbb")
app_secret = os.environ.get("APP_SECRET", "74288dc49a81c48df2524da1e50899e6")
user_id = os.environ.get("USER_ID", "oSPvn6Ll-uN_7DHAp2fBkOQzurmc")
template_id = os.environ.get("TEMPLATE_ID", "W6qTf5HY8yLk4nOPFvPzhDapxfeJCeHEthoLQivLSEs")
user_2_id = "oSPvn6EehyAfw3cpdjM3Ey8fIaKk"

# start_date = os.environ['START_DATE']
# city = os.environ['CITY']
# birthday = os.environ['BIRTHDAY']

# app_id = os.environ["APP_ID"]
# app_secret = os.environ["APP_SECRET"]

# user_id = os.environ["USER_ID"]
# template_id = os.environ["TEMPLATE_ID"]


def get_weather():
  url = "http://autodev.openspeech.cn/csp/api/v2.1/weather?openId=aiuicus&clientType=android&sign=android&city=" + city
  res = requests.get(url).json()
  weather = res['data']['list'][0]
  return weather['weather'], math.floor(weather['temp'])

def get_weather(province, city):
    # 城市id
    city_id = cityinfo.cityInfo[province][city]["AREAID"]
    # city_id = 101280101
    # 毫秒级时间戳
    t = (int(round(time() * 1000)))
    headers = {
      "Referer": "http://www.weather.com.cn/weather1d/{}.shtml".format(city_id),
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    url = "http://d1.weather.com.cn/dingzhi/{}.html?_={}".format(city_id, t)
    response = get(url, headers=headers)
    response.encoding = "utf-8"
    response_data = response.text.split(";")[0].split("=")[-1]
    response_json = eval(response_data)
   # print(response_json)
    weatherinfo = response_json["weatherinfo"]
    # 天气
    weather = weatherinfo["weather"]
    # 最高气温
    temp = weatherinfo["temp"]
    # 最低气温
    tempn = weatherinfo["tempn"]
    return weather, temp, tempn

def get_count():
  delta = today - datetime.strptime(start_date, "%Y-%m-%d")
  return delta.days

def get_birthday():
  next = datetime.strptime(str(date.today().year) + "-" + birthday, "%Y-%m-%d")
  if next < datetime.now():
    next = next.replace(year=next.year + 1)
  return (next - today).days

# def get_words():
#   words = requests.get("https://api.shadiao.pro/chp")
#   if words.status_code != 200:
#     return get_words()
#   return words.json()['data']['text']

def get_words():
    get_url = "https://api.shadiao.pro/chp"
    headers = {
      'Content-Type': 'application/json',
      'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
                    'AppleWebKit/537.36 (KHTML, like Gecko) Chrome/103.0.0.0 Safari/537.36'
    }
    chp = get(get_url, headers=headers).json()['data']['text']
    print(chp)
    return chp

def get_random_color():
  return "#%06x" % random.randint(0, 0xFFFFFF)


client = WeChatClient(app_id, app_secret)

wm = WeChatMessage(client)
wea, temperature, tempn = get_weather(province, city)

# 计算何年何月何日
year = localtime().tm_year
month = localtime().tm_mon
day = localtime().tm_mday
today_trans = datetime.date(datetime(year=year, month=month, day=day))
week_list = ["星期一", "星期二", "星期三", "星期四", "星期五", "星期六","星期日"]
week = week_list[today_trans.isoweekday()-1]

data = {"date":{"value":"{} {}".format(today_trans, week)}, "weather":{"value":wea},"temperature":{"value":temperature},
"temperature_low":{"value":tempn}, "love_days":{"value":get_count()},"birthday_left":{"value":get_birthday()},"words":{"value":get_words(), "color":get_random_color()}}
res = wm.send_template(user_id, template_id, data)
res_2 = wm.send_template(user_2_id, template_id, data)
print(res)
