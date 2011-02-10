# -*- coding: utf-8 -*-
from micolog_plugin import *
import logging
import urllib
from model import *
from google.appengine.api import users
from base import BaseRequestHandler,cache
from google.appengine.ext import webapp
from datetime import datetime, timedelta

def urlencode(value):
	return urllib.quote(value.encode('utf8'))

class wapblog(Plugin):
	def __init__(self):
		Plugin.__init__(self,__file__)
		self.author="云在天边"
		self.authoruri="http://www.tangblog.info"
		self.uri="http://www.tangblog.info"
		self.description="Micolog WAP Blog插件,使用该插件可以方便在手机上浏览新博文，查看并发表评论。（默认仅支持Google Account用户登陆留言，这样可以降低垃圾留言数量。）"
		self.name="Micolog Wap Blog"
		self.version="0.5"
		self.register_urlhandler('(?i)/wap',waphandler)
		self.register_urlhandler('/wap/(\d+)',waphandler)
		self.register_urlhandler('(?i)/wap/page',pagehandler)
		self.register_urlhandler('(?i)/wap/post_comment',postComment)
		self.register_urlhandler('(?i)/wap/(.*)',Error404)

	def get(self,page):
		postcount=OptionSet.getValue("posts_per_page",default="8")
		commentcount=OptionSet.getValue("LatestCommentCount",default="5")
		return '''
		<h3>“WAP Blog”插件已经工作！</h3>
		<p>请完善如下设置</p>
		<form action="" method="post">
		每页显示文章数目:<input name="PostCount" value="%s" onKeyUp="this.value=this.value.replace(/\D/g,'')" onafterpaste="this.value=this.value.replace(/\D/g,'')"  /><br />
		文章最近评论数目:<input name="CommentCount" value="%s" onKeyUp="this.value=this.value.replace(/\D/g,'')" onafterpaste="this.value=this.value.replace(/\D/g,'')"  />(若该值设为0，将显示所有留言)<br />
		<br>
		<input type="submit" title="Save" value="保存">
		</form>
		<p>恭喜你!  你的"Micolog WAP Blog" 插件已经工作!<br />访问Wap页面的URL是：
		<a href="/wap" target="_blank">http://www.yourdomain.com/wap</a><br />
		<b>作者:</b><a href="http://www.tangblog.info" target="_blank">云在天边</a><br/></p>
		<p>您的支持是创作者继续发展的动力，感谢您以实际行动来帮助作者！</p>
		<p>如果在使用过程中遇到任何问题，请到作者的留言板(云在天边 <a href="http://www.tangblog.info/contact">www.tangblog.info/contact</a>)提交报告！</p>
		'''%(postcount,commentcount)

	def post(self,page):
		postcount=int(page.param("PostCount"))
		commentcount=int(page.param("CommentCount"))
		OptionSet.setValue("posts_per_page",postcount)
		OptionSet.setValue("LatestCommentCount",commentcount)
		return self.get(page)

class waphandler(BaseRequestHandler):
	def get(self,page=1):
		self.doget(page)

	@cache()
	def doget(self,page):
		from model import g_blog
		page=int(page)
		entrycount=g_blog.postscount()
		posts_per_page = OptionSet.getValue("posts_per_page",default="8")
		if posts_per_page:
			posts_per_page = 8
		max_page = entrycount / posts_per_page + ( entrycount % posts_per_page and 1 or 0 )
		comments=Comment.all().order('-date').fetch(5)

		if page < 1 or page > max_page:
			return Error404

		entries = Entry.all().filter('entrytype =','post').\
				filter("published =", True).order('-date').\
				fetch(posts_per_page, offset = (page-1) * posts_per_page)

		show_prev =entries and  (not (page == 1))
		show_next =entries and  (not (page == max_page))


		self.render2("plugins/wapblog/index.html",{'entries':entries,
						'show_prev' : show_prev,
						'show_next' : show_next,
						'pageindex':page,
						'ishome':True,
                        'pagecount':max_page,
                        'postscount':entrycount,
						'comments':comments
							})

