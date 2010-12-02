# -*- coding: utf-8 -*-

from micolog_plugin import *
from model import *

class lightbox(Plugin):
    def __init__(self):
        Plugin.__init__(self, __file__)
        self.author = "鸣"
        self.authoruri = "http://qhm123.appspot.com"
        self.uri = ""
        self.description = "overlay images on the pages"
        self.register_filter('footer', self.footer)
        self.register_urlzip('/lightbox/(.*)', 'lightbox.zip')
        self.name = "lightbox"
        self.version = "0.2"

    def get(self, page):
        entryselector = OptionSet.getValue("lightbox_entryselector", default='false')           # 正文处选择器
        loadjquery = OptionSet.getValue("lightbox_loadjquery", default='true')                  # 是否加载jquery
        bgcolor = OptionSet.getValue("lightbox_bgcolor", default='#000')                        # 背景颜色
        bgopacity = OptionSet.getValue("lightbox_bgopacity", default='0.8')                     # 背景透明度
        fixednavi = OptionSet.getValue("lightbox_fixednavi", default='false')                   # 导航按钮是否固定
        speed = OptionSet.getValue("speed", default='400')                                      # 展开速度
        return u'''<h3>设置lightbox</h3>
               <form action="" method="post">
               <div style="float:left;width:130px;">正文选择器:</div><input name="entryselector" value="%s" />(格式：.(#)正文处div的class(id)名称-启用；false-禁用，默认值false)<br />
               <div style="float:left;width:130px;">是否加载jquery:</div> <input name="loadjquery" value="%s" />(格式：false-不加载 ;true-加载，默认值true)<br />
               <div style="float:left;width:130px;">背景颜色:</div><input name="bgcolor" value="%s" />(格式：#rrggbb，默认值#000)<br />
               <div style="float:left;width:130px;">背景透明度:</div> <input name="bgopacity" value="%s" />(格式：0.X，其中X只能是从0到9的整数，默认值0.8)<br />
               <div style="float:left;width:130px;">导航按钮是否固定:</div> <input name="fixednavi" value="%s" />(格式：false-不固定 ;true-固定，默认值false)<br />
               <div style="float:left;width:130px;">展开速度: </div><input name="speed" value="%s" />(格式：整数，单位毫秒，默认值400)<br />
               <br />
               <input type="submit" value="确定">
               </form>
               <br />
               Powered By <a href="http://qhm123.appspot.com" target="_blank">鸣</a>
               ''' % (entryselector, loadjquery, bgcolor, bgopacity, fixednavi, speed)

    def post(self, page):
        entryselector = page.param("entryselector")     # 正文处选择器
        loadjquery = page.param("loadjquery")           # 是否加载jquery
        bgcolor = page.param("bgcolor")                 # 背景颜色
        bgopacity = page.param("bgopacity")             # 背景透明度
        fixednavi = page.param("fixednavi")             # 导航按钮是否固定
        speed = page.param("speed")                     # 展开速度
        
        OptionSet.setValue("lightbox_entryselector", entryselector) # 正文处选择器
        OptionSet.setValue("lightbox_loadjquery", loadjquery)       # 是否加载jquery
        OptionSet.setValue("lightbox_bgcolor", bgcolor)             # 背景颜色
        OptionSet.setValue("lightbox_bgopacity", bgopacity)         # 背景透明度
        OptionSet.setValue("lightbox_fixednavi", fixednavi)         # 导航按钮是否固定
        OptionSet.setValue("lightbox_speed", speed)                 # 展开速度
        return self.get(page)

    def footer(self, content, blog=None, *arg1, **arg2):
        entryselector = "'"+OptionSet.getValue("lightbox_entryselector", default='false').encode("utf8")+"'"# 正文处选择器 
        loadjquery = OptionSet.getValue("lightbox_loadjquery", default='true').encode("utf8")       # 是否加载jquery
        bgcolor = OptionSet.getValue("lightbox_bgcolor", default='#000').encode("utf8")             # 背景颜色
        bgopacity = OptionSet.getValue("lightbox_bgopacity", default='0.8').encode("utf8")          # 背景透明度
        fixednavi = OptionSet.getValue("lightbox_fixednavi", default='false').encode("utf8")        # 导航按钮是否固定
        speed = OptionSet.getValue("lightbox_speed", default='400').encode("utf8")                  # 展开速度
        host = blog.baseurl.encode("utf8")
        if loadjquery == 'true':
            jquery = '<script type="text/javascript" src="http://ajax.googleapis.com/ajax/libs/jquery/1.4.2/jquery.min.js"></script>'
        else:
            jquery = ''
        jquery = jquery.encode("utf8")
        data = content + '''<link rel="stylesheet" type="text/css" href="/lightbox/css/jquery.lightbox-0.5.css" media="screen" />
%(jquery)s
<script type="text/javascript" src="/lightbox/js/jquery.lightbox-0.5.pack.js"></script>
<script type="text/javascript">
$(function() {
    allanchors = null;
    if(%(entryselector)s == 'false'){
        allanchors = $('a[rel=lightbox]');
    } else{
        $(%(entryselector)s+' img').each(function(){
            img = $(this);
            if(img.parent('a').length < 1){
                src = img.attr('src');
                img.wrap('<a href='+src+'></a>');
            }
        });
        allanchors = $(%(entryselector)s+' a:has(img)');
    }
    allanchors.lightBox({
        overlayBgColor: '%(bgcolor)s',
        overlayOpacity: %(bgopacity)s,
        fixedNavigation: %(fixednavi)s,
        containerResizeSpeed: %(speed)s,
        imageLoading: '%(host)s/lightbox/images/lightbox-ico-loading.gif',
        imageBtnClose: '%(host)s/lightbox/images/lightbox-btn-close.gif',
        imageBtnPrev: '%(host)s/lightbox/images/lightbox-btn-prev.gif',
        imageBtnNext: '%(host)s/lightbox/images/lightbox-btn-next.gif',
        imageBlank: '%(host)s/lightbox/images/lightbox-blank.gif'
    });
});
</script>
'''.encode("utf8") % {'jquery': jquery,
                      'entryselector': entryselector,
                      'bgcolor': bgcolor,
                      'bgopacity': bgopacity,
                      'fixednavi': fixednavi,
                      'speed': speed,
                      'host': host}
        return data
