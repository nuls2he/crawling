import schedule
import time

# 원본 데이터 가져오기
import pymysql.cursors
def main():
    # def job():
    conn = pymysql.connect(
        host='192.168.0.61',
        user='day',
        password='word',
        db='one_db',
        charset='utf8mb4'
    )
    cursor = conn.cursor()

    sql = 'SELECT ono, originaldata, siteno FROM test_original WHERE state = %s'
    cursor.execute(sql, 'N')

    original = cursor.fetchall()

    print('original data')
    print(original)

    # 신조어 필터링
    sql = 'SELECT word FROM tb_newdic'
    cursor.execute(sql)

    newdic = cursor.fetchall()

    # print('신조어 사전')
    # print(newdic)

    # 예외사전 데이터 가져오기
    sql = 'SELECT word FROM tb_excdic'
    cursor.execute(sql)

    excdic = cursor.fetchall()
    print('예외 사전')
    print(excdic)


    originalList = []
    for data in original:
        dataList = list(data)

        for word in newdic:
            sql = 'SELECT INSTR(%s, %s)'
            cursor.execute(sql, (dataList[1], word[0]))

            count = cursor.fetchone()

            if count[0] != 0:
                print(dataList[1], '에서', word[0], '은(는) 신조어 사전에 존재하는 단어입니다.')
                dataList[1] = dataList[1].replace(word[0], '')

                sql = 'INSERT INTO test_keyword (ono, keyword, siteno) VALUES (%s, %s, %s)'
                cursor.execute(sql, (dataList[0], word[0], dataList[2]))
                conn.commit()

        for word in excdic:
            sql = 'SELECT INSTR(%s, %s)'
            cursor.execute(sql, (dataList[1], word[0]))

            count = cursor.fetchone()

            if count[0] != 0:
                print(dataList[1], '에서', word[0], '은(는) 예외 사전에 존재하는 단어입니다.')
                dataList[1] = dataList[1].replace(word[0], '')

        originalList.append(dataList)

    original = originalList

    # 트위터로 분석
    from konlpy.tag import Twitter
    twitter = Twitter()

    tresult = []

    for data in original:
        tresult.append([data[0], twitter.nouns(data[1]), data[2]])
        print(twitter.pos(data[1]))

    # 트위터 분석 결과 확인
    print('twitter result')
    print(tresult)

    # 코모란으로 분석
    from konlpy.tag import Komoran
    komoran = Komoran()



    kresult = []

    for data in tresult:
        words = data[1]

        # 문제 없이 분석과 처리과 완료되었는지 체크용, 완료 성공 시 True, 실패 시 False
        state = True

        for word in words:
            try:
                type = komoran.pos(word)[0][1]
                if type == 'NNG' or type == 'NNP':
                    kresult.append([data[0], komoran.morphs(word)[0]])

                    # 예외 사전에 존재 유무 체크용, True가 있는경우, False가 없는경우
                    exist = False
                    # 예외 사전에 있는 단어는 INSERT 전에 필터링
                    for exc in excdic:
                        sql = 'SELECT INSTR(%s, %s)'
                        cursor.execute(sql, (word, exc[0]))

                        count = cursor.fetchone()
                        if count[0] != 0:
                            print(word + '은(는) 사전의 ' + exc[0] + '와(과) 일치')
                            exist = True
                            break

                    if exist:
                        continue

                    # NNG, NNP 타입만 DB에 INSERT
                    # 예외 발생 시 rollback, 아닌 경우 commit으로 처리
                    sql = 'INSERT INTO test_keyword (ono, keyword, siteno) VALUES (%s, %s, %s)'

                    try:
                        if len(komoran.morphs(word)[0]) != 1:
                            cursor.execute(sql, (data[0], komoran.morphs(word)[0], data[2]))

                    except Exception as err:
                        state = False
                        print('ERROR : komoran result의 ' + str(data[0]) + '번 글의 에서 insert 처리 중 오류 발생')
                        print(str(err))
                        conn.rollback()
                    else:
                        conn.commit()

            except Exception as err:
                state = False
                print('ERROR : komoran 키워드 분석 중 오류 발생')
                continue

        ssql = 'UPDATE test_original SET state = %s WHERE ono = %s'
        state = 'Y' if state == True else 'E'
        cursor.execute(ssql, (state, data[0]))

        conn.commit()

    # 코모란 분석 결과 확인
    print('komoran result')
    print(kresult)

    print('-----')
    print('끝')

# schedule.every().day.at("").do(job)
#
# while 1:
#     schedule.run_pending()
#     time.sleep(1)