# FinalHomework
python爬虫期末作业
## You should design and implement a web spider to crawl the OA system. 
## Starter URL:  http://www.ciomp.ac.cn/xwdt/zhxw/
## The date range: 2016-09-01~now
## The information you crawled should include the following information.
- Title
- Submission date
- Submission department
- Main body of the news
## The technology may use
- RegExp
- Multi-thread
- String Handle
- File I/O
## The results are indexed by the submission date
- One date one directory
- Named by the data like 2019-05-21
- One news one file 
- named by the title 
- saved in the same directory
## Simple analysis of the results
- The total amount of the crawled news. The more news your crawl, the more score you will get.
- The total amount news of each week and shown by curve [1]. If possible, divided by department.
- The average amount news of each day
- The average amount news of each weekday, it’s better to give a boxplot [2].
- The average amount news of each department, it’s better to give a boxplot 2].
- Other Statistics data you interested…
## The Word Cloud Plot of the results (20%)
- Segment the news by Jieba [3].
- Delete the stop words
- Extract the keywords of each news by TF-INF and TextRank (Jieba).
- Demonstrate one day’s news by word cloud plot and the scores (D3 [4-5]).
- Design a web page to demonstrate all the results indexed by date.
