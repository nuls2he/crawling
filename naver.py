from selenium import webdriver
import pymysql.cursors

path = "C:/Users/Bit/Desktop/chromedriver_win32/chromedriver.exe"

number = 0;

def selectDB(conn, cursor):

    count = 0

    try:
        sql = 'select max(rank) as count from test_naver'
        cursor.execute(sql)
        count = cursor.fetchone()['count'];
        print(str(count))
        # print(len(cursor.fetchall()))
        # count = len(cursor.fetchall())
        # print("count : " + str(count))

    except Exception as e:
        print("셀렉트 에러 : ", str(e))
        print('ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ에러ㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡㅡ')
        # print(result[1])
    else:
        conn.commit()

    return count

def insertDB(conn, cursor, data):

    global number

    try:
        # print("selectCount : " + str(selectDB()))
        if selectDB(conn, cursor) < 10:
            print(data)
            sql = 'insert into test_naver(keyword) values (%s)'
            cursor.execute(sql, data)
        else:
            print(data)
            number += 1
            sql = 'update test_naver set keyword = (%s) where rank = (%s)'
            cursor.execute(sql, (data, number))
    except Exception as e:
        print("업데이트 에러 : ", str(e))
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
    driver.get("https://datalab.naver.com/keyword/sectionSearch.naver")

    global number

    print("-- 네이버 시작 --")
    if driver.find_element_by_css_selector('li.list:nth-child(10)').get_attribute('class') != 'list inactive':
        driver.find_element_by_link_text('대학생').click()

        test = driver.find_elements_by_css_selector('li.sub_title > a:nth-child(1) > span:nth-child(2)')

        for i in range(0, 10):
            insertDB(conn, cursor, driver.execute_script("return arguments[0].innerText;", test[i]))

    number = 0

    print("-- 네이버 끝 --")
    conn.close()
    driver.close()
