import pymysql

generate_sql = "select url_id, url, harmful_count from collect_endata where harmful=2 and white_visit=0"
insert_sql = "insert into harmful_weight (url_id, url, url_harmful_idx, harmful_child_num) values(%s,%s,%s,%s)"

up_visit = "update collect_endata set white_visit = white_visit+1 where url_id=%s"
update_harmful_url = "update harmful_weight set url_harmful_idx= %s where url_id=%s "

harmful_url_word = [
    ('sex', 1), ('porn', 1), ('gay', 1), ('cam', 1), ('xxx', 1), ('fuck', 1), ('shemal', 1), ('lesbian', 1),('dick', 1),('spank',1),
    ('teen', 2), ('girl', 2), ('pussi', 2), ('ass', 2), ('babe', 2), ('cock', 2), ('anal', 2), ('milf', 2), ('blond', 2), ('nude', 2), ('blowjob', 2),('cum', 2), ('young', 2),
    ('game', 3), ('casino', 3), ('card', 3), ('race', 3),('porker',3),('gamb',3),
    ('escort', 4), ('servic', 4)
]

def generate_url():  # return generate urls
    with connection.cursor() as curs:
        curs.execute(generate_sql)
        generate_urls = curs.fetchmany(size=10)
        print(generate_urls)

    return generate_urls

def save_url_idx(url_info):
        # url_harmful_idx
        # 1: 성인 비디오 사이트
        # 2: 아청 유해 사이트
        # 3: 도박 사이트
        # 4: 성매매 사이트
        with connection.cursor() as curs:
            try:
                url = url_info[1]
                curs.execute(up_visit, url_info[0])  # white_visit + 1
                curs.execute(insert_sql, (url_info[0], url_info[1], 0 , url_info[2]))
                #connection.commit()
                print("Insert URL : " + url)
                for word in harmful_url_word:  # [0]:word , [1]:idx
                     if word[0] in url:
                        curs.execute(update_harmful_url,  (word[1], url_info[0]))
                        print("Update Harmful URL word :  " + word[0])
                        break;

            except:
                print("I dont know why occured this error")

if __name__ == "__main__":
    while 1:
        try:
            connection = pymysql.connect(host='localhost', user='root', password='1234', db='bjcrawl', charset='utf8')
            generated = generate_url()
            for origin_url in generated:
                save_url_idx(origin_url)  # 새 테이블에 URL정보와 IDX 저장

            connection.commit()
            connection.close()

        except:
            connection.commit()
            connection.close()
            print(" ###### Deadlock Occured ! ! ! ######")