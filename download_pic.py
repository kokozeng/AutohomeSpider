# -*- coding: UTF-8 -*-

import requests
import os
import sys
import re
import time
import csv
from bs4 import  BeautifulSoup
import lxml

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

def write_txt(data, filename):
    file = open(filename + '.txt' ,'a')
    file.write(data)
    file.close()

def mkdir(path):
    path = path.strip()
    path = path.rstrip("\\")
    isExists = os.path.exists(path)
    if not isExists:
        os.makedirs(path)
        print path + ' 创建成功'
        return True
    else:
        print path + ' 目录已存在'
        return False

def mkdir_path():
    t = time.localtime(time.time())
    # 反斜杠连接多行
    filename = str(t.__getattribute__("tm_year")) + "_" + \
               str(t.__getattribute__("tm_mon")) + "_" + \
               str(t.__getattribute__("tm_mday"))
    mkdir(filename)
    return filename

def download(img_src, img_name, number, name):
    kw = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64)'}
    try:
        pic = requests.get(img_src, timeout=10, stream=True, headers=kw)
        mkdir(name)
        string = name + '/' + str(img_name) + '-' + str(number) + '.jpg'
        with open(string, 'wb') as wr:
            for chunk in pic.iter_content(chunk_size=1024):
                if chunk:
                    wr.write(chunk)
                    wr.flush()
    except:
        line = str(name) + '\t' + str(img_name) + '\t' + str(img_src) + '\t' + str(number) + '\n'
        write_txt(line, 'missingpic')
        print u'【错误】当前图片无法下载'

def get_car_img(url):
    source = get_GBK_page_html(url)
    soup = BeautifulSoup(source, 'lxml')
    car_img_src = soup.find('div', attrs={'class': 'pic'})
    car_img_src = car_img_src.find('img')
    car_img_src = car_img_src.get('src')
    return car_img_src

def download_img(filename, name):
    file = open(filename)
    number = 0
    for line in file:
        line = line.replace('\n', '')
        line = line.split('\t')
        img_url = 'https://car.autohome.com.cn' + str(line[1])
        try:
            print 'loding'+str(img_url)
            img_src = get_car_img(img_url)
        except:
            print 'warning'+ str(img_url)
            write_txt(line, 'buglink')
            continue
        #img_src = get_car_img(img_url)
        img_src = 'https:' + str(img_src)
        #print img_src
        img_name = line[0]
        number = number + 1
        try:
            download(img_src, img_name, number, name)
        except:
            continue
    file.close()

def get_file(file_dir):
    path = []
    name = []
    #提取文件夹里的表格地址和表格名
    for root, dirs, files in os.walk(file_dir):
        for file in files:
            if os.path.splitext(file)[1] == '.txt':
               path.append(os.path.join(root, file))
               name.append(os.path.splitext(file)[0])
    #这里的path是表格地址 name是以后的文件夹的路径
    for i in range(len(path)):
        print path[i], name[i]
        download_img(str(path[i]), str(name[i]))


get_file(raw_input('Please enter the filename：'))
#download_img(filename = raw_input('Please enter the filename：'))