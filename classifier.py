#!/usr/bin/env python
import pika
import sys
import os
import time
import psutil
import re
import string
import random
import pickle
import pandas as pd
import numpy as np
import xgboost as xgb
import json
from pandas.io.json import json_normalize
from sklearn.model_selection import KFold, GridSearchCV, train_test_split, cross_val_score
from sklearn.metrics import classification_report, confusion_matrix, accuracy_score
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_selection import SelectFromModel
from library import TweetCleaner
from guppy import hpy
from statistics import mean


try:
    connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost'))
    channel = connection.channel()
    channel.queue_declare(queue='antrian')
    h = hpy()
  
    def classifier(df):
        channel.stop_consuming()
        print('Twit masuk!')
        print('Sedang mengklasifikasi...')
        # load data

        start_time = time.time()
        cpu = psutil.cpu_percent(interval=0.01)
        x = h.heap()
        
        X_tweet = df[["tweet"]].values

        #pembersihan
        cleaner = pickle.load(open('cleaner.sav', 'rb'))
        X_tweet = cleaner.transform(X_tweet)

        #vektorisasi dan transformasi
        tfidf = pickle.load(open('tfidf.sav', 'rb'))
        X_tweet = tfidf.transform(X_tweet).toarray()
        X_text = pd.DataFrame(X_tweet,columns=tfidf.get_feature_names())  
        
        #joining dataframe teks dan numeris
        X_numerical = df[df.columns.difference(['tweet', 'id_x'])]
        X_join = X_text.join(X_numerical).set_index(['username'])

        #definisi data X baru
        X_test = X_join.values

        # memuat (loading) model
        loaded_model = pickle.load(open('XGB_Model.sav', 'rb'))
        # membuat prediksi pada data uji
	
        y_pred = loaded_model.predict(X_test)
	
        print("---Waktu Total %.2f seconds ---" % (time.time() - start_time))
        #print(y_pred)
        #print(loaded_model.classes_)
        df_y = pd.DataFrame(y_pred, columns=["label"])
        #df_y = df_y.mul(100)
        df_join = X_numerical.join(df_y)
        df_tweet = df_join.join(df[["tweet"]]).set_index("username")

        mem = x.size
        print("CPU: %.2f%%  RAM: %.2f MB"% (cpu, (mem/10e6)))

        filename = input("Masukkan nama hasil klasifikasi (dalam csv): ")
        df_tweet.to_csv(filename)
        #print("Memory consumption: %.2f MB" % (x.size/10e6))  




    def callback(ch, method, properties, body):
        data = json.loads(body)
        tweet = json_normalize(data)
        tweet.info()
        classifier(tweet)

        

    channel.basic_consume(queue='antrian', on_message_callback=callback, auto_ack=True)

    print('Menunggu tweet masuk. Tekan CTRL+C untuk menghentikan classifier')
    channel.start_consuming()

except KeyboardInterrupt:
    sys.exit("\n")
