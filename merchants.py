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
		action = self.request.get('action')
		success	= self.request.get('success')
		
		logging.debug(action)
		logging.debug(action)
		template_values = {
						'action'	: action,
						'success'	: success
		}
		template = jinja_environment.get_template('templates/login.html')
		self.response.out.write(template.render(template_values))
#		self.response.out.write(os.path.dirname(__file__))
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
					template_values = {
					'success'		: False,
					'email'			: email
					}
					template = jinja_environment.get_template('templates/login.html')
					self.response.out.write(template.render(template_values))
#					self.response.out.write(template_values)
		except:
			levr.log_error()

class LostPasswordHandler(webapp2.RequestHandler):
	'''presents form to user to enter in their email. email is sent to user
	to rest the password'''
	
	def post(self):
		'''input:user email
		output: success, sends email to email account'''
		try: 
			user_email = self.request.get('email')
			user = levr.BusinessOwner.all().filter('email =', user_email).get()
			logging.debug(user)
			if not user:
				logging.debug('flag not user')
				self.redirect('/merchants/login?action=password?success=false')
			else:
				logging.debug('flag is user')
				#send mail to the admins to notify of new pending deal
				url = levr_utils.URL+'/merchants/password/reset?id=' + enc.encrypt_key(user.key())
				logging.info(url)
				try:
					mail.send_mail(sender	="Lost Password<password@levr.com>",
									to		="Patrick Walsh <patrick@getlevr.com>",
									subject	="New pending deal",
									body	="""
									Follow this link to reset your password:
									%s
									""" % url).send()
					logging.debug(url)
#					sent = True
				except:
#					sent = False
					logging.error('mail not sent')
					self.redirect('/merchants/login?action=password&success=false')
					#TODO: add parameter to login that shows it was not a success because the email was not sent
				else:
#					template_values={"sent":sent}
					self.redirect('/merchants/login?')
		except:
			levr.log_error()
		
class ResetPasswordHandler(webapp2.RequestHandler):
	'''User enters in a new password twice'''
	def get(self):
		try:
			'''Template has uid in url to identify them'''
			
			uid = self.request.get('id')
			#If a false attempt has been made, success will be false, otherwise true
			try:
				success = self.request.get('success')
			except:
				success = 'True'
			
			
			template_values = {
							"success"	:success,
							"uid"		:uid,
							"action"	:'reset'
							}
				
			template = jinja_environment.get_template('templates/login.html')
			self.response.out.write(template.render(template_values))
		except:
			levr.log_error()
	def post(self):
		'''Resets password on the database'''
		try:
			password1 = self.request.get('newPassword1')
			password2 = self.request.get('newPassword2')
			uid = self.request.get('id')
			uid = enc.decrypt_key(uid)
			
			if password1 == password2:
				#passwords match
				logging.debug('flag password success')
				encrypted_password = enc.encrypt_password(password1)
				logging.debug(uid)
				owner = levr.BusinessOwner.get(uid)
				owner.pw = encrypted_password
				owner.put()
				
				#log user in and redirect them to merchants/manage
				session = get_current_session()
				session['ownerID'] = enc.encrypt_key(owner.key())#business.key())
				session['loggedIn'] = True
				session['validated'] = owner.validated
				self.redirect('/merchants/manage')
				
			else:
				#passwords do not match
				self.redirect('/merchants/password/reset?id=%s&success=False' % enc.encrypt_key(uid))
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
			logging.debug('!!!!!!')
			logging.info('asdasd')
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
			
			owner = levr.BusinessOwner(
				#create owner with contact info, put and get key
				email			=self.request.get('email'),
				pw				=enc.encrypt_password(self.request.get('password')),
				validated		=False
				).put()
			logging.debug(owner)
			
			#get the business info from the form
			business_name	= self.request.get('business_name')
			geo_point		= levr.geo_converter(self.request.get('geo_point'))
			vicinity		= self.request.get('vicinity')
			types			= self.request.get_all('types[]')
			
			#parse business name to create an upload email
			logging.debug(business_name)
			name_str = levr.tagger(business_name)
			logging.debug(name_str)
			#create unique identifier for the business
			if name_str[0] == 'the' or name_str[0] == 'a' or name_str[0] == 'an':
				#dont like the word the in front
				logging.debug('flag the!')
				identifier = ''.join(name_str[1:3])
			else:
				identifier = ''.join(name_str[:2])
			upload_email = "u+"+identifier+"@levr.com"
			
			#check if that already exists
			num = levr.Business.all().filter('upload_email =',upload_email).count()
			
			logging.debug(num)
			if num != 0:
				#a business already exists with that upload email
				#increment the 
				upload_email = "u+"+identifier+str(num)+"@levr.com"
			
			logging.debug(upload_email)
			
			#check if business exists in database
			business = levr.Business.all().filter('business_name =', business_name).filter('vicinity =',vicinity).get()
			logging.debug(business)
			
			if business:
				logging.debug(levr_utils.log_model_props(business))
				logging.debug('flag business already exists')
				#have to delete business entity instead of update because gae wont update reference on owner entity
				if business.owner == None:
					#grab this business! 
					business.owner	= owner
					upload_email	= upload_email
					#TODO targeted will be set to false in the future, removing signed businesses from the ninja pool
