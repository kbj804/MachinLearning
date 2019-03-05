

harmful_url_word = [
    ('sex', 1), ('porn', 1), ('gay', 1), ('cam', 1), ('xxx', 1), ('fuck', 1), ('shemal', 1), ('lesbian', 1),('dick',1),
    ('teen', 2), ('girl', 2), ('pussi', 2), ('ass', 2), ('babe', 2), ('cock', 2), ('anal', 2), ('milf', 2), ('blond', 2), ('nude', 2), ('blowjob', 2),('cum', 2), ('young', 2),
    ('game', 3), ('casino', 3), ('card', 3), ('race', 3),
    ('escort', 4), ('servic', 4)
]

harmful_url_dic = {'sex': 1, 'porn': 1, 'teen': 2, 'game': 3, 'escort': 4}

def count_harmful_word_num(str):
    harmful_word_num = 0
    idx=0
    idx1 = 0
    idx2 = 0
    idx3 = 0
    idx4 = 0
    for word in harmful_word: # [0]:word , [1]:idx
        if word[0] in str:
            harmful_word_num += 1
            if word[1] == 1 : idx1 +=1
            elif word[1] == 2 : idx2 +=1
            elif word[1] == 3 : idx3 +=1
            elif word[1] == 4 : idx4 +=1
            idx = max(idx1,idx2,idx3,idx4)
    return harmful_word_num, idx


# 딕셔너리 이용해서 word count 하면 될듯!
def fuck(url):
    try:
        print(url in harmful_url_dic)


        if url in harmful_url_dic:
            print(harmful_url_dic[url])


    except:
        print("asd")

fuck('game')
#print(count_harmful_word_num('casino'))