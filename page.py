# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import time
import types 
from bs4 import BeautifulSoup

#抓取分析某一问题和答案
class Page:
    
    def __init__(self):
        pass
    
    def getPageByURL(self, url):
        request = urllib2.Request(url)
        response = urllib2.urlopen(request)
        return response.read().decode("utf-8") 
    
    #传入一个List,返回它的标签里的内容,否则返回None
    def getText(self, html):
        if not type(html) is types.StringType:
            html = str(html)
        pattern = re.compile('<pre.*?>(.*?)</pre>', re.S)
        match = re.search(pattern, html)
        if match:
            return match.group(1)
        else: 
            return None
    
    #传入最佳答案的HTML,分析出回答者和回答时间
    def getGoodAnswerInfo(self, html):
        pattern = re.compile('"answer_tip.*?<a.*?>(.*?)</a>.*?<span class="time.*?>.*?\|(.*?)</span>', re.S)
        match = re.search(pattern, html)
        if match:
            return [match.group(1),match.group(2)]
        else:
            return [None,None]
    
    #传入回答者HTML,分析出回答者,回答时间
    def getOtherAnswerInfo(self, html):
        if not type(html) is types.StringType:
            html = str(html)
        pattern = re.compile('"author_name.*?>(.*?)</a>.*?answer_t">(.*?)</span>', re.S)
        match = re.search(pattern, html)
        if match:
            return [match.group(1),match.group(2)]
        else:
            return [None,None]
    
    
    #获得最佳答案
    def getGoodAnswer(self, page):
        soup = BeautifulSoup(page)
        text = soup.select("div.good_point div.answer_text pre")
        if len(text) > 0:
            ansText = self.getText(str(text[0]))
            info = soup.select("div.good_point div.answer_tip")
            ansInfo = self.getGoodAnswerInfo(str(info[0]))
            #将三者组合成一个List
            answer = [ansText, ansInfo[0], ansInfo[1],1]
            return answer
        else:
            return None
            
    #获得其他答案
    def getOtherAnswers(self, page):
        soup = BeautifulSoup(page)
        results =  soup.select("div.question_box li.clearfix .answer_info")
        #所有答案,包含好多个List,每个List包含了回答内容,回答者,回答时间
        answers = []
        for result in results:
            #获得回答内容
            ansSoup = BeautifulSoup(str(result))
            text = ansSoup.select(".answer_txt span pre")
            ansText = self.getText(str(text[0]))
            #获得回答者和回答时间
            info = ansSoup.select(".answer_tj")
            ansInfo = self.getOtherAnswerInfo(info[0])
            #将三者组合成一个List
            answer = [ansText, ansInfo[0], ansInfo[1],0]
            #加入到answers
            answers.append(answer)
        return answers
            
