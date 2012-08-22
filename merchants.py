import webapp2
#import json
import logging
import os
import jinja2
import levr_classes as levr
import levr_utils
import levr_encrypt as enc
from levr_encrypt import encrypt_key
#from google.appengine.ext import db
#from google.appengine.api import images
#from google.appengine.api import mail
from datetime import datetime
from datetime import timedelta
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import db

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class DealHandler(webapp2.RequestHandler):
	def get(self):
		#check login
		headerData = levr_utils.loginCheck(self, True)
		#get the business information
		businessID = headerData['businessID']
		businessID = enc.decrypt_key(businessID)
		businessID = db.Key(businessID)
		business = levr.Business.get(businessID)
		#create tags from the business
		tags = business.create_tags()
		
		#create the upload url
		url = '/merchants/deal/upload?uid='+headerData['businessID']
		upload_url = blobstore.create_upload_url(url)
		
		#consolidate the values
		template_values = {
						"tags"			: tags,
						"upload_url"	: upload_url,
						"deal"			: None,
						"business"		: business
		}
		template = jinja_environment.get_template('templates/deal.html')
		self.response.out.write(template.render(template_values))
	
class DealUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		levr_utils.dealCreate(self, 'web')
		#redirect
class EditDealHandler(webapp2.RequestHandler):
	def get(self):
		try:
			headerData = levr_utils.loginCheck(self, True)
			logging.debug(headerData)
			#fetch business
			businessID = headerData['businessID']
			logging.debug(headerData['businessID'])
			businessID = enc.decrypt_key(businessID)
			businessID = db.Key(businessID)
			business = levr.Business.get(businessID)
			
			dealID = self.request.get('id')
			#create upload url before decrypting
			url = '/merchants/editDeal/upload?uid='+headerData['businessID']+'&id='+dealID
			upload_url = blobstore.create_upload_url(url)
			#decrypt id, get and format deal
			dealID = enc.decrypt_key(dealID)
			deal = levr.Deal.get(dealID)
			deal = levr.phoneFormat(deal,'manage')
			
			template_values = {
							"edit"		:True,
							"upload_url":upload_url,
							"deal"		:deal,
							"business"	:business,
							"headerData":headerData
			}
			template = jinja_environment.get_template('templates/deal.html')
			self.response.out.write(template.render(template_values))
		except:
			levr.log_error()
class EditDealUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		try:
			levr_utils.dealCreate(self,'edit')
#			self.redirect('/merchants/manage')
		except:
			self.response.out.write('error')
			levr.log_error()
class ManageHandler(webapp2.RequestHandler):
	def get(self):
		try:
			#Bounce if user is not logged in
			headerData = levr_utils.loginCheck(self, True)
			logging.debug(headerData)
			#fetch business identifier
			businessID = headerData['businessID']
			businessID = enc.decrypt_key(businessID)
			businessID = db.Key(businessID)
			business = levr.Business.get(businessID)
			#get deals that are children of the business, ordered by whether or not they are exclusive or not
			d = levr.Deal.all().ancestor(businessID).order("is_exclusive").fetch(None)
			#get all ninja deals
			d.extend(levr.CustomerDeal.all().filter('businessID =', businessID).fetch(None))
			deals = []
			for deal in d:
				logging.debug('---')
				deals.append(levr.phoneFormat(deal, 'manage'))
			
			logging.debug(deals)
			
			
			template_values = {
				'headerData' : headerData,
				'title' : 'Manage',
				'business': business,
				'deals'	: deals
			}
			logging.debug(template_values)
			
			template = jinja_environment.get_template('templates/manageOffers.html')
			self.response.out.write(template.render(template_values))
		except:
			levr.log_error()

class EmailHandler(webapp2.RequestHandler):
	def get(self):
		try:
			template_values = {}
			template = jinja_environment.get_template('templates/emailUpload.html')
			self.response.out.write(template.render(template_values))
		except:
			levr.log_error()
class WidgetHandler(webapp2.RequestHandler):
	def get(self):
		try:
			template_values = {}
			template = jinja_environment.get_template('templates/manageWidget.html')
			self.response.out.write(template.render(template_values))
		except:
			levr.log_error()
class AnalyticsHandler(webapp2.RequestHandler):
	def get(self):
		try:
			template_values = {}
			template = jinja_environment.get_template('templates/analytics.html')
			self.response.out.write(template.render(template_values))
		except:
			levr.log_error()
app = webapp2.WSGIApplication([('/merchants/deal', DealHandler),
								('/merchants/deal/upload', DealUploadHandler),
								('/merchants/editDeal', EditDealHandler),
								('/merchants/editDeal/upload', EditDealUploadHandler),
								('/merchants/manage', ManageHandler),
								('/merchants/email', EmailHandler),
								('/merchants/widget', WidgetHandler),
								('/merchants/analytics', AnalyticsHandler)
								], debug=True)
