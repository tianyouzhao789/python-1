import json
import re
import requests
import datetime
from bs4 import BeautifulSoup
import os

# 获取当天的日期,并进行格式化,用于文件命名，格式为20230201
today = datetime.date.today().strftime('%Y%m%d')


def crawl_wiki_data():
    """
    爬取百度百科中《青春有你2》中参赛选手信息，返回html
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0'
    }
    url = 'https://baike.baidu.com/item/%E9%9D%92%E6%98%A5%E6%9C%89%E4%BD%A0%E7%AC%AC%E4%BA%8C%E5%AD%A3'

    try:
        response = requests.get(url, headers=headers)
        print(response.status_code)

        # 将一段文档传入BeautifulSoup的构造方法,就能得到一个文档的对象, 可以传入一段字符串
        soup = BeautifulSoup(response.text, 'lxml')

        #返回的是class为table-view log-set-param的<table>所有标签
        tables = soup.find_all('table', {'class': 'tableBox_kVEMN'})


        # table = soup.find_all('table', {'class': 'tableBox_kVEMN'})
        # print(table)
        # return table


        # crawl_table_title = "参赛选手"
        #
        # for table in tables:
        #     # 对当前节点前面的标签和字符串进行查找
        #     table_titles = table.find_previous('div').find_all('h3')
        #     for title in table_titles:
        #         if (crawl_table_title in title):
        #             return table
    except Exception as e:
        print(e)


def parse_wiki_data(table_html):
    '''
    从百度百科返回的html中解析得到选手信息，以当前日期作为文件名，存JSON文件,保存到work目录下
    '''
    bs = BeautifulSoup(str(table_html), 'lxml')
    all_trs = bs.find_all('tr')

    error_list = ['\'', '\"']

    stars = []

    for tr in all_trs[1:]:
        all_tds = tr.find_all('td')

        star = {}

        # 姓名
        star["name"] = all_tds[0].text
        # 个人百度百科链接
        star["link"] = 'https://baike.baidu.com' + all_tds[0].find('a').get('href')
        # 籍贯
        star["zone"] = all_tds[1].text
        # 星座
        star["constellation"] = all_tds[2].text
        # 身高
        star["height"] = all_tds[3].text
        # 体重
        star["weight"] = all_tds[4].text

        # 花语,去除掉花语中的单引号或双引号
        flower_word = all_tds[5].text
        for c in flower_word:
            if c in error_list:
                flower_word = flower_word.replace(c, '')
        star["flower_word"] = flower_word

        # 公司
        if not all_tds[6].find('a') is None:
            star["company"] = all_tds[6].find('a').text
        else:
            star["company"] = all_tds[6].text

        stars.append(star)

    json_data = json.loads(str(stars).replace("\'", "\""))
    with open('D:/mycode/python-1/' + today + '.json', 'w', encoding='UTF-8') as f:
        json.dump(json_data, f, ensure_ascii=False)


# def crawl_pic_urls():
#     '''
#     爬取每个选手的百度百科图片，并保存
#     '''
#     with open('python-1/' + today + '.json', 'r', encoding='UTF-8') as file:
#         json_array = json.loads(file.read())
#
#     headers = {
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36'
#     }
#
#     for star in json_array:
#         name = star['name']
#         link = star['link']
#
#         # ！！！请在以下完成对每个选手图片的爬取，将所有图片url存储在一个列表pic_urls中！！！
#         pic_urls = []
#
#         # ！！！根据图片链接列表pic_urls, 下载所有图片，保存在以name命名的文件夹中！！！
#         down_pic(name, pic_urls)

parse_wiki_data(crawl_wiki_data())