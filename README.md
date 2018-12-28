# 汽车之家爬虫

## Introduction

本程序的主要功能是爬取汽车之家上的共有多少种车型，以及爬取具体车型在网页上显示的缩略图或者是该车型的全图。

## Requirements

主要是用requests和beautiful soup手写的爬虫，用wget下载图片。
使用的是python2.7。
## Use Method

### get_model.py/get_make_model.py

直接运行该程序，会得到一个cars.txt。

使用get_make_model.py，得到的数据是。左边的名称是一级品牌-二级品牌-车型，右边的名称是对应在汽车之家上的一个id。
使用get_model.py，得到的数据是。左边的名称是车型，右边的名称是对应在汽车之家上的一个id。

![](https://i.loli.net/2018/11/22/5bf66de878900.png)

### get_id.py

通过上一个文件爬取到的cars.txt，再对cars.txt进行处理，提取关键id。关键id用于之后的爬取。

![](https://i.loli.net/2018/11/22/5bf66f54a1a87.png)


### modelappearance-v1.py / modelappearance-v2.py

通过上一个文件得到的car_id.txt，我们通过汽车之家官网爬取每一个车型外观的缩略图的img_src，和车型全图的url，url还要再进去处理下提取img_src才能进行图片下载。

v1和v2主要是因为汽车之家网站有一个div的class的命名不同，导致爬取的差异。所以需要使用两个版本代码进行爬取。

爬取的效果如下：

car_name | img_url | thumbnail_src

![](https://i.loli.net/2018/11/22/5bf6712c31f7e.png)

![](https://i.loli.net/2018/11/22/5bf6718fa85ff.png)

### download_thumbnail.py

该代码使用上一级生成的针对每个车型的txt中的thumbnail_src，进行下载。
每个缩略图的尺寸是240*180。

效果如下：

![](https://i.loli.net/2018/11/22/5bf672785d0cb.png)

![](https://i.loli.net/2018/11/22/5bf672d8eedd2.png)

### download_pic.py

该代码使用上一级生成的针对每个车型的txt中的img_url，重新抓取img_src，然后进行下载。
每个缩略图的尺寸是1024*768。

![](https://i.loli.net/2018/11/22/5bf673a84879c.png)
