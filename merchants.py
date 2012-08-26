import webapp2
#import json
import logging
import os
import jinja2
import levr_classes as levr
import levr_utils
import levr_encrypt as enc
#from levr_encrypt import encrypt_key
#from google.appengine.ext import db
#from google.appengine.api import images
from google.appengine.api import mail
#from datetime import datetime
#from datetime import timedelta
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from google.appengine.ext import db
from gaesessions import get_current_session

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MerchantsHandler(webapp2.RequestHandler):
	def get(self):
		#check if logged in. if so, redirect to the manage page
		session = get_current_session()
		if session.has_key('loggedIn') == True and session['loggedIn'] == True:
			self.redirect("/merchants/manage")
		else:
			template = jinja_environment.get_template('templates/merchants.html')
			self.response.out.write(template.render())

class LoginHandler(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('templates/login.html')
		self.response.out.write(template.render())
	
	def post(self):
		try:
			#this is passed when an ajax form is checking the login state
			email = self.request.get('email')
			pw = enc.encrypt_password(self.request.get('pw'))
			
			if self.request.get('type') == 'ajax':
				logging.debug('AJAX CHECK')
	
				#check if login is valid
				q = levr.BusinessOwner.gql('WHERE email =:1 AND pw =:2', email, pw)
				if q.get():
					#echo that login was successful
					self.response.out.write(True)
				else:
					#echo that login was not successful
					self.response.out.write(False)
			else:
				#Normal login attempt. Redirects to manage or the login page
				email = self.request.get('email')
#				email = db.Email(email)
				pw = enc.encrypt_password(self.request.get('pw'))
				logging.debug(email)
				logging.debug(pw)
				
				if email == None:
					email = ''
				if pw == None:
					pw = ''
				
				#the required text fields were entered
				#query database for matching email and pw
				owner = levr.BusinessOwner.all().filter('email =', email).filter('pw =', pw).get()
				#search for owner
				logging.debug(owner)
				if owner != None:
					logging.debug('owner exists... login')
					#owner exists in db, and can login
					session = get_current_session()
					session['ownerID'] = enc.encrypt_key(owner.key())#business.key())
					session['loggedIn'] = True
					session['validated'] = owner.validated
					self.redirect('/merchants/manage')
				else:
					#show login page again - login failed
					template = jinja_environment.get_template('templates/login.html')
					self.response.out.write(template.render())
		except:
			levr.log_error()
			
class EmailCheckHandler(webapp2.RequestHandler):
	def post(self):
		'''This is currently a handler to check whether the email entered by a business on signup is available'''
		email = self.request.get('email')
		#pw = enc.encrypt_password(self.request.get('pw'))
		 
		#check if email is already in use
		q = levr.BusinessOwner.gql('WHERE email=:1', email)
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
				email			=self.request.get('email'),
				pw				=enc.encrypt_password(self.request.get('password')),
				validated		=False
				).put()
			logging.debug(owner_key)
			
			business_name = self.request.get('business_name')
			business_key = levr.Business(
				#create business
				owner			=owner_key,
				business_name	=business_name,
				vicinity		=self.request.get('vicinity'),
				geo_point		=levr.geo_converter(self.request.get('geo_point')),
				types			=self.request.get_all('types[]'),
				validated		=False
				).put()
			
			logging.debug(business_key)
			
			#creates new session for the new business
			session = get_current_session()
			session['ownerID']	= enc.encrypt_key(owner_key)
			session['loggedIn']	= True
			session['validated']= False
			logging.debug(session)


			#send email to pat so that he will know that there is a new business.
			message = mail.EmailMessage(
				sender	="LEVR AUTOMATED <patrick@levr.com>",
				subject	="New Merchant signup",
				to		="patrick@levr.com")
			logging.debug(message)
			body = 'New merchant\n\n'
			body += 'Business: '  +str(business_name)+"\n\n"
			body += 'Business ID: '+str(business_key)+"\n\n"
			body += "Owner Email:"+str(self.request.get('email'))+"\n\n"
			message.body = body
			message.send()


			#forward to appropriate page
			if self.request.get('destination') == 'upload':
				self.redirect('/merchants/upload')
			elif self.request.get('destination') == 'create':
				self.redirect('/merchants/deal')
		except:
			levr.log_error(self.request.body)

