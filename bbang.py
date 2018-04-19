from selenium import webdriver
import pymysql.cursors
import math
import re

path = "C:/Users/Bit/Desktop/chromedriver_win32/chromedriver.exe"

number = 0
def calculationPage(firstNum):
    pageNo = (firstNum - number) / 50
    return math.ceil(pageNo) + 1 if (pageNo % 50) > 0 else int(pageNo + 1)

def selectDB(conn, cursor):

    global number

    try:
        sql = 'select max(no) as no from test_original where siteno = 1'
        cursor.execute(sql)
        number = cursor.fetchone()['no']

        # 디비 처음 생성치 처리
        if number is None:
            number = 32906714

    except Exception as e:
        print("error : " + e)
        print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ에러ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
    else:
        conn.commit()

    return

def insertDB(conn, cursor, data, dataNo):

    try:
        if data != " ":
            sql = 'insert into test_original(siteno, originaldata, state, no) values (%s, %s, %s, %s)'
            cursor.execute(sql, (1, data, 'N', dataNo))
    except Exception as e:
        print("error : " + e)
        print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ에러ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
        # print(result[1])
    else:
        conn.commit()

    return

def main():

    conn = pymysql.connect(
        host='192.168.0.61',
        user='day',
        password='word',
        db='one_db',
        charset='utf8mb4'
    )
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    driver = webdriver.Chrome(path)
    driver.get("http://cafe118.daum.net/_c21_/bbs_list?grpid=aVeZ&mgrpid=&fldid=8hHX&firstbbsdepth=2DAQzzzzzzzzzzzzzzzzzzzzzzzzzz&lastbbsdepth=2DAQgzzzzzzzzzzzzzzzzzzzzzzzzz&prev_page=1&page=1&listnum=50&sortType=")

    selectDB(conn, cursor)
    print("넘버 : " + str(number))
    scrapPageNo = calculationPage(int(driver.execute_script("return arguments[0].innerText;", driver.find_element_by_css_selector("#primaryContent > table > tbody > tr.pos_rel > td.cb.pos_rel > form:nth-child(4) > table > tbody > tr:nth-child(5) > td.num"))))

    print(scrapPageNo)
    lastDataNo = 54;
    arr = []
    noArr = []
    print("-- 쭉빵 시작 --")
    for x in range(1, scrapPageNo):
        driver.find_element_by_link_text(str(x)).click()
        arr.clear()
        noArr.clear()
        print("----------------%d 페이지----------------" % (x))
        for y in range(4, lastDataNo):
            dataNo = int(driver.execute_script("return arguments[0].innerText;", driver.find_element_by_css_selector("#primaryContent > table > tbody > tr.pos_rel > td.cb.pos_rel > form:nth-child(4) > table > tbody > tr:nth-child(%d) > td.num" % (y))))
                                                                                                                    # #primaryContent > table > tbody > tr.pos_rel > td.cb.pos_rel > form:nth-child(4) > table > tbody > tr:nth-child(33) > td.num
            if dataNo < number:
                print("-- 쭉빵 끝 --")
                conn.close()
                driver.close()
                return

            insertDB(conn, cursor, re.sub("[^가-힝0-9a-zA-Z\\s]", "", driver.execute_script("return arguments[0].innerText;",driver.find_element_by_css_selector("#primaryContent > table > tbody > tr.pos_rel > td.cb.pos_rel > form:nth-child(4) > table > tbody > tr:nth-child(%d) > td.subject> a" % (y)))),dataNo)

    print("-- 쭉빵 끝 --")
    conn.close()
    driver.close()


