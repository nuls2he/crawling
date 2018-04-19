import inv
import bbang
import naver
import key
import schedule
import time

invenCount = 1
bbangCount = 8
naverCount = 12

#invenTime = 24 / invenCount
invenTime = 17
bbangTime = 24 / bbangCount
naverTime = 24 / naverCount

# -------------사용 소스-------------------
for x in range(0, invenCount):
    schedule.every().day.at("{0}:05".format(int(invenTime))).do(inv.main)

for x in range(0, bbangCount):
    schedule.every().day.at("{0}:0".format(int(bbangTime * x))).do(bbang.main)

for x in range(0, naverCount):
    schedule.every().day.at("{0}:0".format(int(naverTime * x))).do(naver.main)

schedule.every().day.at("11:30").do(key.main)
schedule.every().day.at("14:30").do(key.main)
schedule.every().day.at("17:30").do(key.main)
schedule.every().day.at("13:11").do(key.main)

while 1:
    schedule.run_pending()
    time.sleep(1)