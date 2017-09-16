#!/usr/bin/env python3

import pandas as pd
from pykakasi import kakasi
kakasi=kakasi()
kakasi.setMode('H', 'a')
kakasi.setMode('K', 'a')
kakasi.setMode('J', 'a')
conv = kakasi.getConverter()

pd.set_option('display.max_rows',1000)

listdf=pd.read_csv('crawl.txt', comment='#')  #取得対象の読み込み
obsdf=pd.read_csv('obs.txt')   #全観測所リストの読み込み

list0=pd.merge(listdf,obsdf,on='観測所番号',how='left') #結合
list1=list0[['観測所番号','観測所名']].drop_duplicates() #必要列だけ取り出して重複削除
list2=[]  #ローマ字用空リスト

for n in range(len(list1)):
    list2.append(conv.do(list1.iloc[n,1]))
list1['roman']=list2
output=list1[['観測所番号','roman']]

output.to_csv('obslist.csv',index=False)

#for i,v in listdf.iterrows():
#    print(i,v['観測所番号'])