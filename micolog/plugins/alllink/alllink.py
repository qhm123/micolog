# -*- coding: utf-8 -*-

from base import BaseRequestHandler, requires_admin
from model import Link
from micolog_plugin import *

class alllink(Plugin):
	def __init__(self):
		Plugin.__init__(self, __file__)
		self.author = "鸣"
		self.authoruri = "http://qhm123.appspot.com"
		self.uri = ""
		self.description = "manage links categories"
		self.name = "alllink"
		self.version = "0.1"
		self.register_urlhandler('/admin/plugins/alllink/links', index_handler)
		self.register_urlhandler('/admin/plugins/alllink/link', add_handler)

	def get(self, page):
		return '''
		<a href="/admin/plugins/alllink/links">链接管理</a>
		<a href="/admin/plugins/alllink/link">添加链接</a>
		'''

	def post(self, page):
		return self.get(page)

class index_handler(BaseRequestHandler):
	@requires_admin
	def get(self, slug=None):
		context = {'current': 'plugins', 'links': Link.all()}
		self.render2('plugins/alllink/links.html', context)
		
	@requires_admin
	def post(self):
		linkcheck = self.request.get_all('linkcheck')
		for link_id in linkcheck:
			kid = int(link_id)
			link = Link.get_by_id(kid)
			link.delete()
		self.redirect('/admin/plugins/alllink/links')

class add_handler(BaseRequestHandler):
	@requires_admin
	def get(self, slug=None):
		action = self.param("action")
		vals = {'current': 'plugins'}
		if action and action == 'edit':
			try:
				action_id = int(self.param('id'))
				link = Link.get_by_id(action_id)
				vals.update({'link': link})
			except:
				pass
		else:
			action = 'add'
		vals.update({'action': action})
		self.render2('plugins/alllink/link.html', vals)

	@requires_admin
	def post(self):
		action = self.param("action")
		name = self.param("link_name")
		url = self.param("link_url")
		comment = self.param("link_comment")
		type = self.param("link_type")

		vals = {'action': action, 'postback': True, 'current': 'plugins'}
		if not (name and url and type):
			vals.update({'result': False, 'msg': _('Please input name and url and type.')})
			self.render2('plugins/alllink/link.html', vals)
		else:
			if action == 'add':
				link = Link(linktext=name, href=url, linkcomment=comment, linktype=type)
				link.put()
				#vals.update({'result':True, 'msg':'Saved ok'})
				self.redirect('/admin/plugins/alllink/links')
			elif action == 'edit':
				try:
					action_id = int(self.param('id'))
					link = Link.get_by_id(action_id)
					link.linktext = name
					link.href = url
					link.linkcomment = comment
					link.linktype = type
					link.put()
					#goto link manage page
					self.redirect('/admin/plugins/alllink/links')
				except:
					vals.update({'result':False, 'msg':_('Error:Link can''t been saved.')})
					self.render2('plugins/alllink/link.html', vals)