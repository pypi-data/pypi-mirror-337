import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

df = pd.read_csv('./dataset/spam.csv', encoding='ISO-8859-1')

df = df[['Message', 'Category']]
df.columns = ['SMS', 'Type']

df['Type'] = df['Type'].map({'ham': 0, 'spam': 1})

countvec = CountVectorizer(ngram_range=(1,4), stop_words='english', strip_accents='unicode', max_features=1000)

bow = countvec.fit_transform(df.SMS)
X_train = bow.toarray()
Y_train = df.Type.values

mnb = MultinomialNB()
mnb.fit(X_train, Y_train)

text1 = countvec.transform(['Free gifts for all'])
print('Free gift for all:', mnb.predict(text1))

text2 = countvec.transform(['We will go for a lunch'])
print('We will go for a lunch:', mnb.predict(text2))
