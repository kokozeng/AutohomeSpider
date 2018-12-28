# -*- coding: UTF-8 -*-

import requests
import os
import sys
import re
import time
import csv

def write_txt(data, filename):
    file = open(filename + '.txt' ,'a')
    file.write(data)
    file.close()

def get_id(filename):
    file = open(filename)
    for line in file:
        line = line.replace('\n', '')
        line = line.split('\t')
        line[1] = line[1].replace('/series/','')
        line[1] = line[1].replace('.html#pvareaid=103448','')
        car_id = str(line[0]) + '，' + str(line[1]) + '\n'
        write_txt(car_id, 'car_id')
    file.close()

def mkdir(path):
    # 引入模块
    import os

    # 去除首位空格
    path = path.strip()
    # 去除尾部 \ 符号
    path = path.rstrip("\\")

    # 判断路径是否存在
    # 存在     True
    # 不存在   False
    isExists = os.path.exists(path)

    # 判断结果
    if not isExists:
        # 如果不存在则创建目录
        # 创建目录操作函数
        os.makedirs(path)

        print path + ' 创建成功'
        return True
    else:
        # 如果目录存在则不创建，并提示目录已存在
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


def download_img(filename, name):
    file = open(filename)
    number = 0
    for line in file:
        line = line.replace('\n', '')
        line = line.split('\t')
        img_src = 'https:' + str(line[2])
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


# 得到了cars.txt之后我们需要得到每一辆车对应在汽车之家中的id
#get_id(filename = raw_input('Please enter the filename：'))
get_file('/home/dc2-user/Document/imglink-v2')
#download_img(filename = raw_input('Please enter the filename：'))