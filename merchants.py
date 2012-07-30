import webapp2
#import json
import logging
import os
import jinja2
import levr_classes as levr
import levr_utils
#from google.appengine.ext import db
#from google.appengine.api import images
#from google.appengine.api import mail
from datetime import datetime
from datetime import timedelta
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class DealHandler(webapp2.RequestHandler):
	def get(self):
		upload_url = blobstore.create_upload_url('/merchants/deal/upload')
		template_values = {
			"upload_url"	: upload_url,
		}
		template = jinja_environment.get_template('templates/deal.html')
		self.response.out.write(template.render(template_values))
	
class DealUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		levr_utils.dealCreate(self,'web')

app = webapp2.WSGIApplication([('/merchants/deal', DealHandler),
								('/merchants/deal/upload', DealUploadHandler)
								],debug=True)