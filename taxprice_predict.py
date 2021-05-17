#!/usr/bin/env python
# coding: utf-8

# In[1]:


import datetime
import matplotlib.pyplot as plt
import numpy as np
import pandas_datareader
import sklearn
import sklearn.linear_model
import sklearn.model_selection

#データをひっぱってくる
df_nvda = pandas_datareader.data.DataReader("NVDA","yahoo","2000-01-01")
df_aapl = pandas_datareader.data.DataReader("AAPL","yahoo","2000-01-01")
df_fb = pandas_datareader.data.DataReader("FB","yahoo","2000-01-01")
df_gold = pandas_datareader.data.DataReader("GLD","yahoo","2000-01-01")

#機械学習
df_nvda['label'] = df_nvda['Close'].shift(-30) #30日間過去へ

#過去１４日単純移動平均のcolumnを作成
df_nvda['SMA'] = df_nvda['Close'].rolling(window=14).mean()

#入力データ
#labelとSMA鉄は除外して、High Low Open Close Volume AdjClose changeの計７列を使う

X = np.array(df_nvda.drop(['label','SMA'],axis=1))
X.shape #(1172,7)

#入力データの標準化
X = sklearn.preprocessing.scale(X)

#30日前から現在までのデータを予測に使用する入力データとする
predict_data = X[-30 : ]
predict_data.shape #(30,7)

#直近30日間を除外したデータ
X = X[ : -30]
X.shape #(1142,7)

#30日後の終値
y = np.array(df_nvda['label'])
y.shape

#終値がない部分の削除
y = y[ : -30]
y.shape
#plt.plot(y)

#データを訓練用と検証用に分割して学習モデルを選択して学習させて、検証する
X_train, X_test, y_train, y_test = sklearn.model_selection.train_test_split(X,y,test_size=0.2)

#学習モデルの定義
lr = sklearn.linear_model.LinearRegression()

#学習する
lr.fit(X_train,y_train)

#検証する
accuracy = lr.score(X_test,y_test)
print("accuracy:",accuracy)

#過去30日間の入力データpredict_dataからそれぞれ30日後の未来周知データpredicted_dataを予測する
predicted_data = lr.predict(predict_data)
predicted_data.shape 

#予測結果
#予測済みデータをデータフレームに追加するため、予め、空データを入れておく
df_nvda['Predicted'] = np.nan

#最終日indexを取得する
last_date = df_nvda.iloc[-1].name #timestamp

#1日の数値を定義
one_day = 86400

#最終日に1日を足す
next_unix = last_date.timestamp() + one_day

#予測済みデータ
for data in predicted_data:
    
    #日付の定義
    next_date = datetime.datetime.fromtimestamp(next_unix)
    
    #1日カウントアップ
    next_unix += one_day
    
    #index(未来の日付)に予測終値を追加する
    df_nvda.loc[next_date] = np.append([np.nan] * (len(df_nvda.columns)-1),data)
    
#可視化
df_nvda['Close'].plot(figsize=(16,5),color='green')
df_nvda['Predicted'].plot(figsize=(16,5),color='orange')

#保存
plt.savefig("predict_result.png")
plt.show()


# In[ ]:




