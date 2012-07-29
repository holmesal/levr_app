import webapp2
import jinja2
import os
import levr_utils
import logging
import levr_classes as levr
##!!!! DOESNT HAVE ENCRYPTION HANDLING !!!! #### doesn't need it?
from gaesessions import get_current_session
from google.appengine.ext import db

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class merchantsLanding(webapp2.RequestHandler):
	def get(self):
		pass

class deal(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('templates/deal.html')
		self.response.out.write(template.render())
	

app = webapp2.WSGIApplication([('/merchants', merchantsLanding),
								('/merchants/deal',deal)],
								debug=True)