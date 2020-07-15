# -*- coding: <utf-8> -*-
import io
import random
import re
import sys
import time
import urllib.parse

import pymysql
import requests
from fake_useragent import UserAgent
from lxml import etree



class CSDNSpider(object):
    def __init__(self):
        self.url = 'http://search.dangdang.com/?key={}&act=input'
        self.headers = {'User-Agent': UserAgent().random}
        self.headers01 = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:74.0) Gecko/20100101 Firefox/74.0'}
        self.db = pymysql.connect('localhost', 'root', '123456', 'learningweb_db', charset='utf8')
        self.cursor = self.db.cursor()

    def get_html(self, url):
        html = requests.get(url=url, headers=self.headers).text
        return html

    def xpath_func(self, xpath_bds, html):
        res = etree.HTML(html)
        r_list = res.xpath(xpath_bds)
        return r_list

    def parse_page(self, url):
        html = self.get_html(url)
        xpath_book_url = r"//div/div/div/div/div/div/div/ul[@id='component_59']/li/a/@href"
        xpath_bds_title = r"//div/div/div/div/div/div/div/ul[@id='component_59']/li/a/@title"
        xpath_img_url = r"//div/div/div/div/div/div/div/ul/li/a/img/@src"
        xpath_img_url01 = r"//div/div/div/div/div/div/div/ul/li/a/img/@data-original"

        r_list01 = self.xpath_func(xpath_book_url, html)
        print(r_list01)
        print(len(r_list01))
        r_list02 = self.xpath_func(xpath_bds_title, html)
        print(r_list02)
        print(len(r_list02))

        r_list03 = [self.xpath_func(xpath_img_url, html)[0]]
        print(r_list03)
        r_list03 = r_list03 + self.xpath_func(xpath_img_url01,html)
        print(r_list03)
        print(len(r_list03))

        r_list = list(zip(r_list01, r_list02, r_list03))
        print(r_list)
        print(len(r_list))
        return r_list

    def write_into_mysql(self, l):
        ins = 'insert into book values(%s,%s,%s)'
        self.cursor.executemany(ins, l)
        self.db.commit()
        self.cursor.close()
        self.db.close()

    def main(self):
        ll = []
        key = input('请输入要搜索的关键词:')
        key = urllib.parse.quote(key,encoding='gbk')
        print(key)
        url = self.url.format(key)
        print(url)
        xpath_bds_page = r"//div/div/div/div/div/div/div/ul/li[9]/a/text()"
        total_page = self.xpath_func(xpath_bds_page, self.get_html(url))
        print(total_page)
        while True:
            print('关键词：{}------总页数{}'.format(key, total_page))
            p = int(input('请输入要爬取的页数，进行单页爬取(按q退出):'))
            if p == 'q':
                break
            else:
                ll.append(p)
                for i in range(p, p + 1):
                    url = url + '&page_index={}'.format(i)
                    l = self.parse_page(url)
                    print('第{}页已经爬取完毕！'.format(i))
                    self.write_into_mysql(l)
                    print('第{}页，存入MySQL数据库成功！'.format(i))
                    time.sleep(random.uniform(2, 4))
        print("关键词：{}------爬取页数：{}-------爬虫程序执行完毕！".format(key, ' '.join(ll)))


if __name__ == '__main__':
    spider = CSDNSpider()
    spider.main()


