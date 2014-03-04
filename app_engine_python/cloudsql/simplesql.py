# -*- coding: utf-8 -*-

import cgi
import os
import urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import MySQLdb
import jinja2
import webapp2

# utilise les templates jinja

JINJA_ENVIRONMENT = jinja2.Environment(
	loader=jinja2.FileSystemLoader(os.path.dirname(__file__)),
	extensions=['jinja2.ext.autoescape'],
	autoescape=True)	

class MainPage(webapp2.RequestHandler):

	def get(self):
		self.response.write("Hello world!")

application = webapp2.WSGIApplication([
	('/', MainPage),
	#('/sign', Guestbook),
], debug=True)