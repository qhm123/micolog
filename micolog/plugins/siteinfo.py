# -*- coding: utf-8 -*-

from micolog_plugin import *
from model import *

HTML_DEFAULT = u"""
<div>文章数量：%(entrycount)s</div>
<div>评论数量：%(commentcount)s</div>
<div>浏览数量：%(readtimes)s</div>
"""

class siteinfo(Plugin):
    def __init__(self):
        Plugin.__init__(self, __file__)
        self.author="鸣"
        self.authoruri="http://qhm123.appspot.com"
        self.uri=""
        self.description="show siteinfo for sidebar"
        self.register_filter('siteinfo', self.siteinfo)
        self.name="siteinfo"
        self.version="0.1"
        
    def siteinfo(self, content, blog=None, *arg1, **arg2):
        html = OptionSet.getValue("siteinfo_html", default=HTML_DEFAULT)
        entrycount = Entry.all().filter('entrytype =','post').filter("published =", True).count()    # 发布文章数
        commentcount = Comment.all().count()   # 评论数
        readtimes = (entry.readtimes for entry in Entry.all().filter('entrytype =','post').filter("published =", True))
        totaltimes = 0  # 总的阅读次数
        for readtime in readtimes:
            totaltimes += readtime

        data = html % {"entrycount": entrycount,
                       "commentcount": commentcount,
                       "readtimes": totaltimes,}
        
        return data.encode('utf8')
    
    def get(self, page):
        html = OptionSet.getValue("siteinfo_html", default=HTML_DEFAULT)
        return u"""<h3>siteinfo</h3>
        <form action="" method="post">
        <p>siteinfo HTML:</p>
        <textarea name="html" style="width:500px;height:100px;">%s</textarea>
        <br>
        <input type="submit" value="submit">
        </form>
        """ % html
    
    def post(self, page):
        html = page.param('html')
        OptionSet.setValue("siteinfo_html", html)
        
        return self.get(page)