import pika
import twint
import pandas as pd
import numpy as np
import json
import sys
import math as m

connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', heartbeat=0))
channel = connection.channel()
channel.basic_qos(prefetch_count=1)

antrian = channel.queue_declare(queue='antrian')

c = twint.Config()

def searchTweet():
    twint.storage.panda.clean()
    c.Search = "#pilpres"
    c.Lang = "id"
    c.Limit = 3000
    c.Pandas = True
    
    twint.run.Search(c)
    df_search = twint.storage.panda.Tweets_df
    return df_search
    
def searchUser():
    username = df_cari[["username"]].drop_duplicates().reset_index(drop=True)
    df_final = pd.DataFrame()
    for user in username["username"]:
      print(user)
      twint.storage.panda.clean()
      c.Username = user
      c.Pandas = True
      c.Hide_output = True
      twint.run.Lookup(c)     
      df = twint.storage.panda.User_df
      df_final = df_final.append(df)
    return df_final

print("Mengambil data twit...\n")
df_cari = searchTweet()
#df_cari.info()

df_user = searchUser()
#df_user.info()

df_user = df_user.rename(columns={'media': 'nmedia', 'likes': 'user_likes', 'tweets': 'ntweets'})

df_join = pd.merge(df_cari, df_user, on='username')
df_join = df_join[['username','followers', 'following', 'user_likes', 'private', 'ntweets', 'verified', 'nmedia','id_x', 'tweet',  'nlikes', 'nreplies', 'nretweets']]

df_join.info()

df_join.to_csv("3000_3.csv")

print("Twit lengkap")

rows = len(df_join.index)
cons= antrian.method.consumer_count
steps = m.ceil(rows/cons)

print("Jumlah consumer: ", cons)

frames = {n: df_join.iloc[n:n+steps] 
          for n in range(0, rows, steps)}

for (key, value) in frames.items():
     df_dict = value.to_dict(orient="records")
     data = json.dumps(df_dict)
     channel.basic_publish(exchange='', routing_key='antrian', body=data)

print("Tweet terkirim!")
connection.close()