class pagehandler(BaseRequestHandler):
	@cache()
	def get(self,*arg1):
		id=int(self.param("id"))
		time=datetime.now()
		commentcount = OptionSet.getValue("LatestCommentCount",default="5")
		if commentcount:
			commentcount = 5
		entries = Entry.all().filter("published =", True).filter('entrytype =','post').filter('post_id =',id).fetch(1)
		entry=entries[0]
		if commentcount==0:
			comments=Comment.all().filter("entry =",entry).order('-date')
		else:
			comments=Comment.all().filter("entry =",entry).order('-date').fetch(commentcount)
		Comments=Comment.all().filter("entry =",entry).order('-date')
		user = users.get_current_user()
		if user:
			greeting = ("Welcome, %s! (<a href=\"%s\">sign out</a>)" % 
			(user.nickname(), users.create_logout_url(self.request.uri)))
			email = user.email()
			try:
				query = Comment.all().filter('email =',email).order('-date').fetch(1)
				name = query[0].author
				weburl = query[0].weburl
			except:
				name=user.nickname()
				weburl=None
			self.render2("plugins/wapblog/page.html",{'entry':entry,'id':id,'comments':comments,'Comments':Comments,'user_name':name,'user_email':email,'user':user,'user_url':weburl,'greeting':greeting,'time':time})
		else:
			greeting = ("<a href=\"%s\">Sign in with your Google Account</a>." %
			users.create_login_url(self.request.uri)) 
			self.render2("plugins/wapblog/page.html",{'entry':entry,'id':id,'comments':comments,'Comments':Comments,'greeting':greeting,'user':user,'time':time})

class postComment(BaseRequestHandler):
	def get(self,*arg1):
		self.response.set_status(405)
		self.write('<h1>405 Method Not Allowed</h1>\n<a href="/wap">Back</a>')
	def post(self):
		name=self.param('author')
		#email=self.param('email')
		url=self.param('url')
		key=self.param('key')
		content=self.param('comment')
		parent_id=self.paramint('parentid',0)
		reply_notify_mail=True
		user = users.get_current_user()
		try:
			email=user.email()
		except:
			email=None
		if not (name and email and content):
			self.response.out.write('Please input name and comment content .\n <a href="javascript:history.back(-1)">Back</a>')
		else:
			comment=Comment(author=name,
							content=content+"<br /><small>from wap blog</small>",
							email=email,
							reply_notify_mail=reply_notify_mail,
							entry=Entry.get(key))
			starturl='http://'
			if url:
				try:
					if not url.startswith(('http://','https://')):
						url = starturl + url
					comment.weburl=url
				except:
					comment.weburl=None
			info_str='#@#'.join([urlencode(name),urlencode(email),urlencode(url)])
			logging.info("info:"+name+"#@#"+info_str + "Comment Form Wap Site") 
			cookiestr='comment_user=%s;expires=%s;domain=%s;path=/'%( info_str,
					(datetime.now()+timedelta(days=100)).strftime("%a, %d-%b-%Y %H:%M:%S GMT"),
					'' )
			comment.ip=self.request.remote_addr
			if parent_id:
				comment.parent=Comment.get_by_id(parent_id)
			comment.no=comment.entry.commentcount+1
			try:
				comment.save()
				memcache.delete("/"+comment.entry.link)
				self.response.headers.add_header( 'Set-Cookie', cookiestr)
				self.redirect(self.referer+"#comment-"+str(comment.key().id()))
				comment.entry.removecache()
				memcache.delete("/feed/comments")
			except:
				self.response.out.write('Comment not allowed .\n <a href="javascript:history.back(-1)">Back</a>')

class Error404(BaseRequestHandler):
	def get(self,*arg1):
		self.response.clear() 
		self.response.set_status(404)
		self.response.out.write('<h1>404 Not Found</h1>\n<a href="/wap">Back To Main Page ! </a>')
