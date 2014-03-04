# -*- coding: utf-8 -*-

import cgi
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

# utilise les templates

page_template = """
<form action='/sign' method='post'>
	<input type='text' name='content'/>
	<input type='submit' value='sign'/>
</form>
<br/>

<a href='%s'>%s</a>
"""

DEFAULT_GUESTBOOK = 'default_guestbook'

def get_key(guestbook_name=DEFAULT_GUESTBOOK):
	return ndb.Key('Guestbook', guestbook_name)

class Greeting(ndb.Model):
	author = ndb.UserProperty()
	content = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):

	def get(self):
		self.response.write('begin posts<br/>')

		## méthode api
		greetings_query = Greeting.query(ancestor=get_key()).order(-Greeting.date)
		greetings = greetings_query.fetch(10)

		## methode gql
		# greetings = ndb.gql('SELECT * '
		# 					'FROM Greeting '
		# 					'WHERE ANCESTOR IS :1 '
		# 					'ORDER BY date DESC LIMIT 10',
		# 					get_key())

		#&thinsp;, &ensp;,and &emsp;

		for greeting in greetings:
			self.response.write(greeting.content+'<br/>')
			self.response.write('&emsp;written by: '+greeting.author.nickname()+'<br/>')
			self.response.write('&emsp;at: '+str(greeting.date)+'<br/>')
			self.response.write('<br/>')
		self.response.write('end posts<br/>')

		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			link_text = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			link_text = 'Login'
		self.response.write(page_template%(url, link_text))


#		self.response.write('<a href="'+url+'">'+link_text+'</a>')

class Guestbook(webapp2.RequestHandler):

	def post(self):
		greeting = Greeting(parent=get_key())
		greeting.content = self.request.get('content')
		greeting.author = users.get_current_user()
		greeting.put()
		self.redirect('/')

application = webapp2.WSGIApplication([
	('/', MainPage),
	('/sign', Guestbook),
], debug=True)