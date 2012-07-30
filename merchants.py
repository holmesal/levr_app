import webapp2
#import json
import logging
import os
import jinja2
import levr_classes as levr
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
		try:
			logging.debug(self.request.headers)
			logging.info(self.request.body)
			logging.debug(self.request.get('image'))
			
			#init tags list
			tags = []
			
			#vicinity
			vicinity = self.request.get('vicinity')
			tags.extend(levr.tagger(vicinity))
			logging.info(tags)
			
			#types
			types = self.request.get('types')
			tags.extend(levr.tagger(types))
			logging.info(tags)
			
			#deal line 1
			deal_text	= self.request.get('deal_line1')
			tags.extend(levr.tagger(deal_text))
			logging.info(tags)
			
			#deal line 2
			secondary_name = self.request.get('deal_line2')
			tags.extend(levr.tagger(secondary_name))
			logging.info(tags)
			
			#description
			description = self.request.get('deal_description')
			tags.extend(levr.tagger(description))
			logging.info(tags)
			
			#business name
			business_name = self.request.get('business_name')
			tags.extend(levr.tagger(business_name))
			logging.info(tags)
			
			#geo point
			#geo_point = self.request.get('geo_point')
			#logging.info(geo_point)
			
			
			#check if business exists
			#business = levr.Business.gql("WHERE business_name=:1 and geo_point=:2", business_name, geo_point).get()
			business = levr.Business.gql("WHERE business_name=:1", business_name).get()
			#if a business doesn't exist in db, then create a new one
			if not business:
				business = levr.Business()
			#add data
			business.business_name 	= business_name
			business.vicinity 		= vicinity
			#business.geo_pt			= self.request.get('geo_pt')
			
			#put business
			business.put()
			
			
			#create the deal entity
			deal 	= levr.Deal(parent=business.key())
			upload	= self.get_uploads()[0]
			blob_key= upload.key()
			deal.img= blob_key
			
			#add the data
			deal.deal_text 			= deal_text
			deal.description 		= description
			deal.business_name		= business_name
			deal.businessID			= business.key().__str__()
			deal.vicinity			= vicinity
			deal.tags				= tags
			deal.date_start			= datetime.now()
			deal.deal_status		= "active"
			deal.date_end			= datetime.now() + timedelta(days=7)
			#secondary_name
			if secondary_name:
				deal.deal_type = "bundle"
				tags.extend(levr.tagger(secondary_name))
				deal.secondary_name = secondary_name
			else:
				deal.deal_type = "single"
			
			#put the deal
			deal.put()
			
			self.response.set_status(200)
			self.response.out.write('we good.')
			self.redirect('/new')
		except:
			levr.log_error()
			self.response.set_status(500)
			self.response.out.write('exception')

app = webapp2.WSGIApplication([('/merchants/deal', DealHandler),
								('/merchants/deal/upload', DealUploadHandler)
								],debug=True)