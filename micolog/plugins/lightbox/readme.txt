lightbox是一个micolog的插件，用于实现lightBox图片查看效果。该插件采用最精简的只有6kb的JavaScript代码，兼容大部分浏览器。

使用说明：
1.将下载的插件解压缩。
2.将插件目录放入micolog的plugins目录下。
3.上传你的micolog。
4.在后台激活lightbox插件。
这样lightbox插件就设置完成了。

注意：请确保你的主题中的base.html文件中存在{%mf footer%}{%endmf%}标签，
如果没有请在base.html中footer下添加，主题支持列表参阅我的相关文章。

详细设置：
1.点击lightbox，进入lightbox设置页面。
2.共有5个选项可以设置。
3.对于第一个“是否加载jQuery”选项，需要确认你的base.html文件的head部分是否已经加载了jQuery，如果已加载，可以设置为false，放置重复加载。
4.剩余四个选项，是调节图片弹出显示效果使用。

使用示例：<a href="http://micolog.appspot.com/micolog/micolog.jpg" rel="lightbox" /><img src="http://micolog.appspot.com/micolog/micolog.jpg" /> </a>
说明：就是在你的<img />标签外部添加一个外包的标签<a>，<a>的href属性为展开后的图片地址。<img>的src属性为默认显示的图片地址。

具体效果可参看我的博客的这个页面http://qhm123.appspot.com/2010/10/9/micolog-lightbox-picture-plugin.html

有任何问题或发现bug可以到http://qhm123.appspot.com/2010/10/9/micolog-lightbox-picture-plugin.html留言，
我会尽快回复并修复，谢谢您的支持。

2010-10-14