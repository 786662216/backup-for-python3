import re
import requests
import random
import csv
import datetime
import time

def GetInfo():
    url = 'http://cve.scap.org.cn/'
    headers = {
        'Host': 'cve.scap.org.cn',
        'Connection': 'keep-alive',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Referer': 'http://cve.scap.org.cn/',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9',
        # 'Cookie': __jsluid + __jsl_clearance
    }
    cont = requests.get(url,headers=headers).content # 得到网页内容
    cont=str(cont)
    # print(cont)

    # 1、获得CVEid
    ree = 'http://cve.scap.org.cn/CVE-\d{4}-\d{4}.html' # 正则表达式
    pattern = re.compile(ree) # 编译正则表达式，为了匹配能快一些，也可以不用
    path = re.findall(pattern,cont) # 匹配所有符合的字符串
    cve_id=re.findall(re.compile(r'CVE-\d{4}-\d{4}'),str(path))
    # print(cve_id)
    # print('length(cve_id)',len(cve_id))

    # 2、获得时间
    vul_time=re.findall(r'<span class="cve_list_date">(.*?)</span>',cont)
    # print(vul_time)
    # print('length(vul_time)',len(vul_time))

    # get desc
    title=re.findall(r' class="cve_list_summary"><span class="tip_plain" title="(.*?)"><span class="tip_text" title="',cont)

    # get desc from desc
    desc=['' for i in title]

    # get level
    level_enum='高中低'
    level=[level_enum[random.randint(0,2)] for i in cve_id]
    # print(level)

    return cve_id,vul_time,level,title,desc


def main():
    cve_id,vul_time,level,title,desc=GetInfo()

    w=[]
    for i in range(len(cve_id)):
        w.append((cve_id[i],vul_time[i],level[i],title[i],desc[i]))
    # print(w)

    with open('CVE.csv', 'r') as f:
        f_csv=csv.reader(f)
        headers=next(f_csv)
        for row in f_csv:
            if row == []:
                continue
            else:
                if row[0] not in cve_id:
                    w.append(row)
                    print(row)

    csv_header=[('CVE ID','Time','Level','Title','Description')]
    with open('CVE.csv', 'w') as f:
        f_csv = csv.writer(f)
        f_csv.writerows(csv_header)
        f_csv.writerows(w)


if __name__ == '__main__':
    while(True):
        time.sleep(60)
        now = datetime.datetime.now()
        if (now.hour == 16) :
            main()
