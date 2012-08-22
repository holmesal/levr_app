#import webapp2
#import os
import logging
#import jinja2
import levr_classes as levr
import levr_encrypt as enc
from datetime import datetime
from datetime import timedelta
from google.appengine.ext import blobstore
from google.appengine.ext import db
#from google.appengine.ext.webapp import blobstore_handlers

from gaesessions import get_current_session

def loginCheck(self,strict):
	'''This is a general-purpose login checking function
	   in "strict" mode (strict=True), this script will bounce to the login page if not logged in
	   if strict=False, headers will be returned that indicate the user isn't logged in, but no bouncing'''
	session = get_current_session()
	logging.info(session)
	if session.has_key('loggedIn') == False or session['loggedIn'] == False:
		if strict == True:
			#not logged in, bounce to login page
			logging.info('Not logged in. . .Bouncing!')
			self.redirect('/login')
		else:
			logging.info('Not logged in. . .Sending back headerData')
			headerData = {
				'loggedIn'	: False
			}
			return headerData
	elif session.has_key('loggedIn') == True and session['loggedIn'] == True:
		#logged in, grab the useful bits
		#this is a hack. . . forgive meeee
		try:
			uid = session['businessID']
		except:
			uid = session['uid']
		
		headerData = {
			'loggedIn'		: session['loggedIn'],
			'alias' 		: session['alias'],
			'businessID'	: uid
			}
		#return user metadata.
		return headerData
		#return session['businessID']
	return

def signupCustomer(email,alias,pw):
	pw = enc.encrypt_password(pw)
	'''Check availability of username+pass, create and login if not taken'''
	#check availabilities
	q_email = levr.Customer.gql('WHERE email = :1',email)
	q_alias  = levr.Customer.gql('WHERE alias = :1',alias)
	r_email = q_email.get()
	r_alias = q_alias.get()
	
	if r_email == None and r_alias == None: #nothing found
		c = levr.Customer()
		c.email = email
		c.pw = pw
		c.alias = alias
		#put
		c.put()
		return {'success':True,'uid':enc.encrypt_key(c.key().__str__())}
	elif r_email != None:
		return {
			'success': False,
			'field': 'email',
			'error': 'That email is already registered. Try again!'
		}
	elif r_alias != None:
		return {
			'success': False,
			'field': 'alias',
			'error': 'That username is already registered. Try again!'
		}
		
def loginCustomer(email_or_owner,pw):
	'''This is passed either an email or a username, so check both'''
	logging.info(pw)
	pw = enc.encrypt_password(pw)
	logging.info(pw)
	logging.info(email_or_owner)
	q_email = levr.Customer.gql('WHERE email = :1 AND pw=:2',email_or_owner,pw)
	q_owner  = levr.Customer.gql('WHERE alias = :1 AND pw=:2',email_or_owner,pw)
	r_email = q_email.get()
	r_owner = q_owner.get()
	if r_email != None:
		#found user on the basis of email
		return {
			'success'		: True,
			'uid'			: enc.encrypt_key(r_email.key().__str__()),
			'notifications'	: r_email.get_notifications()
		}
	elif r_owner != None:
		#found user on the basis of username
		return {
			'success'		: True,
			'uid'			: enc.encrypt_key(r_owner.key().__str__()),
			'notifications'	: r_owner.get_notifications()
		}
	else:
		return {
			'success'	: False,
			'error': 'Incorrect username, email, or password. Please try again!'
		}

