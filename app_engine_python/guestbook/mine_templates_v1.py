# -*- coding: utf-8 -*-

import cgi
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import jinja2
import webapp2

# utilise les templates jinja

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)	

DEFAULT_GUESTBOOK = 'default_guestbook'

def get_key(guestbook_name=DEFAULT_GUESTBOOK):
	return ndb.Key('Guestbook', guestbook_name)

class Greeting(ndb.Model):
	author = ndb.UserProperty()
	content = ndb.StringProperty(indexed=False)
	date = ndb.DateTimeProperty(auto_now_add=True)

class MainPage(webapp2.RequestHandler):

	def get(self):
		guestbook_name = self.request.get('guestbook_name', DEFAULT_GUESTBOOK)

		## méthode api
		greetings_query = Greeting.query(ancestor=get_key()).order(-Greeting.date)
		greetings = greetings_query.fetch(10)

		if users.get_current_user():
			url = users.create_logout_url(self.request.uri)
			link_text = 'Logout'
		else:
			url = users.create_login_url(self.request.uri)
			link_text = 'Login'

		template_values = {
			'greetings': greetings,
			'guestbook_name': urllib.quote_plus(guestbook_name),
			'url': url,
			'link_text': link_text
		}

		template = JINJA_ENVIRONMENT.get_template('index.html')
		self.response.write(template.render(template_values))

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