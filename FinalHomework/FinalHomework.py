# coding:utf-8
#FinalHomework.py - By: Shengjie Zhu - 周一 10月 28 2019

import requests
import re
import jieba
from bs4 import BeautifulSoup
import os
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
from matplotlib import pyplot as plt
import sys

last_page = 1
max_steps=27
page_number=0

class ShowProcess():#显示处理进度的类
    i = 0 # 当前的处理进度
    max_steps = 0 # 总共需要处理的次数
    max_arrow = 80 #进度条的长度
    infoDone = 'done'

    def __init__(self, max_steps, infoDone = 'Done'):
        self.max_steps = max_steps
        self.i = 0
        self.infoDone = infoDone
    def show_process(self, i=None):
        if i is not None:
            self.i = i
        else:
            self.i += 1
        num_arrow = int(self.i * self.max_arrow / self.max_steps) #计算显示多少个'>'
        num_line = self.max_arrow - num_arrow #计算显示多少个'-'
        percent = self.i * 100.0 / self.max_steps #计算完成进度，格式为xx.xx%
        process_bar = '第'+ str(page_number) + '页' + '[' + '>' * num_arrow + '-' * num_line + ']'\
                      + '%.2f' % percent + '%' + '\r' #带输出的字符串，'\r'表示不换行回到最左边
        sys.stdout.write(process_bar) #这两句打印字符到终端
        sys.stdout.flush()
        if self.i >= self.max_steps:
            self.close()

    def close(self):
        print('')
        print(self.infoDone)
        self.i = 0

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

def text_create(name, msg):   #文件名不能包含\/：*？"<>|字符
    desktop_path = "./get/"  # 新创建的txt文件的存放路径
    rstr = r"[\/\\\:\*\?\"\<\>\|]"  # '/ \ : * ? " < > |'
    name = re.sub(rstr, "_", name)  # 替换为下划线
    name = name.replace('\n\u3000\u3000',' ')   #解决2018-08-13的标题中有斜杠的问题
    full_path = desktop_path + name + '.txt'  # 创建一个.txt的文档
    file = open(full_path, 'w', encoding='utf-8')
    file.write(msg)
    file.close()

def writers_txt(name):
    if name != None and name != ' ':
        file=open('writers.txt','a', encoding='utf-8')
        name = name + '\n'
        file.write(name)
        file.close()

def fillUnivList(ulist, html):
    global last_page , max_steps , page_number
    soup = BeautifulSoup(html, "html.parser")
    mydata=soup.find_all('a',class_="font06") #找到所有的标题
    mydate=soup.find_all('td',class_="riqi")  #找到所有的日期
    process_bar = ShowProcess(max_steps, 'OK')
    for i in range(len(mydata)):
        if page_number == 37:
            max_steps = 1
            process_bar = ShowProcess(max_steps, 'OK')
        mylink = mydata[i].get('href')
        if mylink == 'http://www.ccb.cas.cn/xwzx2015/zhxw2015/201902/t20190225_5244377.html':
            sublink = mylink       #该地址直接访问另一个地址，不在研究所服务器
        elif mylink == 'http://www.ccb.ac.cn/xwzx2015/zhxw2015/201808/t20180828_5060142.html':
            sublink = mylink       #该地址直接访问另一个地址，不在研究所服务器
        else:
            sublink = 'http://www.ciomp.ac.cn/xwdt/zhxw/' + mylink   #子链接地址

        subText = getHTMLText(sublink)                         #访问子链接
        process_bar.show_process()                             #显示进度条
        subsoup = BeautifulSoup(subText, "html.parser")        #解析子链接
        subdata=subsoup.find('div',class_="TRS_Editor")        #查找文本的位置

        if subdata is None:
            subdata=subsoup.find('td',class_="zw")         #如果是空，就在另一个位置查找
             
        if re.findall(r'xwzx2015',sublink) or re.findall(r'chengguozhuanhua2',sublink) or re.findall(r'lxyz_zbdt',sublink):
            subwriter.string = ' '
        elif re.findall(r'zonghexinwen',sublink):
            subwriter = subsoup.find('span',style="color:#FF6600;")
        else:
            subwriter = subsoup.find('td',width="22%")        #找到发布人(靠编辑的位置的宽度找到)
        #print(subwriter.string)
        if subwriter.string == None:
            subwriter.string = ' '
        writers_txt(subwriter.string)
        if subdata.find('style'):
            [s.extract() for s in subdata("style")]
        mytext=subdata.get_text()
        txtname=mydate[i].string + subwriter.string + '《' + mydata[i].string + '》'
        #print(txtname)
        text_create(txtname,mytext.replace(u'\xa0',u''))          #生成对应txt文件

def stop_words(texts):
    words_list = []
    word_generator = jieba.cut(texts, cut_all=False)  # 返回的是一个迭代器
    with open('stopwords.txt') as f:
        unicode_text = f.read()
        f.close()  # stopwords格式'一词一行'
    for word in word_generator:
        if word.strip() not in unicode_text:
            words_list.append(word)
    return ' '.join(words_list)  # 空格

def txt_add():
    meragefiledir = './get'
    filenames=os.listdir(meragefiledir)  #获取当前文件夹中的文件名称列表  
    file=open('result.txt','w', encoding='utf-8')      #打开当前目录下的result.txt文件，如果没有则创建
    for filename in filenames:
        filepath=meragefiledir+'\\'
        filepath=filepath+filename
        for line in open(filepath,'r', encoding='UTF-8'):      #遍历单个文件，读取行数  
            file.writelines(line)
        file.write('\n')
    file.close()  

def main():
    global page_number
    uinfo = []
    process_bar = ShowProcess(max_steps, 'OK')
    url_first = 'http://www.ciomp.ac.cn/xwdt/zhxw/index.html'  #首页
    html = getHTMLText(url_first)
    fillUnivList(uinfo, html)
    url = 'http://www.ciomp.ac.cn/xwdt/zhxw/index_{list}.html'
    for page_number in range(1,38):         #从1开始到37页
        url_take = url.format(list = page_number)
        html = getHTMLText(url_take)
        fillUnivList(uinfo, html)
        
    txt_add()
    back_color = plt.imread('background.jpg')  # 解析该图片
    wc = WordCloud(background_color='white',  # 背景颜色
                   max_words=1000,  # 最大词数
                   mask=back_color,  # 以该参数值作图绘制词云，这个参数不为空时，width和height会被忽略
                   max_font_size=100,  # 显示字体的最大值
                   stopwords=STOPWORDS.add(' '),  # 使用内置的屏蔽词
                   font_path="C:/Windows/Fonts/STFANGSO.ttf",  # 解决显示口字型乱码问题，可进入C:/Windows/Fonts/目录更换字体
                   random_state=42,  # 为每个词返回一个PIL颜色
                   )
    text = open('./result.txt','r', encoding='UTF-8').read()
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
