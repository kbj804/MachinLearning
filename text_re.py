import re
from collections import Counter
text = '\
escort \
service \
london \
custom \
agency \
company \
manage \
help \
vip \
profile \
product \
web \
offer \
work \
support \
model \
data \
market \
local \
any \
design \
secure \
'
#word=text.split()
#print(word)

#for i in word:
#    print('\''+ i + '\'' + ': 7, ')

harmful_url_dic = {

    'adult': 0, 'material': 0, 'age': 0, 'any': 0, 'view': 0, 'sexual': 0, 'enter': 0, 'explicit': 0, 'access': 0,
    'agree': 0, 'email':0,
     'content': 0, 'community': 0, 'pleas': 0, 'use': 0, 'click': 0, 'condition': 0, 'term': 0,
    'right': 0, 'old': 0, 'download': 0,
    'image': 0, 'action': 0,

    'cam': 2, 'live': 2,  'chat': 2, 'webcam': 2, 'model': 2, 'amateur': 2, 'fetish': 2, 'show': 2, 'gay': 2,
    'link': 2, 'join':2,
    'xxx': 2, 'nude': 2, 'gallery': 2, 'top': 2, 'love': 2,

    'fuck': 3, 'cock': 3, 'like': 3, 'watch': 3, 'see': 3, 'pussi': 3, 'guy': 3, 'post': 3, 'one': 3,
     'hard': 3, 'enjoy': 3, 'go': 3, 'scene': 3, 'today': 3, 'black': 3, 'take': 3, 'blond': 3, 'suck': 3,

    'browser': 4, 'javascript': 4,  'chang': 4, 'set': 4, 'upgrade': 4, 'enable': 4, 'cooki': 4, 'page':4, 'domein':4,
    'require': 4, 'expiration': 4, 'domain' : 4, 'buy':4, 'gateway':4, 'error': 4, 'found': 4, 'address':4,'forbidden':4,
    'any': 4, 'one': 4, 'request':4, 'redirect':4,
    #'look': 4, 'app': 4, 'movi': 4,  'web': 4, 'digit': 4, 'need': 4, 'latest': 4,


    'game': 5, 'casino': 5, 'play': 5,  'mobil': 5,  'travel': 5, 'race': 5,
    'info': 5, 'tip': 5, 'royal':5, 'cash':5, 'bonus':5, 'slot':5, 'bingo':5,
    'educat': 5, 'machin': 5, 'guid': 5, 'kid': 5,  'discount': 5, 'sport': 5, 'insur': 5, 'learn': 5,
    'card': 5, 'poker':5,

     'anal': 6, 'tube': 6,  'xxx': 6, 'tit': 6,  'matur': 6,
    'milf': 6, 'pic': 6, 'espa':6, 'fran':6, 'ol':6,
    'asian': 6,   'young': 6, 'mom': 6,  'hardcore': 6,

    'escort': 7, 'service': 7, 'london': 7, 'custom': 7, 'agency': 7, 'company': 7, 'manage': 7, 'help': 7, 'vip': 7,
    'profile': 7, 'product': 7, 'italiana':7, 'profil':7, 'club':7, 'home':7, 'cart':7, 'review':7,
     'offer': 7, 'work': 7, 'support': 7,  'data': 7, 'market': 7, 'local': 7, 'any': 7,
    'design': 7, 'secure': 7, 'messag':7, 'date':7, 'massag':7,

}

harmful_url_dic2 ={
'adult': 2,  'amateur': 6, 'app': 5, 'black': 6, 'blond': 6, 'cock': 6, 'download': 5, 'casino': 5,
'explicit': 4, 'fuck': 6, 'live': 5, 'love': 3, 'model': 7, 'movi': 6, 'nude': 6, 'plea': 4,  'pussi': 6, 'escort':7,
 'web': 7, 'cam':2 ,'chat':2, 'gateway':4, 'ngnix':4 ,'london':7, 'watch':3, 'fetish':6, 'domain' : 4
}

def count_harmful_word(word):
    top20 = word.split()
    harmful_word_num = 0
    i=[]
    for word in top20: # top 20 word
        if word in harmful_url_dic:
            i.append(harmful_url_dic.get(word))
            if word in harmful_url_dic2:
                i.append(harmful_url_dic2.get(word))
    return i

def generate(List):
    w_count = {}
    for lst in List:
        try: w_count[lst] += 1
        except: w_count[lst]=1
    mlabel=0
    count=0
    print(w_count)


    for label in w_count.keys():
        print(label)
        if count <= w_count.get(label):
            print(w_count.get(label))
            count = w_count.get(label)
            mlabel = label
        else:
            print(label)
    return mlabel


text = "free http good adult bukkak slut webmast porn rate tampa black blaqu phoenixxx review veri websit dirti excel fair get"
myList = count_harmful_word(text)
print(myList)
print("Lable ", generate(myList))

#print (key, result[key])