#					targeted		= False
				else:
#					db.delete(business)
					logging.error('A business owner just signed up claiming a business that another person has claimed')
			else:
				logging.debug('flag business does not exist')
			
				#create business entity
				business = levr.Business(
					#create business
					owner			=owner,
					business_name	=business_name,
					vicinity		=vicinity,
					geo_point		=geo_point,
					types			=types,
					upload_email	=upload_email
					#TODO targeted will be set to false in the future, removing signed businesses from the ninja pool
#					targeted		=False
					)
			logging.debug(levr_utils.log_model_props(business))
			business.put()
			
			#creates new session for the new business
			session = get_current_session()
			session['ownerID']	= enc.encrypt_key(owner)
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
			body += 'Business ID: '+str(business)+"\n\n"
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
			#A merchant is creating a NEW deal from the online form
			
			#make sure than an image is uploaded
			logging.debug(self.get_uploads())
			if self.get_uploads(): #will this work?
				upload	= self.get_uploads()[0]
				blob_key= upload.key()
				img_key = blob_key
			else:
				raise Exception('Image was not uploaded')
			
			params = {
					'uid'				:self.request.get('uid'),
					'business'			:self.request.get('business'),
					'deal_description'	:self.request.get('deal_description'),
					'deal_line1'		:self.request.get('deal_line1'),
					'deal_line2'		:self.request.get('deal_line2'),
					'img_key'			:img_key
					}
			levr_utils.dealCreate(params, 'merchant_create')
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
			#A merchant is EDITING a deal from the online form
			logging.debug(self.request.params)
			
			#make sure than an image is uploaded
			logging.debug(self.get_uploads())
			if self.get_uploads().__len__()>0: #will this work?
				#image has been uploaded
				upload_flag = True
				upload	= self.get_uploads()[0]
				blob_key= upload.key()
				img_key = blob_key
			else:
				#image has not been uploaded
				upload_flag = False
				img_key = ''
			logging.debug('upload_flag: '+str(upload_flag))
			params = {
					'uid'				:self.request.get('uid'),
					'business'			:self.request.get('business'),
					'deal'				:self.request.get('deal'),
					'deal_description'	:self.request.get('deal_description'),
					'deal_line1'		:self.request.get('deal_line1'),
					'deal_line2'		:self.request.get('deal_line2'),
					'img_key'			:img_key
					}
			
			levr_utils.dealCreate(params, 'merchant_edit',upload_flag)
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
#			d = levr.Deal.all().ancestor(ownerID).order("is_exclusive").fetch(None)
#			logging.debug(d)
			#get all ninja deals
			d = levr.Deal().all().filter('businessID =', str(business.key())).fetch(None)
