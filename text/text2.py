import requests
import execjs
import re

url = 'http://www.cnvd.org.cn/flaw/list.htm'

r = requests
content = r.get(url).text

ss = '\d\d\d'
sss = re.compile(ss)
ap = sss.findall(content)
print(ap)

ss = '\d\d\d\d\d\d\d\d\d'
sss = re.compile(ss)
bp = sss.findall(content)
print(bp)

for i in range(0,5):
    jsl = '__jsl_clearance=' + str(bp[0]) + '.' + str(ap[i]) + '|0|'

    js ='''
    function a(jsl) {
        var cd, dc = jsl;
        cd = Array( + [[( + !+[])] + [([ - ~ - ~~~ ! []] + ~~ {} >> -~ - ~~~ ! [])]]);
        var chips = ['TAGGl', (!{} + [[], -~ {}][~~ ! []]).charAt( - ~ [( - ~ {} << -~ {})]), 'w7ZgszEX', [{} + [[], -~ {}][~~ ! []]][0].charAt(3 - ~~~ ! [] - ~~~ ! [] + 3), '%', [{} + [[], -~ {}][~~ ! []]][0].charAt(([ - ~ - ~~~ ! []] + ~~ {} >> -~ - ~~~ ! [])), 'B', ( + {} + [[], -~ {}][~~ ! []]).charAt(2), '86w', (2 + [] + [[]][( + [])]), 'D', ([][~~ {}] + [] + []).charAt(4), 'vHA', ( - ~ [] / ~~ ! [] + [[], -~ {}][~~ ! []]).charAt(6), '%3D'];
        for (var i = 0; i < chips.length; i++) {
            cd.reverse()[i] = chips[i]
        };
        cd = cd.join('');
        dc += cd;
        return dc;
    };
    '''

    ctx = execjs.compile(js)
    result = ctx.call('a',jsl)

    headers = {
    'Host': 'www.cnvd.org.cn',
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'Upgrade-Insecure-Requests': '1',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.181 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
    'Referer': 'http://www.cnvd.org.cn/',
    'Accept-Encoding': 'gzip, deflate',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': '__jsluid=4649a1c0dcdac5d2e429a3c2b01386b5;' + result +';'
    }
    print(headers['Cookie'])
    content = requests.session().get(url,headers=headers).text
    print(content)