# -*- coding: utf-8 -*-
"""Untitled5.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1OKm6wAcriCSI4ivSW7RPycH2PebMZzU8
"""

# Commented out IPython magic to ensure Python compatibility.
import numpy as np
import pandas as pd

import matplotlib.pyplot as plt
import seaborn as sns
sns.set_style("darkgrid")
# %matplotlib inline

import string
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud
from sklearn.feature_extraction.text import CountVectorizer
from nltk.stem import WordNetLemmatizer

from sklearn.model_selection import train_test_split
from sklearn import metrics

messages = pd.read_csv('/content/spam.csv',encoding = 'latin-1')
messages.head()

messages.tail()

messages = messages.drop(labels = ["Unnamed: 2", "Unnamed: 3", "Unnamed: 4"], axis = 1)
messages.columns = ["label", "message"]

messages.head()

messages.info()

messages.describe()

messages.groupby('label').describe().T

messages['length'] = messages['message'].apply(len)
messages.head()

messages['message'].value_counts().rename_axis(['message']).reset_index(name='counts').head()

"""# Data Visulaization

"""

import matplotlib.pyplot as plt

colors = ['#57b3ff','#99ff99']

plt.figure(figsize=(6, 6))
plt.pie(messages["label"].value_counts(), labels=["Ham", "Spam"], autopct='%1.1f%%', startangle=90, explode=[0, 0.1], colors=colors, shadow=True)
plt.title("Spam vs Ham")


centre_circle = plt.Circle((0,0),0.70,fc='white')
fig = plt.gcf()
fig.gca().add_artist(centre_circle)

plt.legend(["Ham", "Spam"])
plt.show()

import matplotlib.pyplot as plt

plt.figure(figsize=(12, 6))
plt.hist(messages['length'], bins=100, color='Blue', edgecolor='black')  # Adjusted the color and added edgecolor
plt.axvline(messages['length'].mean(), color='red', linestyle='dashed', linewidth=2, label='Mean Length')  # Added a red dashed line for mean length
plt.title("Frequency Distribution of Message Length")
plt.xlabel("Length")
plt.ylabel("Frequency")
plt.legend()  # Added a legend for the mean length line
plt.show()

messages['length'].describe()

messages[messages['length'] == 910]['message'].iloc[0]

messages.hist(column='length', by='label', bins=50,figsize=(12,4))

"""# Text Pre-processing"""

def text_preprocess(mess):
    nopunc = [char for char in mess if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    nopunc = nopunc.lower()
    nostop=[word for word in nopunc.split() if word.lower() not in stopwords.words('english') and word.isalpha()]

    return nostop

spam_messages = messages[messages["label"] == "spam"]["message"]
ham_messages = messages[messages["label"] == "ham"]["message"]
print("No of spam messages : ",len(spam_messages))
print("No of ham messages : ",len(ham_messages))

"""# Data Transformation


"""

import nltk

# Download stopwords
try:
    nltk.data.find('corpora/stopwords.zip')
except LookupError:
    nltk.download('stopwords')

# Your existing code
spam_words = text_preprocess(spam_messages)

spam_words[:10]

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Your existing code
spam_wordcloud = WordCloud(width=600, height=400, background_color='black').generate(' '.join(spam_words))

# Create a colored border line
colored_line = plt.Line2D((0, 1), (0, 0), color='blue', linewidth=3)

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 8), facecolor='k')
ax.add_line(colored_line)

# Display the word cloud on top of the colored line
ax.imshow(spam_wordcloud, aspect='auto')
ax.axis("off")

# Adjust layout to ensure the colored line is visible
plt.tight_layout(pad=0)
plt.show()

print("Top 10 Spam words are :\n")
print(pd.Series(spam_words).value_counts().head(10))

"""# Wordcloud for Ham Messages"""

ham_words = text_preprocess(ham_messages)

ham_words[:10]

from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Your existing code
ham_wordcloud = WordCloud(width=600, height=400, background_color='black').generate(' '.join(ham_words))

