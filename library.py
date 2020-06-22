import pandas as pd
import numpy as np
import re
import string
import random
from sklearn.pipeline import Pipeline
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import KFold
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import classification_report,confusion_matrix, accuracy_score
from sklearn.feature_extraction.text import TfidfTransformer
from Sastrawi.Stemmer.StemmerFactory import StemmerFactory
from Sastrawi.StopWordRemover.StopWordRemoverFactory import StopWordRemoverFactory



  
class TweetCleaner() :
    def transform(self,X) :
        tweet_final = []
        for tweet in X :
            tweet = tweet[0]
            tweet = tweet.lower()
            regex = re.compile('\shttp.+\s')
            tweet = regex.sub('',tweet)
            regex = re.compile('\shttps.+\s')
            tweet = regex.sub('',tweet)
            regex = re.compile('\spic.+\s')
            tweet = regex.sub('',tweet)
            regex = re.compile('\sftp.+\s')
            tweet = regex.sub('',tweet)
            regex = re.compile('[^a-zA-Z0-9]')
            tweet = regex.sub(' ',tweet)
            regex = re.compile('[0-9]+')
            tweet = regex.sub('',tweet)
            regex = re.compile(r'\W*\b\w{1,3}\b')
            tweet = regex.sub('',tweet)
            regex = re.compile('rt\s')
            tweet = regex.sub(' ',tweet)

            #remove stopwords
            stop_factory = StopWordRemoverFactory()
            stopword = stop_factory.create_stop_word_remover()
            tweet = stopword.remove(tweet)

            #stemming
            stem_factory = StemmerFactory()
            stemmer = stem_factory.create_stemmer()
            tweet = stemmer.stem(tweet)
            tweet_final.append(tweet)

        tweet_final = np.array(tweet_final)
        return tweet_final

    def fit_transform(self,X) :
        return self.transform(X)
