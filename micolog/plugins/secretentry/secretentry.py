# -*- coding: utf-8 -*-

from micolog_plugin import *

class secretentry(Plugin):
    def __init__(self):
        Plugin.__init__(self, __file__)
        self.author="鸣"
        self.authoruri="http://qhm123.appspot.com"
        self.uri=""
        self.description="password protect for entry"
        self.register_filter('secretentry', self.secretentry)
        self.name="secretentry"
        self.version="0.1"
        
    def get(self, page):
        pass
    
    def post(self, page):
        pass
        
    def secretentry(self, content, blog=None, *arg1, **arg2):

        data = ''

        return data.encode('utf8')