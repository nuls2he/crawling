from selenium import webdriver
import pymysql.cursors
import math
import re

path = "C:/Users/loveh/Desktop/chromedriver_win32/chromedriver.exe"

number = 0

def calculationPage(firstNum):

    pageNo = (firstNum - number) / 50
    print(pageNo)
    return math.ceil(pageNo) + 1 if (pageNo % 50) > 0 else int(pageNo + 1)

def selectDB(conn, cursor):

    global number

    try:
        sql = 'select max(no) as no from test_original where siteno = 2'
        cursor.execute(sql)
        number = cursor.fetchone()['no']

        # 디비 처음 생성치 처리
        if number is None:
            number = 865837

    except Exception as e:
        print(e)
        print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ에러ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
        # print(result[1])
    else:
        conn.commit()

    return

def insertDB(conn, cursor, data, dataNo):

    try:
        if data != " ":
            sql = 'insert into test_original(siteno, originaldata, state, no) values (%s, %s, %s, %s)'
            cursor.execute(sql, (2, data, 'N', dataNo))
    except Exception as e:
        print("error : " + e)
        print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ에러ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
        # print(result[1])
    else:
        conn.commit()

    return

def main():

    conn = pymysql.connect(
        host='127.0.0.1',
        user='day',
        password='word',
        db='OnedayOneword',
        charset='utf8mb4'
    )
    cursor = conn.cursor(pymysql.cursors.DictCursor)

    driver = webdriver.Chrome(path)
    driver.get("http://www.inven.co.kr/board/powerbbs.php?come_idx=2097&query=list&my=&category=&category2=&sort=PID&orderby=&name=&subject=&content=&keyword=&sterm=&eq=&iskin=webzine&mskin=&p=1")

    selectDB(conn, cursor)
    print("넘버 : " + str(number))
    scrapPageNo = calculationPage(int(driver.find_element_by_css_selector(
        "#powerbbsBody > table > tbody > tr > td > div > table > tbody > tr > td > table > tbody > tr:nth-child(3) > td > form > table > tbody > tr:nth-child(6) > td:nth-child(1) > div > a").get_attribute("data-uid")))
    print("페이지 번호 ", scrapPageNo)

    #글 배열
    arr = []
    noArr = []
    testArr = []
    print("-- 인벤 시작 --")
    for x in range(1, scrapPageNo):
        testArr.clear()
        arr.clear()
        noArr.clear()
        testArr = driver.find_elements_by_css_selector("#powerbbsBody > table > tbody > tr > td > div > table > tbody > tr > td > table > tbody > tr:nth-child(3) > td > form > table > tbody > tr")
        print("----------------%d 페이지----------------" % (x))
        for y in range(0, len(testArr)):
            if testArr[y].get_attribute('class') == "ls oh nc" or testArr[y].get_attribute('class') == "bgc":
                print("공지")
                continue

            dataNo = int(driver.find_element_by_css_selector("#powerbbsBody > table > tbody > tr > td > div > table > tbody > tr > td > table > tbody > tr:nth-child(3) > td > form > table > tbody > tr:nth-child(%d) > td.bbsSubject > span" % (y + 1)).get_attribute("data-cmt-uid"))

            if dataNo < number:
                print("-- 인벤 끝 --")
                conn.close()
                driver.close()
                return

            insertDB(conn, cursor, re.sub("[^가-힝0-9a-zA-Z\\s]", "", driver.execute_script("return arguments[0].innerText;", driver.find_element_by_css_selector("#powerbbsBody > table > tbody > tr > td > div > table > tbody > tr > td > table > tbody > tr:nth-child(3) > td > form > table > tbody > tr:nth-child(%d) > td.bbsSubject > a" % (y)))[5:]), dataNo)

        if x != (scrapPageNo - 1):
            driver.get("http://www.inven.co.kr/board/powerbbs.php?come_idx=2097&query=list&my=&category=&category2=&sort=PID&orderby=&name=&subject=&content=&keyword=&sterm=&eq=&iskin=webzine&mskin=&p=%d" % (x + 1))

    print("-- 인벤 끝 --")
    conn.close()
    driver.close()