# Create a colored border line
colored_line = plt.Line2D((0, 1), (0, 0), color='blue', linewidth=3)

# Create a figure and axis
fig, ax = plt.subplots(figsize=(10, 8), facecolor='k')
ax.add_line(colored_line)

# Display the word cloud on top of the colored line
ax.imshow(ham_wordcloud, aspect='auto')
ax.axis("off")

# Adjust layout to ensure the colored line is visible
plt.tight_layout(pad=0)
plt.show()

print("Top 10 Ham words are :\n")
print(pd.Series(ham_words).value_counts().head(10))

"""# Data Transformation"""

messages.head()

messages["message"] = messages["message"].apply(text_preprocess)

messages["message"] = messages["message"].agg(lambda x: ' '.join(map(str, x)))

messages.head()

messages["message"][7]

"""# Creating the Bag of Words"""

from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer()
bow_transformer = vectorizer.fit(messages['message'])

print("20 Bag of Words (BOW) Features: \n")
print(vectorizer.get_feature_names_out()[20:40])

print("\nTotal number of vocab words : ", len(vectorizer.vocabulary_))

message4 = messages['message'][3]
print(message4)

bow4 = bow_transformer.transform([message4])
print(bow4)
print(bow4.shape)

from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer()
bow_transformer = vectorizer.fit(messages['message'])

# Accessing feature names for a specific feature index (e.g., 5945)
feature_name = vectorizer.get_feature_names_out()[5945]
print(feature_name)

messages_bow = bow_transformer.transform(messages['message'])

print('Shape of Sparse Matrix: ', messages_bow.shape)
print('Amount of Non-Zero occurences: ', messages_bow.nnz)

from sklearn.feature_extraction.text import TfidfTransformer

tfidf_transformer = TfidfTransformer().fit(messages_bow)

tfidf4 = tfidf_transformer.transform(bow4)
print(tfidf4)

from sklearn.feature_extraction.text import CountVectorizer

vectorizer = CountVectorizer()
bow_transformer = vectorizer.fit_transform(messages['message'])  # Use fit_transform instead of fit

# Accessing feature names for specific feature indices (e.g., 5945 and 3141)
feature_names = vectorizer.get_feature_names_out()
print(feature_names[5945])
print(feature_names[3141])

messages_tfidf = tfidf_transformer.transform(messages_bow)
print(messages_tfidf.shape)

messages["message"][:10]

from sklearn.feature_extraction.text import TfidfVectorizer

vec = TfidfVectorizer(encoding = "latin-1", strip_accents = "unicode", stop_words = "english")
features = vec.fit_transform(messages["message"])
print(features.shape)

print(len(vec.vocabulary_))

"""# Model Evaluation¶"""

msg_train, msg_test, label_train, label_test = \
train_test_split(messages_tfidf, messages['label'], test_size=0.2)

print("train dataset features size : ",msg_train.shape)
print("train dataset label size", label_train.shape)

print("\n")

print("test dataset features size", msg_test.shape)
print("test dataset lable size", label_test.shape)

from sklearn.naive_bayes import MultinomialNB

clf = MultinomialNB()
spam_detect_model = clf.fit(msg_train, label_train)

predict_train = spam_detect_model.predict(msg_train)

print("Classification Report \n",metrics.classification_report(label_train, predict_train))
print("\n")
print("Confusion Matrix \n",metrics.confusion_matrix(label_train, predict_train))
print("\n")
print("Accuracy of Train dataset : {0:0.3f}".format(metrics.accuracy_score(label_train, predict_train)))

print('predicted:', spam_detect_model.predict(tfidf4)[0])
print('expected:', messages['label'][3])

label_predictions = spam_detect_model.predict(msg_test)
print(label_predictions)

print(metrics.classification_report(label_test, label_predictions))
print(metrics.confusion_matrix(label_test, label_predictions))

print("Accuracy of the model : {0:0.3f}".format(metrics.accuracy_score(label_test, label_predictions)))