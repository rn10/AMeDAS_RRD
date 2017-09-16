#!/usr/bin/env python3
# ver 1.0

import requests
import os
import datetime
from time import sleep
from lxml import html
import pandas as pd

item={'気温':'temp','降水量':'rain','湿度':'humd','気圧':'pres','風速':'wind','日照時間':'sun','積深雪':'snow'}

listdf=pd.read_csv('crawl.txt',comment='#')

for i,v in listdf.iterrows():
    obsnum=v['観測所番号']
    url="http://www.jma.go.jp/jp/amedas_h/yesterday-"+str(obsnum)+".html"
    res = requests.get(url)
    res.encoding = res.apparent_encoding
    dom = html.fromstring(res.text)
    table_xpath = """//*[@id="tbl_list"]"""
    table = dom.xpath(table_xpath)[0]
    df = pd.read_html(html.tostring(table),skiprows=[1],header=0)
    df0=df[0]

    now=datetime.datetime.now()
    yesterday=datetime.datetime(now.year,now.month,now.day,0,0,0)-datetime.timedelta(days=1)

    rrdfile=str(obsnum)+".rrd"
    if not os.path.exists('data/'+rrdfile):
        # temp,rain,humd,pres,wind,sun,snow - 35days/1h ,105days/3h ,548days/day ,3990days/1w
        os.system("/usr/bin/rrdtool create data/"+rrdfile+" --start "+str(int(yesterday.timestamp()))+" --step 3600 DS:temp:GAUGE:7200:-100:100 DS:rain:GAUGE:7200:0:1000 DS:humd:GAUGE:7200:0:100 DS:pres:GAUGE:7200:800:1100 DS:wind:GAUGE:7200:0:100 DS:sun:GAUGE:7200:0:1 DS:snow:GAUGE:7200:0:100000 RRA:AVERAGE:0.5:1:840 RRA:AVERAGE:0.5:3:840 RRA:MIN:0.5:3:840 RRA:MAX:0.5:3:840 RRA:AVERAGE:0.5:24:548 RRA:MIN:0.5:24:548 RRA:MAX:0.5:24:548 RRA:AVERAGE:0.5:168:570 RRA:MIN:0.5:168:570 RRA:MAX:0.5:168:570")

    for n in range(24):
        temp = rain =humd = pres = wind = sun = snow = 'nan'
        time=yesterday+datetime.timedelta(hours=n+1)
        for m in range(len(df0.columns)-1):
            ns=locals()
            ns[item.get(df0.columns[m+1])]=df0.loc[n,[df0.columns[m+1]]][0]
        os.system("/usr/bin/rrdtool update data/"+rrdfile+" "+str(int(time.timestamp()))+":"+str(temp)+":"+str(rain)+":"+str(humd)+":"+str(pres)+":"+str(wind)+":"+str(sun)+":"+str(snow))
    sleep(1)