def dealCreate(self,origin):
	'''pass in "self"'''
	logging.debug(self.request.headers)
	logging.debug(self.request.body)
	logging.debug(self.request.get('image'))
	
	#init tags list
	tags = []
	
	#==== business stuff ====#
	if origin != 'edit':
		#this excludes the case where the deal is being edited by the business
		#in that case, the business information doesn't need to be updated, nor is it passed to the function
		
		#check if business exists - get businessID
		business= levr.Business.gql("WHERE business_name=:1 and geo_point=:2", business_name, geo_point).get()
		
		if not business:
			#if a business doesn't exist in db, then create a new one
			business = levr.Business()
			
			#business name
			business_name = self.request.get('business_name')
			tags.extend(levr.tagger(business_name))
			logging.info(tags)
			
			#geo point
			geo_point = self.request.get('geo_point')
			logging.debug(geo_point)
			geo_point = levr.geo_converter(geo_point)
			logging.debug(geo_point)
			
			#vicinity
			vicinity = self.request.get('vicinity')
			tags.extend(levr.tagger(vicinity))
			logging.info(tags)
			
			#types
			types = self.request.get('types')
			tags.extend(levr.tagger(types))
			logging.info(tags)
			
			#add data
			business.business_name 	= business_name
			business.vicinity 		= vicinity
			business.geo_point		= geo_point
			business.tags			= tags
			
			#put business
			business.put()
			#get businessID
			businessID = business.key()
		else:
			#business exists- grab its tags
			tags.extend(business.tags)
		
	elif origin == 'edit':
		#if the deal is being edited, then business info should not be updated, and we have the businessID
		businessID = self.request.get('uid')
		#get the tags from the business
		business_tags = self.request.get('tags')
		business_tags = levr.tagger(business_tags)
		tags.extend(business_tags)
		
	else:
		#this should never happen. Why is this happening? AHHHHHHH!
		raise Exception('origin is unknown')
	
	
	
	
	#====Deal Information Lines====#
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
	
	
	
	
	upload_flag = True
		#This flag indicates whether an image has been uploaded or not
		#it is tripped false if no image is uploaded
	
	
	#create the deal entity
	if origin	=='web':
			#web deals get active status and are the child of a business
		deal = levr.Deal(parent = businessID)
		deal.deal_status		= "active"
		deal.is_exclusive		= True

	elif origin	=='edit':
		dealID = self.request.get('id')
		logging.debug(dealID)
		dealID = enc.decrypt_key(dealID)
		logging.debug(dealID)
		deal = levr.Deal.get(dealID)
		logging.debug(self.request.get('image'))
		if not self.request.get('image'):
			#if an image was not uploaded, trip upload_flag
			upload_flag = False
			logging.debug(upload_flag)
		else:
				#an image was uploaded, so remove the old one.
			blob = deal.img
#			logging.debug(blob_key)
#			blob = blobstore.BlobInfo.get(blob_key)
			logging.debug(blob)
			blob.delete()
			logging.debug(blob)
	

	elif origin	=='phone':
			#phone deals get pending status and are the child of a ninja
		deal = levr.CustomerDeal(parent = db.Key(enc.decrypt_key(self.request.get('uid'))))
		deal.deal_status		= "pending"
		deal.is_exclusive		= False

	elif origin == 'pending':
		deal = levr.CustomerDeal.get(enc.decrypt_key(self.request.get('dealID')))
		deal.deal_status		= "active"
		deal.date_end			= datetime.now() + timedelta(days=7)
		new_tags = self.request.get('tags')
		tags.extend(levr.tagger(new_tags))
		if not self.request.get('image'):
			#if an image was not uploaded, trip upload_flag
			upload_flag = False
			logging.debug(upload_flag)
		
	
	
	
	
	if upload_flag == True:
		#if an image has been uploaded, add it to the deal. otherwise do nothing.
		#assumes that if an image already exists, that it the old one has been deleted elsewhere
		upload	= self.get_uploads()[0]
		blob_key= upload.key()
		deal.img= blob_key
	
	
	
	
	
	#add the data
	deal.deal_text 			= deal_text
	deal.description 		= description
	deal.tags				= tags
	
	#secondary_name
	if secondary_name:
		deal.deal_type = "bundle"
		tags.extend(levr.tagger(secondary_name))
		deal.secondary_name = secondary_name
	else:
		deal.deal_type = "single"
	
	if origin != 'edit':
		#this excludes the case where the deal is being edited
		#business info should not be overwritten in that case
		deal.business_name		= business_name
		deal.businessID			= business.key().__str__()
		deal.vicinity			= vicinity
		deal.date_start			= datetime.now()
		deal.geo_point			= geo_point
	
	
	
	
	#put the deal
	deal.put()
	
	
	#return share url
	share_url = 'http://getlevr.appspot.com/share/deal?id='+enc.encrypt_key(deal.key())
	return share_url
