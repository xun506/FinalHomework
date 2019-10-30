# coding:utf-8
#FinalHomework.py - By: Shengjie Zhu - 周一 10月 28 2019

import requests
from bs4 import BeautifulSoup
import bs4
import wordcloud
import re

Tag = 1

def getHTMLText(url):
    try:
        r = requests.get(url, timeout=10)
        r.raise_for_status()
        r.encoding = r.apparent_encoding
        #print('getHTMLText Successful!\n')
        return r.text
    except:
        print('getHTMLText Error!\n')
        return ""

def text_create(name, msg):
    desktop_path = "./get/"  # 新创建的txt文件的存放路径
    full_path = desktop_path + name + '.txt'  # 也可以创建一个.doc的word文档
    file = open(full_path, 'w')
    file.write(msg)
    file.close()


def fillUnivList(ulist, html):
    soup = BeautifulSoup(html, "html.parser")
    mydata=soup.find_all('a',class_="font06") #找到所有的标题
    mydate=soup.find_all('td',class_="riqi")  #找到所有的日期
    global Tag
    for i in range(len(mydata)):
        if mydate[i].string == '(2019-08-30)':
            Tag = 0
        if Tag:
            mylink=mydata[i].get('href')
            sublink='http://www.ciomp.ac.cn/xwdt/zhxw/' + mylink   #子链接地址
            subText = getHTMLText(sublink)                         #访问之链接
            subsoup = BeautifulSoup(subText, "html.parser")        #解析子链接
            subdata=subsoup.find('div',class_="TRS_Editor")
            #subwriter = subsoup.find_all('td',class_="align")        #找到发布人
            if (subdata.find('style')!= None ):
                [s.extract() for s in subdata("style")]
            mytext=subdata.get_text()
            txtname=mydate[i].string + mydata[i].string
            text_create(txtname,mytext.replace(u'\xa0',u''))          #生成对应txt文件


def main():
    uinfo = []
    url_first = 'http://www.ciomp.ac.cn/xwdt/zhxw/index.html'
    html = getHTMLText(url_first)
    fillUnivList(uinfo, html)
    url = 'http://www.ciomp.ac.cn/xwdt/zhxw/index_{list}.html'
    for n in range(1,3):
        url_take = url.format(list=n)
        html = getHTMLText(url_take)
        fillUnivList(uinfo, html)
main()



