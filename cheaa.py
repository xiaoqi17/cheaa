# -*- coding: utf-8 -*-

from multiprocessing import Pool
import pymongo
from requests import ConnectionError
import requests
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding( "utf-8" )

client = pymongo.MongoClient('localhost', 27017)
ceshi = client['cheaa']
item_info = ceshi['cheaa']


def index_html(headers,i):
    try:
        url = 'http://digitalhome.cheaa.com/index_{}.shtml'.format(i)
        response = requests.get(url,headers=headers)
        soup = BeautifulSoup(response.text,'lxml')
        urls = soup.select(' div.clear.news-mid > div > a')
        for url in urls:
            url = url.get('href')
            item_info.insert_one({'url':url})
            yield url
    except ConnectionError:
        pass

def title_html(url,headers):
    try:
        if item_info.find_one({'url': url}):
            print '%s爬过'%url
        else:
            response = requests.get(url, headers=headers)
            soup = BeautifulSoup(response.text, 'lxml')
            titles = soup.find_all('h1')
            for title in titles:
                title = title.get_text()
                return title
    except ConnectionError:
        print('Error occurred')
        return None

def text_html(url,headers):
    try:
        response = requests.get(url, headers=headers)
        soup = BeautifulSoup(response.text, 'lxml')
        texts = soup.select('#ctrlfscont')
        for text in texts:
            text = text.get_text()
            print url
            return text

    except:
        print('Error occurred')
        return None

def write_to_file(text,title):
    try:
        with open(title + ".doc", 'w' ) as f:
            f.write(str(text))
            f.close()
    except IOError:
        pass


def main(i):
        headers={
            'User - Agent': 'Mozilla / 5.0(Windows NT 6.1;WOW64) AppleWebKit / 537.36(KHTML, likeGecko) Chrome / 59.0.3071.86Safari / 537.36'
        }
        for url in index_html(headers,i):
            data = text_html(url,headers)
            title = title_html(url,headers)
            write_to_file(data, title)

if __name__ == '__main__':
    pool = Pool()
    groups = ([i for i in range(1, 21)])
    pool.map(main, groups)
    pool.close()
    pool.join()
    # main()