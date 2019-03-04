from bs4 import BeautifulSoup
import urllib.request as req
import requests
import re
import nltk
from nltk.stem.snowball import SnowballStemmer
#nltk.download('punkt')
#nltk.download('stopwords')
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter

import matplotlib.pyplot as plt

stopwords = nltk.corpus.stopwords.words('english') # '은,는,이,가' 이런거 없애주는 사전
stemmer = SnowballStemmer("english")  # 부사,형용사 이런걸 어근으로 바꿔줌


# HTML 파일 전처리 함수
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

    return text.lower()


def wordCounter(soup):
    #text = soup.read()
    word_list = soup.replace(',', ' ').replace('.', ' ').split()
    word_list_no_duplicate = list(set(word_list))
    word_count = []
    for word in word_list_no_duplicate:
        word_count.append((word_list.count(word), word))
    n = 0
    for result in sorted(word_count, reverse=True):
        n += 1
        print(result[1], ':', result[0])
        if n == 50:
            break

def tokenize_and_stem(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    stems = [stemmer.stem(t) for t in filtered_tokens]
    return stems

def tokenize_only(text):
    # first tokenize by sentence, then by word to ensure that punctuation is caught as it's own token
    tokens = [word.lower() for sent in nltk.sent_tokenize(text) for word in nltk.word_tokenize(sent)]
    filtered_tokens = []
    # filter out any tokens not containing letters (e.g., numeric tokens, raw punctuation)
    for token in tokens:
        if re.search('[a-zA-Z]', token):
            filtered_tokens.append(token)
    return filtered_tokens



if __name__ == "__main__":
    # amsterdamsexxx.com
    # mango6.info
    url = "http://" + "amsterdamsexxx.com"

    # urlopen()으로 데이터 가져오기 --- (※1)
    response = requests.get(url)
    res = response.text


    # BeautifulSoup으로 분석하기 --- (※2)
    html = BeautifulSoup(res, "html.parser")
    text = pre_process(html)

    text1 = []
    #url = []
    max_document_length = 0

    str = tokenize_and_stem(text)
    #print(str)
    if len(str) > max_document_length:
        max_document_length = len(str)
    text1.append(' '.join(str))  # join: list -> str
    #url.append(i[0])
    #print(text1)
    #print(text1[:2])

    count_vectorizer = CountVectorizer(stop_words=stopwords,
                                       #max_df=0.9,
                                       max_features=10000,
                                       min_df= 0.9,
                                       #ngram_range=(1,2),
                                       tokenizer=tokenize_only
                                        )

    X = count_vectorizer.fit_transform(text1)
    #word_vec = count_vectorizer.vocabulary_
    #print(word_vec)
    vocab = list(count_vectorizer.get_feature_names())
    counts = X.sum(axis=0).A1

    freq_distribution = Counter(dict(zip(vocab, counts)))
    print(freq_distribution.most_common(20))
    temp=[]
    for word in freq_distribution.most_common(20):
        #print(word[0])
        temp.append(word[0])
    most20_word_str = ' '.join(temp)
    print(most20_word_str)
    print(most20_word_str.split())
    #tfidv = TfidfVectorizer().fit(corpus)

    #terms = count_vectorizer.get_feature_names()
    #print(terms)


    #plt.savefig('C:/Users/DBLAB/Desktop/ward_clusters.png', dpi=200)  # save figure as ward_clusters
    #wordCounter(text)