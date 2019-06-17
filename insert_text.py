import pymysql


generate_sql = "SELECT url_id, url FROM bjcrawl.final_result where url_idx =0"
# select url_id, url, harmful_count from collect_endata where harmful=7 and white_visit=0
s = "select text from en_data where url_id = %s"
update_sql = "update final_result set text=%s where url_id=%s"
# ref_count

# harmful_1_seed2
up_visit = "update final_result set url_idx = url_idx+1 where url_id=%s"


harmful_url_word = [
    ('sex', 1), ('porn', 1), ('gay', 1), ('xxx', 1), ('fuck', 1), ('shemal', 1), ('lesbian', 1),('dick', 1),('spank',1),
    ('teen', 2), ('girl', 2), ('pussi', 2), ('ass', 2), ('babe', 2), ('cock', 2), ('anal', 2), ('milf', 2), ('blond', 2), ('nude', 2), ('blowjob', 2),('cum', 2), ('young', 2),
    ('game', 3), ('casino', 3), ('card', 3), ('race', 3),('porker',3),('gamb',3),
    ('escort', 4), ('servic', 4),
    ('cam', 5), ('chat',5)
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
                url_id = url_info[0]
                curs.execute(up_visit, url_info[0])  # white_visit + 1
                curs.execute(s,url_info[0])
                text = curs.fetchone()
                curs.execute(update_sql, (text,url_info[0]) )
                #connection.commit()


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

            connection.commit()
            connection.close()

        except:
            connection.commit()
            connection.close()
            print(" ###### Deadlock Occured ! ! ! ######")