'''
爬虫，把最新的CNVD漏洞信息爬下来，存到CSV文件中。内容暂定为
标题（
时间
编号
危害级别
漏洞描述
2018年4月2日19:49:06
'''

import datetime
import re
import requests
import time
import random
import csv
from selenium import webdriver
from pyvirtualdisplay import Display

#要怕的链接
url = 'http://www.cnvd.org.cn/flaw/list.htm'

#模拟浏览器运行，取出cookies
# display = Display(visible=0, size=(800, 600))
# display.start()
chrome = webdriver.Chrome()
chrome.get(url)
time.sleep(5)
__jsluid = '__jsluid=' + chrome.get_cookie('__jsluid')['value'] + ';'
__jsl_clearance = '__jsl_clearance=' + chrome.get_cookie('__jsl_clearance')['value'] + ';'
chrome.quit()
# display.stop()

#请求头，注意要和上面模拟浏览器的头差不多，尤其是User-Agent
headers = {
'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
'Accept-Encoding': 'gzip, deflate',
'Accept-Language': 'en-US,en;q=0.9',
'Cache-Control': 'max-age=0',
'Connection': 'keep-alive',
'Host': 'www.cnvd.org.cn',
'Referer': 'http://www.cnvd.org.cn/',
'Upgrade-Insecure-Requests': '1',
'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
'Cookie': __jsluid + __jsl_clearance
}

host = 'http://www.cnvd.org.cn'
title = []

def getURL():#获得当前页面所有的漏洞详情页面

    r = requests.session()#设置会话
    content = r.get(url,headers=headers).text#得到网页内容
    #print(content)

    #开始使用正则匹配
    #1、获得链接
    ree = '/flaw/show/CNVD-\d\d\d\d-\d\d\d\d\d'#正则表达式
    pattern = re.compile(ree)#编译正则表达式，为了匹配能快一些，也可以不用
    path = re.findall(pattern,str(content))#匹配所有符合的字符串

    #2、获得标题
    ree = 'title=".+">'
    pattern2 = re.compile(ree)
    t = re.findall(pattern2, str(content))[1:]#去掉第一个

    return path,t

def accessURL(URL):#访问获得的漏洞详情页面,并取出需要的信息

    r = requests.session()  # 设置会话
    content = r.get(host + URL, headers=headers).text  # 得到网页内容

    #3、获得日期
    ree = r'\d\d\d\d-\d\d-\d\d'  # 正则表达式
    pattern = re.compile(ree)  # 编译正则表达式，为了匹配能快一些，也可以不用,直接匹配
    time = re.findall(pattern, str(content))  # 匹配所有符合的字符串,由于网页里多次出现时间，所以只要其中一个
    if (len(time) == 0):
        return
    else:
        time = re.findall(pattern, str(content))[0]

    CNVDid = URL[11:]

    # 开始使用正则匹配
    #4、获得漏洞等级
    ree = '\s[高中低]\s'
    pattern = re.compile(ree)
    bb = re.findall(pattern, content)
    level = str(bb[0]).strip()

    #5、获得详细信息
    s = '漏洞描述</td>.+[.\n\t]+.+[.\n\t]+[\n\t]+.+[.\n\t]+.+[.\n\t]+.+[.\n\t]+.+[.\n\t]+.+[.\n\t]+.+[.\n\t]+.+'
    pattern = re.compile(s)
    res = re.findall(pattern, str(content))
    result = res[0]
    result = ''.join(result.split())  # 去掉不可见字符
    result = result.replace('<br/>', '')
    result = result.replace('漏洞描述', '')
    result = result.replace('</td>', '')
    result = result.replace('<td>', '')

    return CNVDid,time,level,result

def main():
    a, title = getURL()
    count = 0  # 计数
    result = []
    tem = []

    reURL = []

    #取出之前的URL，看是否已经爬过了
    with open('URL.csv', 'r') as f:
        re = f.read()

    re = re.split('\n')

    for i in re:
        i = i.replace(',', '')
        reURL.append(i)

    for i in a[:-10]:  # 访问每个获得的链接
        if i in reURL:
            continue
        else:
            sleep = random.randint(5, 10)  # 反爬，每次访问随机间隔5-10s
            count = count + 1
            print(count)
            print(i)
            time.sleep(sleep)
            tep = accessURL(i)
            tem.append(tep)

    # 合并结果
    for i in tem:
        if i == None:
            tem.remove(i)
        else:
            i = list(i)
            result.append(i)
    for i in result:
        i.append(title[result.index(i)][6:-2].strip('"'))

    # 放到文件中
    # headers = ['编号', '时间', '危害级别', '漏洞描述', '标题',]

    with open('CNVD.csv', 'a') as f:
        f_csv = csv.writer(f)
        # f_csv.writerow(headers)
        f_csv.writerows(result)

    con = []

    #URL去重，新的URL存进去，以备之后使用
    for i in a[:-10]:
        if i in reURL:
            continue
        else:
            con.append(i)

    #把数据写入文件
    with open('URL.csv', 'a') as f:
        f_csv = csv.writer(f)
        # f_csv.writerow(headers)
        f_csv.writerows(con)

if __name__ == '__main__':

    #放到服务器上跑
    while (True):
        now = datetime.datetime.now()  # 返回值里面有微秒
        time.sleep(1800)
        #一天运行一次
        if (now.hour == 23):
            main()
            print(str(now) + '到时间了！')
        else:
            print(str(now) + '没到时间')
            continue



