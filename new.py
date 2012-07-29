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

class NewDealHandler(webapp2.RequestHandler):
	def get(self):
		upload_url = blobstore.create_upload_url('/new/upload')
		template_values = {
			"upload_url"	: upload_url,
		}
		template = jinja_environment.get_template('templates/deal.html')
		self.response.out.write(template.render(template_values))
	
class NewDealUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		try:
			logging.debug(self.request.headers)
			logging.debug(self.request.body)
			logging.debug(self)
			logging.debug(dir(self))
			logging.debug(self.get_uploads())
			
			full_address = self.request.get('business_select')
			#split address by commas
			split_address = full_address.split(',')
			#remove whitespace on beginning and end of each element
			split_address 	= [x.strip() for x in split_address]
			business_name 	= split_address[0]
			address_line1 	= split_address[1]
			city			= split_address[2]
			state			= split_address[3]
			zip_code		= ''
		
		
			#will have the businessID upon login
			##### spoof value
			businessID = ''
	#		##### /spoof
			#grab the business or create a new one
			business = levr.Business.gql('WHERE business_name = :1',business_name).get()
			if not business:
				business = levr.Business()
			#give the business its address values
			business.business_name 	= business_name
			business.address_line1	= address_line1
			business.city			= city
			business.state			= state
			business.zip_code		= zip_code
			#need geo point and zip code
			
			
			
			#create the deal entity
			deal = levr.Deal()#parent=businessID)
			upload	= self.get_uploads()[0]
			blob_key= upload.key()
			deal.img= blob_key
			deal.description= self.request.get('deal_description')
			
			deal.deal_text	= self.request.get('deal_line1')
			
			secondary_name	= self.request.get('deal_line2')
			if secondary_name:
				deal.deal_type = "bundle"
				deal.secondary_name = secondary_name
			else:
				deal.deal_type = "single"
			
			deal.businessID		= business.key()
			deal.business_name 	= business_name
			deal.date_start		= datetime.now()
			deal.deal_status	= "active"
			deal.address_string = full_address
			
			
			logging.debug(deal)
			logging.debug(business)
			deal.put()
			business.put()
			self.response.set_status(200)
			self.response.out.write('we good.')
		
	#		
	#		deal. deal_line1
	#		deal_line2
	#		deal_description
	#		business_select
		except:
			levr.log_error()
			self.response.set_status(500)
			self.response.out.write('exception')
			
	

app = webapp2.WSGIApplication([('/new', NewDealHandler),
								('/new/upload', NewDealUploadHandler)
								],debug=True)
