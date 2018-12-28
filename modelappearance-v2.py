# -*- coding: UTF-8 -*-

import requests
import os
import sys
import re
import time
import csv
from bs4 import  BeautifulSoup
import  lxml

reload(sys)
sys.setdefaultencoding( "utf-8" )

#得到一个网址的html信息
def get_page_html(detailurl):
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;",
               "Accept-Encoding": "gzip",
               "Accept-Language": "zh-CN,zh;q=0.8",
               "Referer": "http://www.example.com/",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"}
    #user_agent = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
    #headers = {'User_agent': user_agent}
    r = requests.get(detailurl, headers=headers)
    #r = requests.get(detailurl)
    r.encoding = 'UTF-8'
    result = r.text
    return result

def get_GBK_page_html(detailurl):
    #user_agent = 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.101 Safari/537.36'
    #headers = {'User_agent': user_agent}
    headers = {"Accept": "text/html,application/xhtml+xml,application/xml;",
               "Accept-Encoding": "gzip",
               "Accept-Language": "zh-CN,zh;q=0.8",
               "Referer": "http://www.example.com/",
               "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"}
    r = requests.get(detailurl, headers=headers)
    r.encoding = 'GBK'
    result = r.text
    return result

#将一个网页信息保存在txt文档里
def write_html_txt(detail_url):
    data = get_GBK_page_html(detail_url)
    file = open('/home/koko/Documents/carspider/save/car_model.txt','w')
    file.write(data)
    file.close()


def write_csv(data):
    with open('huaian.csv', 'w') as csvfile:
        writer = csv.writer(csvfile)
        for row in data:
            writer.writerow(row)

def write_txt(data, filename):
    file = open(filename + '.txt' ,'a')
    file.write(data)
    file.close()

def replace_others(data):
    data = str(data)
    data = data.replace('\r', '').replace('\n', '').replace('\t', '')
    return data

def get_car_img(url, car_name):
    source = get_GBK_page_html(url)
    soup = BeautifulSoup(source, 'lxml')
    car_list = soup.find('div', attrs={'class': 'uibox-con carpic-list03'})
    car_list = car_list.find_all('li')
    for car_link in car_list:
        main = car_link.find('a')
        main_href = main.get('href')
        main_title = main.get('title')
        img = car_link.find('img')
        img = img.get('src')
        img_info = str(main_title) + '\t' + str(main_href) + '\t' + str(img) + '\n'
        write_txt(img_info, str(car_name))

def count_page(url):
    source = get_GBK_page_html(url)
    soup = BeautifulSoup(source, 'lxml')
    pagecont = soup.find('div', attrs={'class': 'page'})
    number = str(pagecont).count('href')
    #number = (len(str(pagecont)) - len(str(pagecont).replace('href', '')))/4
    return number

def get_allpage_car_img(car_id, car_name):
    url = 'https://car.autohome.com.cn/pic/series-t/' + str(car_id) + '-1.html#pvareaid=2042222'
    #print url
    get_car_img(url, car_name)
    number = count_page(url)
    number = int(number) - 3
    for i in range(number):
        page_number = i + 2
        page = 'https://car.autohome.com.cn/pic/series-t/' + str(car_id) +'-1-p' + str(page_number) + '.html#pvareaid=2042222'
        print page
        get_car_img(page, car_name)

def download_car_imglink(filename):
    file = open(filename)
    for line_o in file:
        line = line_o.replace('\n', '')
        line = line.split('\t')
        car_name = line[0]
        car_id = line[1]
        try:
            print 'loding'+str(line_o)
            get_allpage_car_img(car_id, car_name)
        except:
            print 'warning'+ str(line_o)
            write_txt(line_o, 'buglink')
            continue
    file.close()

filename = 'data/car_id.txt'
download_car_imglink(filename)
#car_id = 879
#car_name = 'weizhiV2'
#get_allpage_car_img(car_id, car_name)