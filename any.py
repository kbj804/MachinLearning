import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from tldextract import extract
from summa import summarizer
import graphviz




harmful_url_dic = {'sex': 1, 'porn': 1, 'gay': 1, 'movi': 1, 'movie': 1, 'free': 1, 'tube': 1, 'video': 1, 'phone': 1, 'cam': 1,
                   'live': 1, 'xxx': 1, 'matur': 1, 'fuck': 1, 'pic': 1, 'chat': 1, 'dick': 1,    'hot': 1, 'amateur': 1, 'site': 1,
                   'webcam': 1, 'anal': 1, 'boy': 1, 'asian': 1, 'milf': 1, 'adult': 1,    'big':1 , 'shemal': 1, 'best': 1, 'cartoon':1,
                   'pictur': 1, 'picture': 1, 'lesbian': 1,

                   'teen': 2, 'big': 2, 'girl': 2, 'sex': 2, 'fuck': 2, 'video': 2, 'porn': 2, 'pussi': 2, 'ass': 2, 'tit': 2,
                   'matur': 2, 'babe': 2, 'hot': 2, 'amateur': 2, 'cock': 2, 'asian': 2, 'anal': 2,    'milf': 2, 'sexi': 2, 'black': 2,
                   'lesbian': 2, 'watch': 2, 'pic': 2, 'blond': 2, 'nude': 2,    'free': 2, 'hairi': 2, 'blowjob': 2, 'cum': 2, 'young': 2,
                   'shemal': 2, 'hardcor': 2, 'hardcore': 2 ,

                   'game': 3, 'casino': 3, 'play': 3, 'onlin': 3, 'free': 3, 'review': 3, 'mobil': 3, 'download': 3, 'travel': 3,
                   'best': 3, 'home': 3, 'hotel': 3, 'live': 3, 'read': 3, 'new': 3, 'info': 3,    'video': 3, 'tip': 3,
                   'contact': 3, 'site': 3, 'machin': 3, 'guid': 3, 'kid': 3,    'app': 3, 'discount': 3, 'sport': 3, 'sex': 3, 'learn': 3,
                   'card': 3, 'insur': 3, 'news': 3,    'race': 3, 'real': 3, 'dress': 3, 'visit': 3, 'admin': 3, 'softwar': 3,

                   'escort': 4, 'london': 4, 'servic': 4, 'girl': 4, 'agenc': 4, 'home': 4, 'contact': 4, 'directori': 4,
                   'galleri': 4, 'new': 4, 'read': 4, 'massag': 4, 'model': 4, 'link': 4, 'blog': 4,    'review': 4, 'femal': 4, 'fmale': 4,
                   'view': 4, 'vip': 4, 'asian': 4, 'book': 4, 'rate': 4, 'high': 4,    'uk': 4, 'sex': 4, 'russian': 4, 'profil': 4,
                   'busti': 4, 'class': 4, 'adult': 4, 'sexi': 4,    'blond': 4, 'york': 4, 'list': 4, 'guid': 4, 'comment': 4, 'date': 4
}

def count_child_num(generate_url):
    req = requests.get("http://" + generate_url, timeout=3)  # need to modify to adapt "http or https"
    html = req.text

    soup = BeautifulSoup(html, 'html.parser')
    urls = soup.find_all('a', href=True)
    urls_set = set()  # make set to remove duplication.
    data = ''  # to save text data
    for url in urls:

        if url.text != '' or url.text != ' ':
            data = data + url.text.replace('\n', '').replace('\r', '') + ' '
        try:
            str = urlparse(url['href']).netloc  # by using urlparse, we can check it is http:// or https:// etc.
            if str != "":
                urls_set.add(extract("http://" + str.replace(" ", "")).registered_domain)
        except:
            print("URL not Valid : %s" + url)
    print(urls_set)
    try:  # this try is to catch set error.
        urls_set.remove("")
        return len(urls_set)

    except:
        return len(urls_set)


def count_harmful_word(top20):
    harmful_word_num = 0
    for word in top20: # top 20 word
        if word in harmful_url_dic:
            harmful_word_num += 1
            print(word)
            #if harmful_url_dic.get(word) == 1: idx += 1

    return harmful_word_num



def count_img_num(generate_url):
    req = requests.get("http://" + generate_url, timeout=3)  # need to modify to adapt "http or https"
    html = req.text

    soup = BeautifulSoup(html, 'html.parser')
    imgs = soup.find_all('img')
    imgs_set = set()  # make set to remove duplication.
    #print(imgs)
    return len(imgs)

def exe(url):
    print("child_num : ", count_child_num(url))
    print("img num : ", count_img_num(url))


def class_(top20):
    list = top20.split()
    for word in list:
        if word in harmful_url_dic:
            return harmful_url_dic[word]
            break;

    return 0

str1 = "porn sex free video teen movi tube gay girl escort milf xxx adult webcam porno colleg toy mobil amateur cam"
str2 = "vlr fosdj dsfnaj dslfjan dsflakjnf sldfka asdfka sdkf kdsl cam porn"
url = "pornvideobook.com"


print(class_(str1))

