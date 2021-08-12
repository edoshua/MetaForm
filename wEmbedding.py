import pymongo
from pymongo import MongoClient
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import string
import matplotlib.pyplot as plt
import nltk
from nltk.corpus import stopwords
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
import gensim
from gensim.models import Word2Vec
from nltk.stem import WordNetLemmatizer
nltk.download('wordnet')

#MongoDB connection
client = MongoClient("mongodb://localhost:27017")
sourcedb = client.wikidb
sourcecoll = sourcedb['wikipedia']
outputdb = client.wordEmbedding
outputcoll = outputdb['similarWords']

#Storing all text content in the database in a list
query = sourcecoll.find({},{'text':1, '_id':0})
liste = list(query)

# Clean up characters that do not have a place in the ascii table and give errors when printing
i = ""
for item in liste:
    i += item['text'].encode("ascii", errors="ignore").decode()

i = i.lower()

for character in i:
    if character in string.punctuation:
        i = i.replace(character, "")

lemmatizer = WordNetLemmatizer()
text_tokens = word_tokenize(i)
tokens_without_sw = [word for word in text_tokens if word not in STOPWORDS]

temp=""
for item in tokens_without_sw:
    temp += lemmatizer.lemmatize(item) + " "

tokens = word_tokenize(temp)

corpus = []
for word in text_tokens:
    corpus.append(word.split())

model = Word2Vec(corpus,  window = 2, min_count = 2, sg = 1)
i = 0
for word in tokens:
    try:
        sims = model.wv.most_similar(word)
    except KeyError:
        continue
    for similar in sims:
            item = {'key' : word , 'similar' : similar[0]}
            outputcoll.insert_one(item)
