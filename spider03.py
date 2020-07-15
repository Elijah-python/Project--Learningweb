# -*- coding: <utf-8> -*-
import io
import random
import re
import sys
import time

import pymysql
import requests
from fake_useragent import UserAgent
from lxml import etree


class CSDNSpider(object):
    def __init__(self):

        self.url ='https://so.csdn.net/so/search/s.do?q={}&t=blog&p='
        self.headers = {'User-Agent':UserAgent().random}
        self.headers01 = {'User-Agent':'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'}

        self.db = pymysql.connect('localhost','root','123456','learningweb_db',charset='utf8')
        self.cursor = self.db.cursor()

    def get_html(self,url):
        # html = requests.get(url=url,headers=self.headers).content.decode('utf-8','ignore')
        html = requests.get(url=url,headers=self.headers01).text.encode(encoding='utf-8')
        return html

    # def re_func(self,re_bds,html):
    #     res = re.compile(re_bds,re.S)
    #     r_list = res.findall(html)
    #     return r_list
    def xpath_func(self,xpath_bds,html):
        res = etree.HTML(html)
        r_list = res.xpath(xpath_bds)
        return r_list

    def parse_page(self,url):
        html = self.get_html(url)
        xpath_bds_url = r"//div/div/div/dl/dt/div[@class='limit_width']/a[1]/@href"
        xpath_bds_title = r"//div/div/div/dl/dt/div[@class='limit_width']/a[1]/text()"
        xpath_bds_detail = r"//div/div/div/dl/dd[@class='search-detail']/text()"

        r_list01 = self.xpath_func(xpath_bds_url,html)
        r_list02 = self.xpath_func(xpath_bds_title,html)
        r_list03 = self.xpath_func(xpath_bds_detail,html)
        r_list = list(zip(r_list01,r_list02,r_list03))
        print(r_list01)
        print(len(r_list01))
        print(r_list02)
        print(len(r_list02))
        print(r_list03)
        print(len(r_list03))
        print(r_list)
        print(len(r_list))
        return r_list
    def write_into_mysql(self,l):

        ins= 'insert into redis_blog values(%s,%s,%s)'
        self.cursor.executemany(ins,l)
        self.db.commit()
        self.cursor.close()
        self.db.close()
    def main(self):
        ll = []
        q = input('请输入要搜索的关键词:')
        url = self.url.format(q)
        xpath_bds_page = r"//div/div/div/div/span/a[6]/text()"
        total_page = self.xpath_func(xpath_bds_page,self.get_html(url))[0]
        while True:
            print('关键词：{}------总页数{}'.format(q,total_page))
            p = int(input('请输入要爬取的页数，进行单页爬取(按q退出):'))
            if p == 'q':
                break
            else:
                ll.append(p)
                url = url + '{}'.format(p)
                l = self.parse_page(url)
                print('第{}页已经爬取完毕！'.format(p))
                self.write_into_mysql(l)
                print('第{}页，存入MySQL数据库成功！'.format(p))
                time.sleep(random.uniform(2,4))
        print("关键词：{}------爬取页数：{}-------爬虫程序执行完毕！".format(q,' '.join(ll)))

if __name__ == '__main__':
    spider = CSDNSpider()
    spider.main()


