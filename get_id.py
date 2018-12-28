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
        car_id = str(line[0]) + '\t' + str(line[1]) + '\n'
        write_txt(car_id, 'car_id')
    file.close()

if __name__ == '__main__':
    # 得到了cars.txt之后我们需要得到每一辆车对应在汽车之家中的id
    get_id(filename = raw_input('Please enter the filename：'))