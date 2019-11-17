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
import datetime

from pylab import *
mpl.rcParams['font.sans-serif'] = ['SimHei']

last_page = 1
max_steps=27
page_number=0
week = [0 for i in range(0,170)]
subwriter = ' '

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
    global last_page , max_steps , page_number , week , subwriter
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
             
        if re.findall(r'xwzx2015',sublink) or re.findall(r'chengguozhuanhua2',sublink) \
            or re.findall(r'lxyz_zbdt',sublink) or re.findall(r'chengguojiangliguanli',sublink):
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
        mytext = subdata.get_text()
        txtname = mydate[i].string + subwriter.string + '《' + mydata[i].string + '》'
        text_create(txtname,mytext.replace(u'\xa0',u''))          #生成对应txt文件

        #对发布日期进行统计分析（每周发布数量）
        date_str = re.findall(r"\d+",mydate[i].string)
        date_year = int(date_str[0])
        date_month = int(date_str[1])
        date_day = int(date_str[2])
        interval = datetime.datetime(date_year,date_month,date_day)-datetime.datetime(2016,8,29)
        week_count = interval.days//7
        week[week_count]+=1
        #print(week[week_count])


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

def DepartmentNub():
    result = pattern = ['0' for i in range(0,44)]
    all_the_text = open('./writers.txt', 'r',encoding='UTF-8').read()
    pattern[0] =re.compile(u"应光室|应光室党支部")
    pattern[1] =re.compile(u"发光室")
    pattern[2] =re.compile(u"空间新技术部")
    pattern[3] =re.compile(u"探测部|光电探测部")
    pattern[4] =re.compile(u"图像部|图像室")
    pattern[5] =re.compile(u"空间部|空间一部|空间二部|空间三部")
    pattern[6] =re.compile(u"航测部|航测一部|航测二部|航测三部|航测二部党支部")
    pattern[7] =re.compile(u"Light中心")
    pattern[8] =re.compile(u"信息中心")
    pattern[9] =re.compile(u"研究生部")
    pattern[10] =re.compile(u"质检中心")
    pattern[11] =re.compile(u"长光集团")
    pattern[12] =re.compile(u"人力资源处|人力处")
    pattern[13] =re.compile(u"基础科研处|基础处|基础科研管理处")
    pattern[14] =re.compile(u"光栅中心|光栅中心党支部|光栅中心党总支")
    pattern[15] =re.compile(u"保密管理处|保密处")
    pattern[16] =re.compile(u"离退中心")
    pattern[17] =re.compile(u"党委办公室|党办")
    pattern[18] =re.compile(u"研发中心")
    pattern[19] =re.compile(u"知识产权与成果转化处|成果转化处|成果处")
    pattern[20] =re.compile(u"国际合作处|国合处")
    pattern[21] =re.compile(u"光学中心|光学中心党支部")
    pattern[22] =re.compile(u"光子实验室")
    pattern[23] =re.compile(u"工程处")
    pattern[24] =re.compile(u"质量管理处|质量处")
    pattern[25] =re.compile(u"所办|所长办公室")
    pattern[26] =re.compile(u"条件保障处")
    pattern[27] =re.compile(u"长光华大")
    pattern[28] =re.compile(u"电装中心|电装中心党支部")
    pattern[29] =re.compile(u"监察审计处|监审处")
    pattern[30] =re.compile(u"青促会|青促会长光活动小组|青促会活动小组|长光所青促会活动小组")
    pattern[31] =re.compile(u"奥普公司|奥普公司质管部生吉林|奥普公司研发中心党支部|奥普质管部")
    pattern[32] =re.compile(u"机器人中心|空间机器人中心党支部")
    pattern[33] =re.compile(u"孵化器|孵化器公司")
    pattern[34] =re.compile(u"长光青年学术社")
    pattern[35] =re.compile(u"OSA/SPIE学生分会|OSA/SPIE长春光机所学生分会")
    pattern[36] =re.compile(u"长光所羽毛球协会")
    pattern[37] =re.compile(u"科宇公司")
    pattern[38] =re.compile(u"光电对抗党总支创新室党支部")
    pattern[39] =re.compile(u"期刊编辑部|中国光学编辑部")
    pattern[40] =re.compile(u"光学技术中心")
    pattern[41] =re.compile(u"长光瑞思")
    pattern[42] =re.compile(u"新产业公司|新产业公司党支部")
    pattern[43] =re.compile(u"工程师培训中心")
    for i in range(44):
        result[i] = len(re.findall(pattern[i],all_the_text))
        #print(result[i])
    x1 = ['应光室','发光室','空间新技术部','探测部','图像部',\
          '空间部','航测部','Light中心','信息中心','研究生部',\
          '质检中心','长光集团','人力资源处','基础科研处','光栅中心',\
          '保密管理处','离退中心','党委办公室','研发中心','知识产权与成果转化处',\
          '国际合作处','光学中心','光子实验室','工程处','质量管理处',\
          '所办','条件保障处','长光华大','电装中心','监察审计处',\
          '青促会','奥普公司','机器人中心','孵化器','长光青年学术社',\
          'OSA/SPIE学生分会','长光所羽毛球协会','科宇公司','光电对抗党总支创新室党支部','期刊编辑部',\
          '光学技术中心','长光瑞思','新产业公司','工程师培训中心']
    plt.figure()
    plt.xticks(rotation=90)
    plt.bar(x1,result,label='Count')
    plt.xlabel('Number issued by each department')
    plt.ylabel('The article number')
    plt.title('Department')
    plt.show()

def main():
    global page_number , week
    uinfo = []
    process_bar = ShowProcess(max_steps, 'OK')
    open('writers.txt','w', encoding='UTF-8')
    os.remove("writers.txt")
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
    wc.recolor(color_func=image_colors)
    wc.to_file('WordCloud_out.png')    # 保存图片

    fig0 = plt.figure()
    fig_wc = fig0.add_subplot(121) 
    fig_wc.imshow(wc)    # 负责对图像进行处理，并显示其格式
    fig_wc.axis('off')    # 关闭坐标轴
    
    fig_week = fig0.add_subplot(122) 
    fig_week.axis('on')    # 开启坐标轴
    x1 = range(0,170)
    fig_week.plot(x1,week,label='Count',color='r',markerfacecolor='r',markersize=12)
    plt.xlabel('Week Number')
    plt.ylabel('The article number')
    plt.title('Release statistics')
    plt.show()
    DepartmentNub()

main()
