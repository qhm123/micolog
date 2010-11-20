# -*- coding: utf-8 -*-

from micolog_plugin import *

class pagenavi(Plugin):
    def __init__(self):
        Plugin.__init__(self, __file__)
        self.author="鸣"
        self.authoruri="http://qhm123.appspot.com"
        self.uri=""
        self.description="pagenavi"
        self.register_filter('pagenavi', self.pagenavi)
        self.register_urlzip('/pagenavi/(.*)', 'pagenavi.zip')
        self.name="pagenavi"
        self.version="0.1"
        
    def get(self, page):
        pass
    
    def post(self, page):
        pass
        
    def pagenavi(self, content, blog=None, *arg1, **arg2):
        pagevar = content.split(',')
        page = pagevar[0]
        max_page = pagevar[1]
        data = u'''<div class="wp-pagenavi clearfix">
<link rel="stylesheet" type="text/css" href="/pagenavi/pagenavi.css" />
<script type="text/javascript" src="/pagenavi/pagenavi.js"></script>
<script type="text/javascript">showPageLink("/page/",%s,%s,"");</script>
</div>
''' % (page, max_page)
        return data.encode('utf8')