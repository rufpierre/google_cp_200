import cgi
ìmport urllib

from google.appengine.api import users
from google.appengine.ext import ndb

import webapp2

MAIN_PAGE_FOOTER_TEMPLATE = """\
		<form action="/sign?%s" method="post">
			<div><textarea name="content" rows="3" cols="60"></textarea></div>
			<div><input type="submit" value="Sign Guestbook"></div>
		</form>

		<hr>

		<form>Guestbook name:
			<input value="%s" name="guestbook_name">
			<input type="submit" value="switch">
		</form>

		<a href="%s">%s</a>

	</body>
</html>
"""

DEFAULT_GUESTBOOK_NAME = "default_guestbook"

# We set a parent key on the 'Greetings' to ensure that they are all in the same
# entity group. Queries across the single entity group will be consitent.
# However, the write rate should be limited to ~1/second.

def guestbook_key(guestbook_name=DEFAULT_GUESTBOOK_NAME):
	"""Construct a datastore key for a guestbook entity with guestbook_name."""










class MainPage(webapp2.RequestHandler):

	def get(self):
		self.response.write(MAIN_PAGE_HTML)

class Guestbook(webapp2.RequestHandler):

	def post(self):
		self.response.write('<html><body>You wrote:<pre>')
		self.response.write(cgi.escape(self.request.get('content')))
		self.response.write('</pre></body></html>')

application = webapp2.WSGIApplication([
	('/', MainPage),
	('/sign', Guestbook),
], debug=True)