class DealHandler(webapp2.RequestHandler):
	def get(self):
		'''This is the deal upload page'''
		try:
			#check login
			headerData = levr_utils.loginCheck(self, True)
			logging.debug(headerData)
			#get the owner information
			ownerID = headerData['ownerID']
			ownerID = enc.decrypt_key(ownerID)
			ownerID = db.Key(ownerID)
			owner = levr.BusinessOwner.get(ownerID)
			logging.debug(owner)
			
			#get the business
			business = owner.businesses.get()#TODO: this will be multiple businesses later
			
			#create tags from the business
			tags = business.create_tags()
			
			#create the upload url
			url = '/merchants/deal/upload?uid=' + headerData['ownerID'] + '&business=' + enc.encrypt_key(business.key())
			logging.debug(url)
			upload_url = blobstore.create_upload_url(url)
			
			#consolidate the values
			template_values = {
							"tags"			: tags,
							"upload_url"	: upload_url,
							"deal"			: None,
							"business"		: business, #TODO need to grab multiple businesses later
							"owner"			: owner
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
			#check login
			headerData = levr_utils.loginCheck(self, True)
			
			#get the owner information
			ownerID = headerData['ownerID']
			ownerID = enc.decrypt_key(ownerID)
			ownerID = db.Key(ownerID)
			owner = levr.BusinessOwner.get(ownerID)
			logging.debug(owner)
			
			#get the business
			business = owner.businesses.get()#TODO: this will be multiple businesses later
			
			#get deal
			dealID = self.request.get('id')
			
			
			#create upload url BEFORE DECRYPTING
			url = '/merchants/editDeal/upload?uid=' + headerData['ownerID'] + '&business='+ enc.encrypt_key(business.key()) +'&deal=' + dealID
			upload_url = blobstore.create_upload_url(url)
			
			
			#decrypt id, get and format deal
			dealID = enc.decrypt_key(dealID)
			deal = levr.Deal.get(dealID)
			deal = levr.phoneFormat(deal, 'manage')
			
			template_values = {
							"edit"		:True,
							"upload_url":upload_url,
							"deal"		:deal,
							"owner"		:owner,
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
			levr_utils.dealCreate(self, 'edit')
			self.redirect('/merchants/manage')
		except:
			levr.log_error(self.request.body)
class ManageHandler(webapp2.RequestHandler):
	def get(self):
		try:
			#check login
			headerData = levr_utils.loginCheck(self, True)
			
			#get the owner information
			ownerID = headerData['ownerID']
			ownerID = enc.decrypt_key(ownerID)
			ownerID = db.Key(ownerID)
			owner = levr.BusinessOwner.get(ownerID)
			logging.debug(owner)
			
			#get the business
			business = owner.businesses.get()#TODO: this will be multiple businesses later
			
			
			#get all deals that are children of the owner ordered by whether or not they are exclusive or not
			d = levr.Deal.all().ancestor(ownerID).order("is_exclusive").fetch(None)
			logging.debug(d)
			#get all ninja deals
			#this doesnt work
#			d.extend(levr.CustomerDeal.all().filter('businessID =', businessID).fetch(None))
			
			#package deals - mostly for getting the correct urls
			deals = []
			for deal in d:
				logging.debug('---')
				deals.append(levr.phoneFormat(deal, 'manage'))
			
			logging.debug(deals)
			
			
			template_values = {
				'headerData':headerData,
				'title'		:'Manage',
				'owner'		:owner,
				'business'	:business,
				'deals'		:deals
			}
			logging.debug(template_values)
			
			template = jinja_environment.get_template('templates/manageOffers.html')
			self.response.out.write(template.render(template_values))
		except:
			levr.log_error()

class UploadHandler(webapp2.RequestHandler):
	def get(self):
		'''This is for the page where they see info about how to upload via email'''
		try:
			template_values = {}
			template = jinja_environment.get_template('templates/emailUpload.html')
			self.response.out.write(template.render(template_values))
		except:
			levr.log_error()
class WidgetHandler(webapp2.RequestHandler):
	def get(self):
		'''The page where they view info about the widget'''
		try:
			headerData = levr_utils.loginCheck(self, True)
			logging.debug(headerData)
			
			ownerID = headerData['ownerID']
			ownerID = enc.decrypt_key(ownerID)
			logging.debug(ownerID)
			businessID	= levr.Business.all(keys_only=True).filter('owner = ',db.Key(ownerID)).get()
			logging.debug(businessID)
			businessID	= enc.encrypt_key(businessID)
			template_values = {
				'businessID'	: businessID
			}
			template = jinja_environment.get_template('templates/manageWidget.html')
			self.response.out.write(template.render(template_values))
		except:
			levr.log_error()
class MyAccountHandler(webapp2.RequestHandler):
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
								('/merchants/myAccount', MyAccountHandler)
								], debug=True)
