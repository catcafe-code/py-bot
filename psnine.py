import urllib.request
from lxml import etree
import datetime

url = "https://www.psnine.com/psngame/12518?psnid=zws945&ob=trophyid&psngamelang=zh-Hans"


def format_date(date):
    return '2023-'+date[0].strip() + ' ' + date[1].strip()


def cal_date_range(now_time, last_time):
    res = ''
    delta = now_time - last_time
    if delta.days > 0:
        res += str(delta.days) + '天'
    if delta.seconds > 3600:
        res += (str(int(delta.seconds / 3600)) + '小时')
    if (delta.seconds % 3600) / 60 > 0:
        res += (str(int((delta.seconds % 3600) / 60)) + '分钟')
    return res


def parse(content):
    document = etree.HTML(content)
    trophy_list = document.xpath("//table[@class='list']/tr[@class='trophy']")
    data = []
    for trophy in trophy_list:
        img = trophy.xpath("td[1]/a/img/@src")
        name = trophy.xpath("td[2]/p/a/text()")[0]
        tip = trophy.xpath("td[2]//em[@class='text-gray']/text()")[0]
        time = format_date(trophy.xpath("td[3]/em/text()"))
        type = trophy.xpath("td[4]/em/text()")[0]
        data.append({'name': name, 'tip': tip, 'time': time, 'type': type.strip()})
    data.sort(key=lambda it: it['time'])
    print("顺序\t奖杯名称\t提示\t完成难度\t完成时间\t时间间隔\n")
    last_time = datetime.datetime.strptime(data[0]['time'], "%Y-%m-%d %H:%M")
    for idx, it in enumerate(data):
        now_time = datetime.datetime.strptime(it['time'], "%Y-%m-%d %H:%M")
        print('{}\t{}\t{}\t{}\t{}\t{}\n'.format(idx + 1, it['name'], it['tip'], it['type'], it['time'], cal_date_range(now_time, last_time)))
        last_time = now_time


try:
    html = urllib.request.urlopen(url)
    content = html.read()
    parse(content)
except urllib.error.HTTPError as e:
    if e.code == 404:
        print(404)   # 404
