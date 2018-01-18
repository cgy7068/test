#!/usr/bin python
# -*- coding: utf-8 -*-
from HTMLParser import HTMLParser
import urllib2
import urllib
import sys
import time
reload(sys)
sys.setdefaultencoding('utf8')


class Spider():
    def get_content(self, url):
        self.url = url
        self.user_agent = 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.84 Safari/537.36'
        self.headers = {'User_Agent':self.user_agent}
        self.request = urllib2.Request(url=self.url, headers=self.headers)
        self.response = urllib2.urlopen(self.request)
        self.content = self.response.read()


class MyParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_span = False
        self.in_a = False
        self.urls = []

#获取个人主页链接
    def handle_starttag(self, tag, attrs):
        def _attr(attrlist, attrname):
            for attr in attrlist:
                if attr[0] == attrname:
                    return attr[1]
            return None
        if tag == 'span' and _attr(attrs, 'class') == 'frs-author-name-wrap':
            self.in_span = True
        if self.in_span == True and tag == 'a' and _attr(attrs, 'rel') == 'noreferrer':
            self.user = {}
            myurl = 'http://tieba.baidu.com'+_attr(attrs, 'href')
            self.user['url'] = myurl
            self.urls.append(myurl)
            self.in_span = False


class InfoParser(HTMLParser):
    def __init__(self):
        HTMLParser.__init__(self)
        self.in_myspan = False
        self.in_mydiv = False
        self.user = {}

    def handle_starttag(self, tag, attrs):
        def _attr(attrlist, attrname):
            for attr in attrlist:
                if attr[0] == attrname:
                    return attr[1]
            return None
        if tag == 'span' and _attr(attrs, 'class') == 'userinfo_username ':
            self.in_myspan = True
        elif tag == 'span' and _attr(attrs, 'class') == 'userinfo_username  vip_red ':
            self.in_myspan = True
        if tag == 'div' and _attr(attrs, 'class') == 'userinfo_left_head':
            self.in_mydiv = True
#获取用户名
    def handle_data(self, data):
        if self.in_myspan:
            self.user['name'] = data
            print('%(name)s' % self.user)
            self.in_myspan = False

#获取头像链接
    def handle_startendtag(self, tag, attrs):
        def _attr(attrlist, attrname):
            for attr in attrlist:
                if attr[0] == attrname:
                    return attr[1]
            return None
        if self.in_mydiv and tag == 'img':
            self.user['img_url'] = _attr(attrs, 'src')
            self.in_mydiv = False

#下载头像
def download_img(username, url):
    fname = username
    urllib.urlretrieve(url, 'E:\gy\spider\demos\imgs\%s.jpg' % fname)


if __name__ == "__main__":
    spider = Spider()
    spider.get_content(url='http://tieba.baidu.com/f?kw=python&fr=ala0&tpl=5')
    spider.parser = MyParser()
    spider.parser.feed(spider.content)
    for i in spider.parser.urls:
        print(i)
        detail_spider = Spider()
        detail_spider.get_content(url=i)
        detail_spider.parser = InfoParser()
        detail_spider.parser.feed(detail_spider.content)
        username = detail_spider.parser.user['name']
        username = username.encode('gb2312')
        download_img(username=username, url=detail_spider.parser.user['img_url'])
        time.sleep(1)
