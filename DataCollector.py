from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse
from langdetect import detect_langs
import pymysql
import logging
from tld import get_tld
from tldextract import extract
import re
import time
import string

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(message)s')

ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(formatter)
logger.addHandler(ch)

find_url_sql = "select url from collected_url where url=%s"
find_url_id_sql = "select url_id from collected_url where url=%s"
find_auto_increment_sql = "select AUTO_INCREMENT from information_schema.TABLES where TABLE_SCHEMA =%s and TABLE_NAME=%s"


insert_sql = "insert into collected_url (url, visited, parents, country) values(%s, %s, %s, %s)"
insert_en_data_sql = "insert into en_data (url_id, text_data) values(%s, %s)"
insert_an_data_sql = "insert into another_data (url_id, text_data, lang) values(%s, %s, %s)"
insert_relation_sql = "insert into url_relation (parent_id, child_id) values(%s,%s)"
# visited state -
# 0:not visited yet,
# 1:visited,
# 2:visited and redirect to warning,
# 3:visited but not exist

generate_sql = "select url, url_id from collected_url where visited=0"
after_generate_exist_sql = "update collected_url set visited=1, child_num=%s where url=%s"
after_generate_warning_sql = "update collected_url set visited=2, harmful=1 where url=%s"
after_generate_not_exist_sql = "update collected_url set visited=3 where url=%s"

update_url_sql = "update collected_url set child=%s, parent=%s where url=%s"
dup_update_sql = "update collected_url set ref_count= ref_count+1 where url=%s"
##determine where to put visit check SQL. 1.at generate_url()-default, 2.parsed_data()-can check orgin url is valid or not. , 3.save_db()


def generate_url():  # return generate urls
    connection = pymysql.connect(host='localhost', user='bj', password='1234', db='url_db', charset='utf8')
    with connection.cursor() as curs:
        curs.execute(generate_sql)
        generate_urls = curs.fetchmany(size=10)
        print(generate_urls)
        #for url in generate_urls :
        #    curs.execute(after_generate_exist_sql,url[0])
        connection.commit()
        connection.close()
    return generate_urls  # need to tokenize ( generate_urls -> generate_url )


def parse_data(generate_url): #parse the url to create outlink urls.
    connection = pymysql.connect(host='localhost', user='bj', password='1234', db='url_db', charset='utf8')
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

def save_db(origin_url_id, text_data, urls_set, result, lang):
    # sould use 'try-finally' and 'with' because connection to db can cause connection leak when it raise exceptions.
    connection = pymysql.connect(host='localhost', user='bj', password='1234', db='url_db', charset='utf8')
    try:
        with connection.cursor() as curs:
            for url in urls_set: # insert new url info.
                if curs.execute(find_url_id_sql, (url)) == 0:  # when new url is not in database.
                    curs.execute(insert_sql, (url, 0, origin_url_id, lang))
                    logger.info("Inserted : " + url)
                else:
                    curs.execute(dup_update_sql,url)
                    logger.info("Duplicated : " + url)
            connection.commit()
            for url in urls_set: #insert url relation info.
                curs.execute(find_url_id_sql,url)
                child_id = curs.fetchone()[0]
                if origin_url_id != child_id :
                    curs.execute(insert_relation_sql,(origin_url_id,child_id))
                    #curs.execute(update_url_sql,(child_id, origin_url_id,url))
            connection.commit()
            if text_data !="" and result == 1:
                curs.execute(insert_en_data_sql,(origin_url_id,text_data)) # insert url text data info.
            elif text_data!="" and result ==2:
                curs.execute(insert_an_data_sql,(origin_url_id, text_data, lang))
        connection.commit()
    finally:
        connection.close()



#if __name__ == "__main__":
 #   generated = generate_url()
  #  for origin_url in generated:
   #         parsed, text_data, result = parse_data(origin_url[0])
    #        save_db(origin_url[1], text_data, parsed, result)

if __name__ == "__main__":
    while 1:
        try:
            generated = generate_url()
            for origin_url in generated:
                    parsed, text_data, result, lang = parse_data(origin_url[0])
                    print(origin_url,
                          "origin_url[0] = "+ origin_url[0])
                    print(parse_data(origin_url[0]))
                    save_db(origin_url[1], text_data, parsed, result, lang)
            time.sleep(1)
        except:
            logger.error('Deadlock has occured.')