#!/usr/bin/env python
#coding=utf-8

'''
Created on 2010-12-03
GPL License
@author: sypxue@gmail.com
'''

from micolog_plugin import *
from model import OptionSet,Category
from google.appengine.api import urlfetch
class tableofcontents(Plugin):
	def __init__(self):
		Plugin.__init__(self,__file__)
		self.author="sypxue"
		self.authoruri="http://sypxue.appspot.com"
		self.uri="http://sypxue.appspot.com"
		self.description="""将文章内容中指定的标签自动形成文章内容导航目录的样式，方便读者快速移动到某个标题的位置。"""
		self.name="Table of contents"
		self.version="0.1"
		self.register_filter('entry_content',self.filter)
		self.default_config = {'tags':['h2','h4'],'style':''}
		self.anchors = {}
		self.toctags = ''
	
	def filter(self,content,*arg1,**arg2):
		cfg = OptionSet.getValue("tableofcontents_config",default=self.default_config)
		tags = cfg['tags']
		style = cfg['style']
		out,tocli='',[]
		if style:
			out += """<style type="text/css">""" + style.encode('utf-8') + "</style>"
		p = '|'.join(tags)
		docli = []
		if p:
			docli = re.findall('(<('+p+').*?>.*?</('+p+')>)',content)
		doctags = [i[1] for i in docli]
		doctags = [j for j in tags if doctags.count(j)>0]
		self.toctags = '|'.join(doctags)
		if doctags:
			tocli = self.g(doctags,docli)
		if tocli:
			out += """ 
			<div id="toc">
				<div id="toc-tit">文章导航 &nbsp; <a href="javascript:void(0);" onclick="(function(o){ $('#toc-content').toggle();if($(o).html()=='[隐藏]'){$(o).html('[显示]');}else{$(o).html('[隐藏]');} })(this)">[隐藏]</a></div>
				<div id="toc-content">
			"""
			out += self.toc(tocli,0)
			out += """ 
				</div>
			</div>
			"""
		else:
			return content
		return out + self.format(content)
	
	def format(self,content):
		s = content
		for i,j in self.anchors.items():
			#p = re.findall('(<(.*?)>(.*?)</.*?>)',i)[0]
			#a = p[0].replace(p[2],'<a name="'+j+'"></a>'+p[2])
			s = s.replace(i,'<a name="'+j+'"></a>'+i)
		return s
	
	def toc(self, li,level):
		s = '<ul class="toc-ul toc-level'+str(level)+'">'
		j=0
		for i in li:
			j+=1
			s += '<li>'
			b = 'toc-level'+str(level)+'-'+str(j)
			self.anchors[i[1]] = b
			a = re.findall('>(.*?)</',i[1])
			s += '<a href="#'+b+'">'+a[0]+'</a>'
			if len(i)>2:
				s += self.toc(i[2],level+1)
			s += '</li>'
		s += '</ul>'
		return s

	#获取同级目录
	def g(self,tags,li):
		if len(tags)==1:
			return [[i[1],i[0]] for i in li]
		a,b=[],[]
		for i in li:
			if i[1]==tags[0]:
				if b:
					a[-1].append(b)
					b=[]
				a.append([i[1],i[0]])
			else:
				b.append(i)
		if b:
			a[-1].append(b)		
		for i in a:
			if len(i)>2:
				i[2] = self.g(tags[1:],i[2])
		return a

	def get(self,page):
		cfg=OptionSet.getValue("tableofcontents_config",default=self.default_config)
		return '''<h3>文章内容导航目录生成</h3>
					<form action="" method="post">
					<p>输入多个html标签,用","分割:</p>
					<input name="tags" style="width:400px;" value="%s">
					该插件有多级目录支持,请按标签优先级高低依次输入
					<br>
					<p>输入所需的Css样式</p>
					<textarea name="style" style="width:400px;height:80px;">%s</textarea>
					如果已在其他位置定义，可留空<br />
					<br />
					<input type="submit" value="submit">
					</form>'''%(','.join([i.encode('utf-8') for i in cfg['tags']]),cfg['style'].encode('utf-8'))

	def post(self,page):
		cfg={}
		tags=page.param("tags").split(',')
		style=page.param("style")
		cfg['tags'] = tags
		cfg['style'] = style
		OptionSet.setValue("tableofcontents_config",cfg)
		return self.get(page)