#			d += ninja_deals
			#package deals - mostly for getting the correct urls
			deals = []
			for deal in d:
				logging.debug('-----------')
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
			#check login
			headerData = levr_utils.loginCheck(self, True)
			
			#get the owner information
			ownerID = headerData['ownerID']
			ownerID = enc.decrypt_key(ownerID)
			ownerID = db.Key(ownerID)
			owner = levr.BusinessOwner.get(ownerID)
			logging.debug(owner)
			if not owner:
				self.redirect('/merchants')
			
			#get the business
			business = owner.businesses.get()#TODO: this will be multiple businesses later
			
			
			template_values = {
				'headerData':headerData,
				'title'		:'Upload Instructions',
				'owner'		:owner,
				'business'	:business
			}
			
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
			
			template_values = {
				'owner'		: owner,
				'business'	: business,
				'mode'		: '', #which form to show
				'error'		: ''
				}
				
			template = jinja_environment.get_template('templates/editAccount.html')
			self.response.out.write(template.render(template_values))
		except:
			levr.log_error()
	def post(self):
		try:
			logging.debug(self.request.headers)
			logging.debug(self.request.body)
			logging.debug(self.request.params)
			
			#check login
			headerData = levr_utils.loginCheck(self, True)
			
			#get the owner information
			ownerID = headerData['ownerID']
			ownerID = enc.decrypt_key(ownerID)
			ownerID = db.Key(ownerID)
			owner = levr.BusinessOwner.get(ownerID)
			logging.debug(owner)
			
			password = enc.encrypt_password(self.request.get('old_password'))
			mode = self.request.get('change')
			logging.debug(owner.pw == password)
			if owner.pw == password:
				
				#password is correct
				
				if mode == 'email':
					#user is changing their email
					
					email			= self.request.get('new_email')
					confirm_email	= self.request.get('confirm_new_email')
					if email == confirm_email:
						logging.debug(email)
						#emails match - change owner email
						owner.email = email
						owner.put()
						self.redirect('/merchants/myAccount?success=true')
					else:
						#get the business
						business = owner.businesses.get()#TODO: this will be multiple businesses later
						
						template_values = {
						'owner'		: owner,
						'business'	: business,
						'mode'		: mode, #which form to show
						'error'		: 'confirm_new_email'
						}
						logging.debug(template_values)
						#password is incorrect
						template = jinja_environment.get_template('templates/editAccount.html')
						self.response.out.write(template.render(template_values))
					
				elif mode == 'password':
					#user is changing their password
					new_password		= self.request.get('new_password')
					confirm_new_password= self.request.get('confirm_new_password')
					
					if new_password == confirm_new_password:
						logging.debug(new_password)
						#passwords match - change owner password
						owner.pw = new_password
						owner.put()
						self.redirect('/merchants/myAccount?success=true')
					else:
						#new passwords do not match
						#get the business
						business = owner.businesses.get()#TODO: this will be multiple businesses later
						
						template_values = {
						'owner'		: owner,
						'business'	: business,
						'mode'		: mode, #which form to show
						'error'		: 'confirm_new_password'
						}
				
						#password is incorrect
						template = jinja_environment.get_template('templates/editAccount.html')
						self.response.out.write(template.render(template_values))
				else:
					#mode not recognized
					logging.error('mode not recognized')
			else:
				#old password is incorrect
				#get the business
				business = owner.businesses.get()#TODO: this will be multiple businesses later
				
				template_values = {
				'owner'		: owner,
				'business'	: business,
				'mode'		: mode, #which form to show
				'error'		: 'old_password'
				}
				
				logging.debug(template_values)
				template = jinja_environment.get_template('templates/editAccount.html')
				self.response.out.write(template.render(template_values))
		except:
			levr.log_error(self.request.headers)
			
class CheckPasswordHandler(webapp2.RequestHandler):
	def post(self):
		try:
			logging.debug(self.request.headers)
			logging.debug(self.request.body)
			logging.debug(self.request.params)
			
			#check login
			headerData = levr_utils.loginCheck(self, True)
			
			#get the owner information
			ownerID = headerData['ownerID']
			ownerID = enc.decrypt_key(ownerID)
			ownerID = db.Key(ownerID)
			owner = levr.BusinessOwner.get(ownerID)
			logging.debug(owner)
			
			password = enc.encrypt_password(self.request.get('password'))
			if owner.pw == password:
				self.response.out.write(True)
			else:
				self.response.out.write(False)
			
		except:
			levr.log_error()
app = webapp2.WSGIApplication([('/merchants', MerchantsHandler),
								('/merchants/', MerchantsHandler),
								('/merchants/login', LoginHandler),
								('/merchants/password/lost', LostPasswordHandler),
								('/merchants/password/reset', ResetPasswordHandler),
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
								('/merchants/myAccount', MyAccountHandler),
								('/merchants/myAccount/checkPassword', CheckPasswordHandler)
								], debug=True)
