#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import glob
import re
import pandas as pd
import numpy as np
import lightgbm as lgb

from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error as m

import os

files = glob.glob('#')
data_list = []
# print(files)
for file in files:
    data_list.append(pd.read_csv(file, index_col=0))
df = pd.concat(data_list)

def prepare(df):
    nonnull_list = []
    for col in df.columns:
        nonnull = df[col].count()
        if nonnull == 0:
            nonnull_list.append(col)
    # print(nonnull_list)
    df = df.drop(nonnull_list,axis=1)
    df = df.drop("市区町村名",axis=1)
    df = df.drop("種類",axis=1)
    #時間の置き換え
    minu = {
        "30分?60分":45,
        "1H?1H30":75,
        "2H?":120,
        "1H30?2H":105,
    }
    df['最寄駅：距離（分）'] = df['最寄駅：距離（分）'].replace(minu).astype(float)
    df["面積（㎡）"] = df["面積（㎡）"].replace("2000㎡以上",2000).astype(float)
    
    y_list = {}
    for i in df["建築年"].value_counts().keys():
        if "平成" in i:
            num = float(i.split("平成")[1].split("年")[0])
            year = 33 - num
        if "令和" in i:
            num = float(i.split("令和")[1].split("年")[0])
            year = 3 - num
        if "昭和" in i:
            num = float(i.split("昭和")[1].split("年")[0])
            year = 96 - num
        y_list[i] = year
    y_list["戦前"] = 76
    df["建築年"] = df["建築年"].replace(y_list)
    year = {
        "年第1四半期": ".25",
        "年第２四半期": ".50",
        "年第３四半期": ".75",
        "年第４四半期": ".99"
    }
    year_list = {}
    year_rep = 0
    for i in df["取引時点"].value_counts().keys():
        for k, j in year.items():
            if k in i:
                year_rep = i.replace(k, j)
        year_list[i] = year_rep
    df["取引時点"] = df["取引時点"].replace(year_list).astype(float)
    for col in ["都道府県名", "地区名", "最寄駅：名称", "間取り", "建物の構造", "用途", "今後の利用目的", "都市計画", "改装", "取引の事情等"]:
        df[col] = df[col].astype("category")
    df = df.drop("取引の事情等",axis=1)
    return df

df_test = pd.read_csv("#", index_col=0)
df_test = prepare(df_test)

predict = model.predict(df_test)
df_test["取引価格（総額）_log"] = predict
df_test["取引価格（総額）_log"].to_csv(index=True, path_or_buf='#')

