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
			logging.debug(self.request.body)
			logging.debug(self.request.get('image'))
			
			#init tags list
			tags = []
			
			full_address = self.request.get('business_select')
			#split address by commas
			split_address = full_address.split(',')
			#remove whitespace on beginning and end of each element
			split_address 	= [x.strip() for x in split_address]
			logging.debug(split_address)
			business_name 	= split_address[0]
			tags.extend(levr.tagger(business_name))

			#will have the businessID upon login
			##### spoof value
			businessID = ''
	#		##### /spoof
			#grab the business or create a new one
			business = levr.Business.gql('WHERE business_name = :1',business_name).get()
			if not business:
				business = levr.Business()
			#give the business its address values
			#need geo point and zip code
			business.put()
			
			
			#create the deal entity
			deal 	= levr.Deal()#parent=businessID)
			upload	= self.get_uploads()[0]
			blob_key= upload.key()
			deal.img= blob_key
			
			#parse description into tags
			desc	= self.request.get('deal_description')
			tags.extend(levr.tagger(desc))
			deal.description = desc
			
			
			#parse deal text into tags
			deal_text	= self.request.get('deal_line1')
			tags.extend(levr.tagger(deal_text))
			deal.deal_text = deal_text
			
			#check existence of secondary name and parse
			secondary_name	= self.request.get('deal_line2')
			if secondary_name:
				deal.deal_type = "bundle"
				tags.extend(levr.tagger(secondary_name))
				deal.secondary_name = secondary_name
			else:
				deal.deal_type = "single"
			
			
			deal.businessID		= business.key().__str__()
			deal.business_name 	= business_name
			deal.date_start		= datetime.now()
			deal.deal_status	= "active"
			deal.address_string = full_address
			deal.tags			= tags
			
			logging.debug(tags)
			logging.debug(deal)
			logging.debug(business)
			deal.put()
			business.put()
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