from bs4 import BeautifulSoup
import urllib.request as req
import requests
import re
import string
from collections import Counter

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

if __name__ == "__main__":
    # amsterdamsexxx.com
    # mango6.info
    url = "http://" + "mango6.info"

    # urlopen()으로 데이터 가져오기 --- (※1)
    response = requests.get(url)
    res = response.text

    # BeautifulSoup으로 분석하기 --- (※2)
    html = BeautifulSoup(res, "html.parser")
    text = pre_process(html)
    wordCounter(text)