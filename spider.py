# -*- coding:utf-8 -*-

import urllib
import urllib2
import re
import time
from bs4 import BeautifulSoup

class Spider:
    
    #初始化
    def __init__(self):
        self.page_num = 1
        self.total_num = None
    
    #获取当前时间
    def getCurrentTime(self):
        return time.strftime('[%Y-%m-%d %H:%M:%S]',time.localtime(time.time()))
    
    #通过网页的页码数来构建网页的URL
    def getPageURLByNum(self, page_num):
        page_url = "http://iask.sina.com.cn/c/978-all-" + str(page_num) + ".html"
        return page_url
    
    
    #通过传入网页页码来获取网页的HTML
    def getPageByNum(self, num):
        request = urllib2.Request(self.getPageURLByNum(num))
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
    
    #主函数
    def main(self):
        self.total_num = self.getTotalPageNum()
        print self.getCurrentTime(),"获取到目录页面个数",self.total_num,"个"
        for x in range(1,int(self.total_num)+1):
            print self.getCurrentTime(),"正在抓取第",x,"个页面"

spider = Spider()
spider.main()       


