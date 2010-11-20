# -*- coding: utf-8 -*-

import urllib

from micolog_plugin import *
from model import Tag

def my_urlencode(s):
    p = repr(s).replace(r'\x', '%')
    return p[1:-1]

class tagfilter(Plugin):
    def __init__(self):
        Plugin.__init__(self, __file__)
        self.author="鸣"
        self.authoruri="http://qhm123.appspot.com"
        self.uri=""
        self.description="filter tag by count"
        self.register_filter('tagfilter', self.tagfilter)
        self.name="tagfilter"
        self.version="0.1"
        
    def get(self, page):
        filter_count = OptionSet.getValue("tagfilter_filter_count", default='2')
        return u'''<h3>设置tagfilter</h3>
               <form action="" method="post">
               <div style="float:left;width:130px;">过滤个数:</div> <input name="filter_count" value="%s" /><br />
               <br />
               <input type="submit" value="确定">
               </form>
               <br />
               Powered By <a href="http://qhm123.appspot.com" target="_blank">鸣</a>
               ''' % (filter_count.encode,)
    
    def post(self, page):
        filter_count = page.param("filter_count")
        OptionSet.setValue("tagfilter_filter_count", filter_count)

        return self.get(page)
        
    def tagfilter(self, content, blog=None, *arg1, **arg2):
        filter_count = OptionSet.getValue("tagfilter_filter_count", default='2')
        filter_tags = Tag.all().filter('tagcount >', int(filter_count)).fetch(limit=1000)
        html = u"<a title='%d pages' href='/tag/%s' style='font-size:%dpx;'>%s</a>"
        tag_htmls = [html % (tag.tagcount, urllib.quote(tag.tag.encode('utf8')), tag.tagcount+10, tag.tag) for tag in filter_tags]
        data = ' '.join(tag_htmls)
        return data.encode('utf8')