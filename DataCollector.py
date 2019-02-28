import csv, codecs
from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
# from langdetect import detect_langs
# import pymysql
# import logging
# from tld import get_tld
# from tldextract import extract
import re
import time




def parse_data(generate_url): #parse the url to create outlink urls.
    #connection = pymysql.connect(host='localhost', user='bj', password='1234', db='url_db', charset='utf8')
    try: # this try is to catch HTTP GET exception.
        req = requests.get("http://" + generate_url, timeout=3)  # need to modify to adapt "http or https"
        html = req.text
        #when url redirect 'warning.or.kr'
        if get_tld(req.url) =='warning.or.kr':
            with connection.cursor() as curs:
                curs.execute(after_generate_warning_sql,(generate_url))
            connection.commit()
            connection.close()
        # when url normal --- deleted because deadlock. put in generate_url()
        else :
        #move to else phase...
            soup = BeautifulSoup(html, 'html.parser',from_encoding='utf-8')
            urls = soup.find_all('a', href=True)
            urls_set = set()  # make set to remove duplication.

            data = '' # to save text data
            for url in urls:
                if url.text != '' or url.text != ' ':
                    data = data + url.text.replace('\n', '').replace('\r', '') + ' '
                try:
                    str = urlparse(url['href']).netloc  # by using urlparse, we can check it is http:// or https:// etc.
                    if str != "":
                        urls_set.add(extract("http://" + str.replace(" ", "")).registered_domain)
                except:
                    logger.error("URL not Valid : %s"%url)
            try: # this try is to catch set error.
                urls_set.remove("")

            finally:
                #data = re.sub('[^0-9a-zA-Z\\s\\.\\,]', '', data).lower()[:-1]
                #data = re.sub('\\s+', ' ', data)[:1000]
                with connection.cursor() as curs:
                    curs.execute(after_generate_exist_sql, (len(urls_set), generate_url))
                    print("Update visited url = " + generate_url)
                connection.commit()
                connection.close()
                # can check url is redirected by req.url vs generate_url


                data_lang = re.sub('\\s+', ' ', data)[:1000]
                data = re.sub('[^0-9a-zA-Z\\s\\.\\,]', '', data_lang).lower()

                try:
                    # Use moudle -> https://pypi.python.org/pypi/langdetect
                    # result state
                    # 0 : no language!
                    # 1 : english!
                    # 2 : other language!

                    lang = detect_langs(data_lang)[0].lang
                    logger.info("Web Site Language : %s"%lang)
                    if lang == 'en':
                        result = 1
                        return urls_set, data, result, lang

                    elif bool(re.search('cn', lang)) or generate_url.endswith('.cn'):  # import string
                        print("China Number 99!")
                        return 0

                    else:
                        result = 2
                        return urls_set, data, result, lang

                except:
                    result = 0
                    return urls_set, data, result
    except:
        logger.error("URL not exist : %s"%generate_url)
        with connection.cursor() as curs:
            curs.execute(after_generate_not_exist_sql,(generate_url))
        connection.commit()
        connection.close()

# CSV 파일 열기
filename = "harmful_7_seed.csv"
fp = codecs.open(filename, "r", "EUC-KR")
# 한 줄씩 읽어 들이기
reader = csv.reader(fp, delimiter=",", quotechar='"')
for white_url in reader:
    #print(cells[1], cells[2])
    print(cells)


if __name__ == "__main__":
    while 1:
        try:
            # CSV 파일 열기
            filename = "harmful_7_seed.csv"
            fp = codecs.open(filename, "r", "EUC-KR")
            # 한 줄씩 읽어 들이기
            reader = csv.reader(fp, delimiter=",", quotechar='"')
            for white_url in reader:
                # print(cells[1], cells[2])
                parsed, text_data, result, lang = parse_data(white_url[1])
                print(white_url, "origin_url[0] = "+ white_url[1])
                print(parse_data(white_url[0]))
                save_db(white_url[1], text_data, parsed, result, lang)
            time.sleep(1)
        except:
            logger.error('Deadlock has occured.')