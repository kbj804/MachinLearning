from bs4 import BeautifulSoup
import urllib.request as req
import requests
import re
import nltk
import pymysql
import logging
from nltk.stem.snowball import SnowballStemmer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from collections import Counter
import matplotlib.pyplot as plt


#nltk.download('punkt')
#nltk.download('stopwords')

stopwords = nltk.corpus.stopwords.words('english') # '은,는,이,가' 이런거 없애주는 사전
stemmer = SnowballStemmer("english")  # 부사,형용사 이런걸 어근으로 바꿔줌

generate_sql = "select url, url_id from collected_url where degree=4"

def pre_process(soup):
    # kill all script and style elements
    for script in soup(["script", "style"]):
         script.extract()  # rip it out

    # get text
    text = soup.get_text()

    # break into lines and remove leading and trailing space on each
    lines = (line.strip() for line in text.splitlines())
    # break multi-headlines into a line each
    chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
    # drop blank lines
    text = '\n'.join(chunk for chunk in chunks if chunk)

    return text.lower()

def generate_url():  # return generate urls

    with connection.cursor() as curs:
        curs.execute(generate_sql)
        generate_urls = curs.fetchmany(size=10)
        print(generate_urls)
        connection.commit()

    return generate_urls


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

def parse_data(generate_url): #parse the url to create outlink urls.
    try: # this try is to catch HTTP GET exception.
        response = requests.get("http://" + generate_url, timeout=3)  # need to modify to adapt "http or https"
        res = response.text
        html = BeautifulSoup(res, "html.parser")
        text = pre_process(html)

        text1 = []
        # url = []
        max_document_length = 0

        str = tokenize_and_stem(text)
        if len(str) > max_document_length:
            max_document_length = len(str)
        text1.append(' '.join(str))  # join: list -> str

        count_vectorizer = CountVectorizer(stop_words=stopwords,
                                           # max_df=0.9,
                                           max_features=10000,
                                           min_df=0.9,
                                           # ngram_range=(1,2),
                                           tokenizer=tokenize_only
                                           )

        X = count_vectorizer.fit_transform(text1) # 데이터 백터화

        vocab = list(count_vectorizer.get_feature_names())
        counts = X.sum(axis=0).A1 # 단어 카운트

        freq_distribution = Counter(dict(zip(vocab, counts)))
       # print(freq_distribution.most_common(20))
        data = []
        for word in freq_distribution.most_common(20):
            print(word[0])
            data.append(word[0])
        data_string=' '.join(data)

        return data_string

    except:
        print("####  FAIL TO INSERT WORD DATA ####")





if __name__ == "__main__":
    while 1:
        connection = pymysql.connect(host='localhost', user='root', password='1234', db='bjcrawl', charset='utf8')
        try:
            generated = generate_url()
            for origin_url in generated:
                most20_word = parse_data(origin_url[1])
                print(most20_word)
            connection.close()


        except:
            connection.close()
            logger.error('Deadlock has occured.')