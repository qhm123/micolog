# -*- coding: utf-8 -*-

from model import *
from micolog_plugin import *

def translate_bool_to_check(bool):
    if bool == "True":
        return "checked='checked'"
    else:
        return ""

class happychristmas(Plugin):
    def __init__(self):
        Plugin.__init__(self, __file__)
        self.author = "鸣"
        self.authoruri = "http://qhm123.appspot.com"
        self.uri = ""
        self.description = "create Christmas snowman Wish everyone a Merry Christmas!"
        self.name = "happychristmas"
        self.version = "0.1"
        self.register_filter('happychristmas', self.happychristmas)
        self.register_urlzip('/happychristmas/(.*)', 'happychristmas.zip')
        
    def get(self, page):
        showsnowman = OptionSet.getValue("happychristmas_showsnowman", default='True')
        snowmanonlyshowhome = OptionSet.getValue("happychristmas_snowmanonlyshowhome", default='True')
        showsnows = OptionSet.getValue("happychristmas_showsnows", default='True')
        snowsonlyshowhome = OptionSet.getValue("happychristmas_snowsonlyshowhome", default='True')
        return u'''<h3>设置happychristmas</h3>
               <form action="" method="post">
               <div><span>显示雪人:</span><input type="checkbox" name="showsnowman" value="on" %(showsnowman_checked)s /></div>
               <div><span>只在主页显示雪人:</span><input type="checkbox" name="snowmanonlyshowhome" value="on" %(snowmanonlyshowhome_checked)s /></div>
               <div><span>显示雪花:<input type="checkbox" name="showsnows" value="on" %(showsnows_checked)s /></div>
               <div><span>只在主页显示雪花:</span><input type="checkbox" name="snowsonlyshowhome" value="on" %(snowsonlyshowhome_checked)s /></div>
               <br />
               <input type="submit" value="确定">
               </form>
               <br />
               Powered By <a href="http://qhm123.appspot.com" target="_blank">鸣</a>
               ''' % {"showsnowman": showsnowman, 
                      "snowmanonlyshowhome": snowmanonlyshowhome, 
                      "showsnows": showsnows, 
                      "snowsonlyshowhome": snowsonlyshowhome,
                      "showsnowman_checked": translate_bool_to_check(showsnowman),
                      "snowmanonlyshowhome_checked": translate_bool_to_check(snowmanonlyshowhome),
                      "showsnows_checked": translate_bool_to_check(showsnows),
                      "snowsonlyshowhome_checked": translate_bool_to_check(snowsonlyshowhome)}

    def post(self, page):
        # parambool参见base，自动和on比较
        showsnowman = page.parambool("showsnowman")
        snowmanonlyshowhome = page.parambool("snowmanonlyshowhome")
        showsnows = page.parambool("showsnows")
        snowsonlyshowhome = page.parambool("snowsonlyshowhome")
        
        OptionSet.setValue("happychristmas_showsnowman", str(showsnowman))
        OptionSet.setValue("happychristmas_snowmanonlyshowhome", str(snowmanonlyshowhome))
        OptionSet.setValue("happychristmas_showsnows", str(showsnows))
        OptionSet.setValue("happychristmas_snowsonlyshowhome", str(snowsonlyshowhome))

        return self.get(page)

    def happychristmas(self, content, blog=None, *arg1, **arg2):
        try:
            ishome = bool(content.strip())
        except:
            return ""
         
        showsnowman = OptionSet.getValue("happychristmas_showsnowman", default='True')
        snowmanonlyshowhome = OptionSet.getValue("happychristmas_snowmanonlyshowhome", default='True')
        showsnows = OptionSet.getValue("happychristmas_showsnows", default='True')
        snowsonlyshowhome = OptionSet.getValue("happychristmas_snowsonlyshowhome", default='True')
        host = blog.baseurl.encode("utf8")
        
        snows = u'''<script type="text/javascript">
        sitePath = "%s/happychristmas/";
        sflakesMax = 84;
        sflakesMaxActive = 81;
        svMaxX = 4;
        svMaxY = 3;
        ssnowStick = 0;
        sfollowMouse = 1;
        </script>
        <script type="text/javascript" src="/happychristmas/snowstorm.js"></script>
        ''' % (host, )
        
        snowman = u'''<div id="MagicFace" Style="POSITION:absolute;Z-INDEX:99;visibility:hidden;">
        <script type="text/javascript" src="/happychristmas/wp-christmas.js"></script>
        </div>
        '''
        
        list = []
        if showsnows == 'True':
            if snowsonlyshowhome == 'True' and ishome:
                list.append(snows)
            if snowsonlyshowhome != 'True':
                list.append(snows)
        
        if showsnowman == 'True':
            if snowmanonlyshowhome == 'True' and ishome:
                list.append(snowman)
            if snowmanonlyshowhome != 'True':
                list.append(snowman)
            
        data = ''.join(list)
        return data
