import nltk

harmful_url_dic = {'sex': 1, 'porn': 1, 'gay': 1, 'movi': 1, 'movie': 1, 'free': 1, 'tube': 1, 'video': 1, 'phone': 1, 'cam': 1, 'pornhub':1,
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

stop_list = ['\'s','a','b','c','d,','e','f','g','h','i','j','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z',
             'com','www','net','ai','en','al','de','la','le','ol','un','http','https','arent','couldnt','didnt','dont','doe','doesnt','ha',
             'hadnt','hasnt','havent','isnt','might','mightnt','mustnt','neednt','shant','shes','shouldnt','shouldve','thatll','wa','wasnt','werent',
             'wont','wouldnt','youd','youll','youre','youve']
stopwords = nltk.corpus.stopwords.words('english') # '은,는,이,가' 이런거 없애주는 사전

for word in stop_list:
    stopwords.append(word)


harmful_url_dic_temp = {

    'adult': 0, 'material': 0, 'age': 0, 'any': 0, 'view': 0, 'sexual': 0, 'enter': 0, 'explicit': 0, 'access': 0,
    'agree': 0,
    'year': 0, 'web': 0, 'content': 0, 'community': 0, 'plea': 0, 'use': 0, 'click': 0, 'condition': 0, 'term': 0,
    'right': 0, 'old': 0, 'download': 0,
    'image': 0, 'action': 0,

    'cam': 2, 'live': 2, 'adult': 2, 'chat': 2, 'webcam': 2, 'model': 2, 'amateur': 2, 'fetish': 2, 'show': 2, 'gay': 2,
    'link': 2,
    'xxx': 2, 'nude': 2, 'gallery': 2, 'top': 2, 'love': 2,

    'fuck': 3, 'cock': 3, 'like': 3, 'watch': 3, 'see': 3, 'pussy': 3, 'guy': 3, 'post': 3, 'one': 3,
    'love': 3, 'hard': 3, 'enjoy': 3, 'go': 3, 'scene': 3, 'today': 3, 'black': 3, 'take': 3, 'blond': 3, 'suck': 3,

    'browser': 4, 'javascript': 4, 'plea': 4, 'change': 4, 'set': 4, 'upgrade': 4, 'enable': 4, 'cookie': 4,
    'require': 4, 'expiration': 4,
    'any': 4, 'one': 4, 'look': 4, 'app': 4, 'movie': 4, 'use': 4, 'web': 4, 'digit': 4, 'need': 4, 'latest': 4,
    'espa': 4, 'erot': 4,
    'et': 4, 'enter': 4, 'explicit': 4, 'event': 4, 'enjoy': 4, 'english': 4,

    'game': 5, 'casino': 5, 'play': 5, 'review': 5, 'mobile': 5, 'download': 5, 'travel': 5, 'race': 5, 'live': 5,
    'info': 5, 'tip': 5,
    'educate': 5, 'machine': 5, 'guide': 5, 'kid': 5, 'app': 5, 'discount': 5, 'sport': 5, 'insure': 5, 'learn': 5,
    'card': 5,

    'fuck': 6, 'pussy': 6, 'anal': 6, 'tube': 6, 'amateur': 6, 'xxx': 6, 'tit': 6, 'movie': 6, 'cock': 6, 'mature': 6,
    'milf': 6, 'pic': 6,
    'asian': 6, 'black': 6, 'nude': 6, 'young': 6, 'mom': 6, 'blond': 6, 'hardcore': 6,

    'escort': 7, 'service': 7, 'london': 7, 'custom': 7, 'agency': 7, 'company': 7, 'manage': 7, 'help': 7, 'vip': 7,
    'profile': 7, 'product': 7,
    'web': 7, 'offer': 7, 'work': 7, 'support': 7, 'model': 7, 'data': 7, 'market': 7, 'local': 7, 'any': 7,
    'design': 7, 'secure': 7

}