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

class MerchantsHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('templates/merchants.html')
		self.response.out.write(template.render())

class LoginHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('templates/merchants.html')
		self.response.out.write(template.render())


class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('templates/new.html')
		self.response.out.write(template.render())
		
	def post(self):
		#build the business object
		business = levr.Business()
		business.business_name = self.request.get('business_name')
		business.vicinity = self.request.get('vicinity')
		business.geo_point = self.request.get('geo_point')
		business.types = self.request.get('types')
		
		logging.info('SOMETHING HAS HAPPENED')
		logging.info(business.types)
		
		#forward to appropriate page
		if self.request.get('destination') == 'upload':
			self.redirect('/merchants/upload')
		elif self.request.get('destination') == 'create':
			self.redirect('/merchants/deal')
	

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
		levr_utils.dealCreate(self, 'web')
		#redirect
class EditDealHandler(webapp2.RequestHandler):
	def get(self):
		try:
			headerData = levr_utils.loginCheck(self, True)
			
			dealID = self.request.get('id')
			#create upload url before decrypting
			upload_url = blobstore.create_upload_url('/merchants/editDeal/upload?id='+dealID)
			dealID = enc.decrypt_key(dealID)
			
			deal = levr.Deal.get(dealID)
			deal = levr.phoneFormat(deal,'manage')
			logging.debug(deal)
			
			template_values = {
							"edit"		:True,
							"upload_url":upload_url,
							"deal"		:deal,
#							"business"	:business,
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
			
		except:
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
			#get deals that are children of the business, ordered by whether or not they are exclusive or not
			d = levr.Deal.all().ancestor(businessID).order("is_exclusive").fetch(None)
			#get all ninja deals
			d.extend(levr.CustomerDeal.all().filter('businessID =', businessID).fetch(None))
			deals = []
			for deal in d:
				logging.debug('---')
				deals.append(levr.phoneFormat(deal, 'manage'))
			
			logging.debug(deals)
			business = levr.Business.get(businessID)
			
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

class UploadHandler(webapp2.RequestHandler):
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
app = webapp2.WSGIApplication([('/merchants', MerchantsHandler),
								('/merchants/login', LoginHandler),
								('/merchants/welcome', WelcomeHandler),
								('/merchants/deal', DealHandler),
								('/merchants/deal/upload', DealUploadHandler),
								('/merchants/editDeal', EditDealHandler),
								('/merchants/editDeal/upload', EditDealUploadHandler),
								('/merchants/manage', ManageHandler),
								('/merchants/upload', UploadHandler),
								('/merchants/widget', WidgetHandler),
								('/merchants/analytics', AnalyticsHandler)
								], debug=True)
