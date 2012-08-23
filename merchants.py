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
from gaesessions import get_current_session

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MerchantsHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('templates/merchants.html')
		self.response.out.write(template.render())

class LoginHandler(webapp2.RequestHandler):
	def get(self):
		pass
		#in the future, show the login form
	
	def post(self):
		#this is passed when an ajax form is checking the login state
		if self.request.get('type') == 'ajax':
			logging.debug('AJAX CHECK')
			email = self.request.get('email')
			pw = self.request.get('pw')
			
			#check if login is valid
			q = levr.BusinessOwner.gql('WHERE email=:1 AND pw=:2',email,pw)
			if q.get():
				#echo that login was successful
				self.response.out.write(True)
			else:
				#echo that login was not successful
				self.response.out.write(False)
		else:
			logging.debug('AN ACTUAL LOGIN ATTEMPT')
			#check if login is valid
			q = levr.BusinessOwner.gql('WHERE email=:1 AND pw=:2',email,pw)
			if q.get():
				#set session variable to logged in
				session = get_current_session()
				session['loggedIn'] = True
				#redirect to manage page
				self.redirect('/merchants/manage')
			else:
				self.redirect('/login')
	
			
class EmailCheckHandler(webapp2.RequestHandler):
	def post(self):
		'''This is currently a handler to check whether the email entered by a business on signup is available'''
		email = self.request.get('email')
		pw = self.request.get('pw')
		 
		#check if email is already in use
		q = levr.Deal.gql('WHERE email=:1',email)
		if q.get():
			#echo that email is in use
			self.response.out.write(False)
		else:
			#echo that email is available
			self.response.out.write(True)


class WelcomeHandler(webapp2.RequestHandler):
	def get(self):
		try:
			template = jinja_environment.get_template('templates/new.html')
			self.response.out.write(template.render())
		except:
			levr.log_error()
	def post(self):
			#A business owner is signing up in the tour
		try:
			logging.debug(self.request.headers)
			logging.debug(self.request.body)
			logging.debug(self.request.params)
			
			owner_key = levr.BusinessOwner(
				#create owner with contact info, put and get key
				email			= self.request.get('email'),
				pw				= enc.encrypt_password(self.request.get('password')),
				validated		= False
				).put()
			
			business_name = self.request.get('business_name')
			business_key = levr.Business(
				#create business that is child of the owner
				parent			= owner_key,
				business_name	= business_name,
				vicinity		= self.request.get('vicinity'),
				geo_point		= levr.geo_converter(self.request.get('geo_point')),
				types			= self.request.get_all('types[]'),
				validated		= False
				).put()
			
			logging.debug(owner_key)
			logging.debug(business_key)
			
			#creates new session for the new business
			session = get_current_session()
			session['businessID'] 	= enc.encrypt_key(business_key)
			session['loggedIn']		= True
			session['alias']		= business_name
			session['validated']	= False
			
			logging.debug(session)
			#forward to appropriate page
			if self.request.get('destination') == 'upload':
				self.redirect('/merchants/upload')
			elif self.request.get('destination') == 'create':
				self.redirect('/merchants/deal')
		except:
			levr.log_error(self.request.body)

class DealHandler(webapp2.RequestHandler):
	def get(self):
		try:
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
		except:
			levr.log_error()
class DealUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		try:
			levr_utils.dealCreate(self, 'web')
			self.redirect('/merchants/manage')
		except:
			levr.log_error(self.request.body)
class DeleteDealHandler(webapp2.RequestHandler):
	def get(self):
		try:
			logging.debug(self.request)
			dealID = self.request.get('id')
			dealID = enc.decrypt_key(dealID)
			db.delete(dealID)
			
			self.redirect('/merchants/manage')
		except:
			levr.log_error()
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
			self.redirect('/merchants/manage')
		except:
			levr.log_error(self.request.body)
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
								('/merchants/emailCheck', EmailCheckHandler),
								('/merchants/welcome', WelcomeHandler),
								('/merchants/deal', DealHandler),
								('/merchants/deal/upload', DealUploadHandler),
								('/merchants/deal/delete', DeleteDealHandler),
								('/merchants/editDeal', EditDealHandler),
								('/merchants/editDeal/upload', EditDealUploadHandler),
								('/merchants/manage', ManageHandler),
								('/merchants/upload', UploadHandler),
								('/merchants/widget', WidgetHandler),
								('/merchants/analytics', AnalyticsHandler)
								], debug=True)
