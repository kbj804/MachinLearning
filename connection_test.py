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
stopwords.append('\'s')
stopwords.append('n\'t')
stemmer = SnowballStemmer("english")  # 부사,형용사 이런걸 어근으로 바꿔줌

harmful_url_dic = {'sex': 1, 'porn': 1, 'gay': 1, 'movi': 1, 'movie': 1, 'free': 1, 'tube': 1, 'video': 1, 'phone': 1, 'cam': 1,
                   'live': 1, 'xxx': 1, 'matur': 1, 'fuck': 1, 'pic': 1, 'chat': 1, 'dick': 1,    'hot': 1, 'amateur': 1, 'site': 1,
                   'webcam': 1, 'anal': 1, 'boy': 1, 'asian': 1, 'milf': 1, 'adult': 1,    'big':1 , 'shemal': 1, 'best': 1, 'cartoon':1,
                   'pictur': 1, 'picture': 1, 'lesbian': 1,

                   'teen': 2, 'big': 2, 'girl': 2, 'sex': 2, 'fuck': 2, 'video': 2, 'porn': 2, 'pussi': 2, 'ass': 2, 'tit': 2,
                   'matur': 2, 'babe': 2, 'hot': 2, 'amateur': 2, 'cock': 2, 'asian': 2, 'anal': 2,    'milf': 2, 'sexi': 2, 'black': 2,
                   'lesbian': 2, 'watch': 2, 'pic': 2, 'blond': 2, 'nude': 2,    'free': 2, 'hairi': 2, 'blowjob': 2, 'cum': 2, 'young': 2,
                   'shemal': 2, 'hardcor': 2, 'hardcore': 2 ,

                   'game': 3, 'casino': 3, 'play': 3, 'onlin': 3, 'free': 3, 'review': 3, 'mobil': 3, 'download': 3, 'travel': 3,
                   'best': 3, 'home': 3, 'hotel': 3, 'live': 3, 'read': 3, 'new': 3, 'info': 3,    'video': 3, 'tip': 3, 'educ': 3,
                   'contact': 3, 'site': 3, 'machin': 3, 'guid': 3, 'kid': 3,    'app': 3, 'discount': 3, 'sport': 3, 'sex': 3, 'learn': 3,
                   'card': 3, 'insur': 3, 'news': 3,    'race': 3, 'real': 3, 'dress': 3, 'visit': 3, 'admin': 3, 'softwar': 3,

                   'escort': 4, 'london': 4, 'servic': 4, 'girl': 4, 'agenc': 4, 'home': 4, 'contact': 4, 'directori': 4,
                   'galleri': 4, 'new': 4, 'read': 4, 'massag': 4, 'model': 4, 'link': 4, 'blog': 4,    'review': 4, 'femal': 4, 'fmale': 4,
                   'view': 4, 'vip': 4, 'asian': 4, 'book': 4, 'rate': 4, 'high': 4,    'uk': 4, 'sex': 4, 'russian': 4, 'profil': 4,
                   'busti': 4, 'class': 4, 'adult': 4, 'sexi': 4,    'blond': 4, 'york': 4, 'list': 4, 'guid': 4, 'comment': 4, 'date': 4
}


generate_sql = "select url_id, url from harmful_weight where top_word is null "
save_wd = "update harmful_weight set harmful_word_num=%s, top_word=%s where url_id=%s"
insert_txt="insert into en_data (url_id, text) values(%s,%s)"

fail_acceses = "update harmful_weight set top_word=0 where url=%s"
fail_lang = "update harmful_weight set top_word=1 where url_id=%s"

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
        #connection.commit()

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

def parse_word(generate_url): #parse the url to create outlink urls.
    try: # this try is to catch HTTP GET exception.
        response = requests.get("http://" + generate_url, timeout=3)  # need to modify to adapt "http or https"
        res = response.text
        html = BeautifulSoup(res, "html.parser")
        text = pre_process(html)
        print("connection . . . . . . . .  .  " + generate_url)
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
                                           min_df=0.8,
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
            #print(word[0])
            data.append(word[0])

        count = count_harmful_word(data)
        data_string=' '.join(data)
        return data_string, count, text1


    except:
        with connection.cursor() as curs:
            curs.execute(fail_acceses, (generate_url))
        print("####  FAIL TO INSERT WORD DATA URL : "+ generate_url)


def save_word(str_top_word, count_word, url_id, text):
    try:
        with connection.cursor() as curs:
            curs.execute(save_wd, (count_word, str_top_word, url_id))
            curs.execute(insert_txt, (url_id, text))
            print("Insert Complete : ")
    except:
        with connection.cursor() as curs:
            curs.execute(fail_lang, url_id)
            print("Maybe, FAIL TO INCODING....! ")

def count_harmful_word(top20):
    harmful_word_num = 0
    for word in top20: # top 20 word
        if word in harmful_url_dic:
            harmful_word_num += 1
            #if harmful_url_dic.get(word) == 1: idx += 1

    return harmful_word_num

if __name__ == "__main__":
    while 1:
        try:
            connection = pymysql.connect(host='localhost', user='root', password='1234', db='bjcrawl', charset='utf8')

            generated = generate_url()
            for origin_url in generated:
                # origin_url[0] : url_id
                # origin_url[1] : url
                most20_word, count, text = parse_word(origin_url[1]) # top 20 word 정보 str로 반환
                save_word(most20_word, count, origin_url[0], text)
                #print(most20_word)

            connection.commit()
            connection.close()


        except Exception as ex:
            print(" ###### Deadlock Occured ! ! ! ######   ", ex)
            connection.commit()
            connection.close()
