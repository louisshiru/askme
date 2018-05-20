# -*- coding: utf-8 -*-
"""
Created on Wed May 16 19:38:22 2018

@author: BirdJesus
"""

import sys
import pandas as pd
import gspread
from oauth2client.service_account import ServiceAccountCredentials as SAC
import time
import redis
from flask import current_app
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import jieba as jb
import jieba.analyse

############## 金鑰 ############## 
GDriveJSON = 'My-First-Project-dbe1b2d12e48.json'
GSpreadSheet = 'AI_project'


############## 連接google試算表 ############## 
scope = ['https://spreadsheets.google.com/feeds','https://www.googleapis.com/auth/drive']
key = SAC.from_json_keyfile_name(GDriveJSON, scope)
gc = gspread.authorize(key)
sheet1 = gc.open(GSpreadSheet).sheet1


############## 資料庫使用函數 ############## 

def getCellValue(row,col): #讀取單個儲存格資料
    return sheet1.cell(row,col).value

def getAllValues(): #讀取全部試算表資料
    return pd.DataFrame(sheet1.get_all_values())  

def setCellValue(row,col,value): #上傳單個儲存格資料
    sheet1.update_cell(row,col,value)
    
def setAnimeName(col,value): #上傳動漫名稱，第一列
    sheet1.update_cell(1,col,value)
        
def setCollValues(col,values): #上傳動漫資料，第三列開始
    for i,v in enumerate(values):
        setCellValue(i+3,col,v)
        
  ######################################################   
#def cutsentence(sentence):
 # print ("Input：", sentence)
  #words = jb.cut(sentence, cut_all=False)
  #return words
##########################################################   
#從雲端拉資料
data = getAllValues()
#轉置矩陣
data_T = data.T
#預備放斷詞模型的空陣列
corpus = []
for row in data_T[1]:
        corpus.append(" ".join(jieba.cut(row.split(',')[0], cut_all=False)))

#設定TFIDF參數
tf = TfidfVectorizer(analyzer='word',
                     ngram_range=(1, 3),
                     min_df=0,
                     )

#將斷詞後矩陣建立TFIDF模型
tfidf_matrix = tf.fit_transform(corpus)
#推薦系統(COS相關性)
cosine_similarities = linear_kernel(tfidf_matrix, tfidf_matrix)

#測試用資料
valid =pd.read_csv('valid.csv',encoding ='UTF-8',header = None)

#斷詞函數
def cut(sentence):
    cutlist = []
    for row in sentence:
        cutlist.append(" ".join(jieba.cut(row.split(',')[0], cut_all=False)))
    return cutlist

#回報作品函數(索引值)
def answer(cutlist,AllDB):
    temp = cutlist + AllDB
    temp1 = tf.fit_transform(temp)
    cosine_similarities = linear_kernel(temp1, temp1)
    ans = cosine_similarities[0].argsort()[-3:][::-1]#-3代表取相關性前三高的  可以自己設定
    return ans

aaa = cut(valid[2])

#基本上這邊設計  INDEX=0的那筆資料要刪掉  因為就是自己本身
bbb =answer(aaa,corpus)#回報作品函數  需要有兩個INPUT:使用者輸入的語句、斷詞後之模型

##不能將使用者輸入語句跟模型分別做TF-IDF後再取餘旋，因為惟度不一樣，而且又是特殊格式  很難改
##所以採取 輸入的是斷詞後資料，在函數中做餘旋相關
