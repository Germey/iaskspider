# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import time
import types
import page

from bs4 import BeautifulSoup

class Spider:
    
    #初始化
    def __init__(self):
        self.page_num = 1
        self.total_num = None
        self.page_spider = page.Page()
    
    #获取当前时间
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))
    
    #获取当前时间
    def getCurrentDate(self):
        return time.strftime('%Y-%m-%d',time.localtime(time.time()))
    
    #通过网页的页码数来构建网页的URL
    def getPageURLByNum(self, page_num):
        page_url = "http://iask.sina.com.cn/c/978-all-" + str(page_num) + ".html"
        return page_url
    
    
    #通过传入网页页码来获取网页的HTML
    def getPageByNum(self, page_num):
        request = urllib2.Request(self.getPageURLByNum(page_num))
        try:
            response = urllib2.urlopen(request)
        except urllib2.URLError, e:
            if hasattr(e, "code"):
                print self.getCurrentTime(),"获取页面失败,错误代号", e.code
                return None
            if hasattr(e, "reason"):
                print self.getCurrentTime(),"获取页面失败,原因", e.reason
                return None
        else:
            page =  response.read().decode("utf-8")
            return page
    
    #获取所有的页码数
    def getTotalPageNum(self):
        print self.getCurrentTime(),"正在获取目录页面个数,请稍候"
        page = self.getPageByNum(1)
        #匹配所有的页码数,\u4e0b\u4e00\u9875是下一页的UTF8编码
        pattern = re.compile(u'<span class="more".*?>.*?<span.*?<a href.*?class="">(.*?)</a>\s*<a.*?\u4e0b\u4e00\u9875</a>', re.S)
        match = re.search(pattern, page)
        if match:
            return match.group(1)
        else:
            print self.getCurrentTime(),"获取总页码失败"
    
    #分析问题的代码,得到问题的提问者,问题内容,回答个数,提问时间
    def getQuestionInfo(self, question):
        if not type(question) is types.StringType:
            question = str(question)
        #print question
        pattern = re.compile(u'<span.*?question-face.*?>.*?<img.*?alt="(.*?)".*?</span>.*?<a href="(.*?)".*?>(.*?)</a>.*?answer_num.*?>(\d).*?</span>.*?answer_time.*?>(.*?)</span>', re.S)
        match = re.search(pattern, question)
        if match:
            #获得提问者
            author = match.group(1)
            #问题链接
            href = match.group(2)
            #问题详情
            text = match.group(3)
            #回答个数
            ans_num = match.group(4)
            #回答时间
            time = match.group(5)
            time_pattern = re.compile('\d{4}\-\d{2}\-\d{2}', re.S)
            time_match = re.search(time_pattern, time)
            if not time_match:
                time = self.getCurrentDate()
            return [author, href, text, ans_num, time]
        else:
            return None
        
        
    
    #获取全部问题
    def getQuestions(self, page_num):
        page = self.getPageByNum(page_num)
        soup = BeautifulSoup(page)
        questions = soup.select("div.question_list ul li")
        for question in questions:
            info = self.getQuestionInfo(question)
            if info:
                url = "http://iask.sina.com.cn/" + info[1]
                good_ans = self.page_spider.getAnswer(url)
                
        
    
    
    #主函数
    def main(self):
        self.total_num = self.getTotalPageNum()
        print self.getCurrentTime(),"获取到目录页面个数",self.total_num,"个"
        self.getQuestions(1)
        #for x in range(1,int(self.total_num)+1):
        #print self.getCurrentTime(),"正在抓取第",x,"个页面"

spider = Spider()
spider.main()       


