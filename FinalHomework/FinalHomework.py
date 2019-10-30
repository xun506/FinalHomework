# coding:utf-8
#FinalHomework.py - By: Shengjie Zhu - 周一 10月 28 2019

import requests
import re
import jieba
from bs4 import BeautifulSoup
import os
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from matplotlib import pyplot as plt

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

            #subwriter = subsoup.find('td')        #找到发布人
            #print(subwriter)

            if (subdata.find('style') != None ):
                [s.extract() for s in subdata("style")]
            mytext=subdata.get_text()
            txtname=mydate[i].string + mydata[i].string
            text_create(txtname,mytext.replace(u'\xa0',u''))          #生成对应txt文件

def stop_words(texts):
    words_list = []
    word_generator = jieba.cut(texts, cut_all=False)  # 返回的是一个迭代器
    with open('C:/Users/ShengjieZhu/Desktop/cloud/stopwords.txt') as f:
        unicode_text = f.read()
        f.close()  # stopwords格式'一词一行'
    for word in word_generator:
        if word.strip() not in unicode_text:
            words_list.append(word)
    return ' '.join(words_list)  # 空格

def txt_add():
    meragefiledir = './get'
    filenames=os.listdir(meragefiledir)  #获取当前文件夹中的文件名称列表  
    file=open('result.txt','w')      #打开当前目录下的result.txt文件，如果没有则创建
    for filename in filenames:
        filepath=meragefiledir+'\\'
        filepath=filepath+filename
        for line in open(filepath):      #遍历单个文件，读取行数  
            file.writelines(line)  
        file.write('\n')  
    file.close()  



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
    txt_add()
    back_color = plt.imread('background.jpg')  # 解析该图片
    wc = WordCloud(background_color='white',  # 背景颜色
                   max_words=1000,  # 最大词数
                   mask=back_color,  # 以该参数值作图绘制词云，这个参数不为空时，width和height会被忽略
                   max_font_size=100,  # 显示字体的最大值
                   stopwords=STOPWORDS.add('苟利国'),  # 使用内置的屏蔽词
                   font_path="C:/Windows/Fonts/STFANGSO.ttf",  # 解决显示口字型乱码问题，可进入C:/Windows/Fonts/目录更换字体
                   random_state=42,  # 为每个词返回一个PIL颜色
                   )
    text = open('./result.txt').read()
    text = stop_words(text)
    jieba.load_userdict('NoCut.txt')
    wc.generate(text)
    image_colors = ImageColorGenerator(back_color)# 基于彩色图像生成相应彩色
    plt.imshow(wc)    # 显示图片
    plt.axis('off')    # 关闭坐标轴
    plt.figure()    # 绘制词云
    plt.imshow(wc.recolor(color_func=image_colors))
    plt.axis('on')
    wc.to_file('WordCloud_out.png')    # 保存图片


main()



