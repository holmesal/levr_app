import webapp2
import json
import logging
import os
import jinja2
from google.appengine.ext import db
from google.appengine.api import images
#from google.appengine.api import mail
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class new(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('templates/deal.html')
		self.response.out.write(template.render())
		
	

app = webapp2.WSGIApplication([('/new', new)],debug=True)