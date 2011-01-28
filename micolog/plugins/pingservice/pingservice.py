# coding: utf-8

import logging
import xmlrpclib

from micolog_plugin import *

DEFAULT_PING_LISTS = """http://blogsearch.google.com/ping/RPC2
http://ping.baidu.com/ping/RPC2
http://www.feedsky.com/api/RPC2
http://blog.youdao.com/ping/RPC2
http://www.zhuaxia.com/rpc/server.php
http://www.xianguo.com/xmlrpc/ping.php
http://rpc.weblogs.com/RPC2
"""

class pingservice(Plugin):
    def __init__(self):
        Plugin.__init__(self, __file__)
        self.author = "鸣"
        self.authoruri = "http://qhm123.appspot.com"
        self.uri = "http://qhm123.appspot.com"
        self.description = "pingservice"
        self.name = "pingservice"
        self.version = "0.1"
        self.register_action('save_post', self.save_post)
        
        pinglists = OptionSet.get_by_key_name('pingservice_pinglists')
        if not pinglists:
            OptionSet.setValue('pingservice_pinglists', DEFAULT_PING_LISTS)
        
    def get(self, page):
        pinglists = OptionSet.getValue('pingservice_pinglists', '')
        return '''<h3>Ping lists</h3>
<form action="" method="post">
    <textarea name="pinglists" id="pinglists" cols="60" rows="10">%s</textarea>
    <input name="submit" id="submit" type="submit" value="submit" />
</form>
如果您对Ping服务不是很了解，最好不要更改以上默认列表。''' % (pinglists,)
    
    def post(self, page):
        self.pinglists = page.param('pinglists')
        OptionSet.setValue('pingservice_pinglists', self.pinglists)
        
        return self.get(page)

    def save_post(self, entry, *arg1, **arg2):
        if not entry.published:
            return
        self.pinglists = OptionSet.getValue('pingservice_pinglists', '')
        pinglists = self.pinglists.splitlines()
        
        site_domain = self.blog.baseurl
        site_name = self.blog.title
        entry_title = entry.title
        for url in pinglists:
            try:
                server = xmlrpclib.ServerProxy(url)
                response = server.weblogUpdates.ping(site_name, site_domain, entry_title, site_domain + '/feed')
                # NOTE: 各个ping服务商提供的返回结构不一，无法同意进行判断，
                # 如果没有出现异常则认为Ping操作成功。
                if response:
                    logging.info('OK: Ping service: ' + url)
                else:
                    logging.warning('Reached but got error: Ping service: ' + url)
            except:
                logging.warning('Failed: Ping service: ' + url)
