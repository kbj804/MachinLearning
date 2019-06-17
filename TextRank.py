# https://github.com/summanlp/textrank

from summa import summarizer
from summa import keywords
from bs4 import BeautifulSoup
import requests

from nltk.stem import WordNetLemmatizer
import nltk
import string
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import requests
import re
from tldextract import extract
from sklearn.feature_extraction.text import TfidfVectorizer
from collections import Counter
import ipt
from sklearn.feature_extraction.text import CountVectorizer

remove_punct_dict = dict((ord(punct), None) for punct in string.punctuation)
lemmar = WordNetLemmatizer()

def count_harmful_word(top20):
    harmful_word_num = 0
    for word in top20: # top 20 word
        if word in ipt.harmful_url_dic:
            harmful_word_num += 1
            #if harmful_url_dic.get(word) == 1: idx += 1

    return harmful_word_num

def LemTokens(tokens):
    return [lemmar.lemmatize(token) for token in tokens]

def LemNormalize(text):
    return LemTokens(nltk.word_tokenize(text.lower().translate(remove_punct_dict)))

def pre_process(soup):
    # kill all script and style elements
    for script in soup(["script", "style"]):
        script.extract()    # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)
    text = re.sub("[^a-zA-Z]", " ", text)

    return text.lower()

def tfidf_parse(text): #parse the url to create outlink urls.
    try: # this try is to catch HTTP GET exception.
        print("connection . . . . . . . .  .  ")
        text1 = []
        # url = []
        #max_document_length = 0

        str = text
        #if len(str) > max_document_length:
         #   max_document_length = len(str)
        text1.append(''.join(str))  # join: list -> str

        tfidf_vect = CountVectorizer(stop_words=ipt.stopwords,
                                           # max_df=0.9,
                                           #max_features=10000,
                                           min_df=0.8,
                                           # ngram_range=(1,2),
                                           tokenizer=LemNormalize
                                           )

        X = tfidf_vect.fit_transform(text1) # 데이터 백터화

        vocab = list(tfidf_vect.get_feature_names())
        counts = X.sum(axis=0).A1 # 단어 카운트

        freq_distribution = Counter(dict(zip(vocab, counts)))
       # print(freq_distribution.most_common(20))
        data = []
        data1 =[]
        for word in freq_distribution.most_common(20):
            #print(word[0])
            data.append(word[0])
        print("DATA: ",data)
        count = count_harmful_word(data)
        data_string=' '.join(data)
        print(count)

        return data_string, count, text1

    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    # amsterdamsexxx.com
    # mango6.info
    # hot-cams.nl
    url = "http://" + "wowtrannyporn.com"
#amsterdamsexxx.com
    # urlopen()으로 데이터 가져오기 --- (※1)
    response = requests.get(url)
    res = response.text


    # BeautifulSoup으로 분석하기 --- (※2)
    html = BeautifulSoup(res, "html.parser")
    text = pre_process(html)
    #print(summarizer.summarize(text))
    print("Text Rank:")
    data_string = ' '.join(keywords.keywords(text, words=20, split=True, language='english'))
    list_string = data_string.split()
    print(list_string)

    print("TF-IDF: ")
    print(tfidf_parse(text))

