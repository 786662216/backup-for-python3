import datetime
import time

schedtime = datetime.datetime(2018, 4, 6, 12, 22, 00)  # 要执行的时间
Frequency = datetime.timedelta(minutes = 1)  # 频率，这个函数的参数有days,months,seconds,years,minutes都是字面意思,也可以为负

while(True):

    time.sleep(40)
    now = datetime.datetime.now()  # 返回值里面有微秒
    print(now)
    if now.date() == schedtime.date():
        if (now.hour == schedtime.hour) and (now.minute == schedtime.minute):
            schedtime = schedtime + Frequency
            print('caonima')
        else:
            continue
    else:
        continue
