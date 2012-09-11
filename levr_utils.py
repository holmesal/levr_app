#import webapp2
import os
import logging
#import jinja2
import levr_classes as levr
import levr_encrypt as enc
from datetime import datetime
from datetime import timedelta
#from google.appengine.ext import blobstore
from google.appengine.ext import db
#from google.appengine.ext.webapp import blobstore_handlers
from gaesessions import get_current_session
import base_62_converter as converter

# ==== Variables ==== #
if os.environ['SERVER_SOFTWARE'].startswith('Development') == True:
	#we are on the development environment
	URL = 'http://localhost:8080'
else:
	#we are deployed on the server
	URL = 'http://www.levr.com'



# ==== Functions ==== #
def loginCheck(self,strict):
	'''	for merchants
		This is a general-purpose login checking function 
		in "strict" mode (strict=True), this script will bounce to the login page if not logged in
		if strict=False, headers will be returned that indicate the user isn't logged in, but no bouncing'''
	session = get_current_session()
	logging.debug(session)
	if session.has_key('loggedIn') == False or session['loggedIn'] == False:
		if strict == True:
			#not logged in, bounce to login page
			logging.info('Not logged in. . .Bouncing!')
			self.redirect('/merchants/login')
		else:
			logging.info('Not logged in. . .Sending back headerData')
			headerData = {
				'loggedIn'	: False
			}
			return headerData
	elif session.has_key('loggedIn') == True and session['loggedIn'] == True:
		#logged in, grab the useful bits
		#this is a hack. . . forgive meeee
		uid = session['ownerID']
		
		headerData = {
			'loggedIn'	: session['loggedIn'],
			'ownerID'	: uid
			}
		#return user metadata.
		return headerData
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
		c 		= levr.Customer()
		c.email = email
		c.pw 	= pw
		c.alias = alias
		#put
		c.put()
		return {'success':True,'uid':enc.encrypt_key(c.key().__str__()),'email':email,'userName':alias}
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
			'data'			: {
								'uid'			: enc.encrypt_key(r_email.key().__str__()),
								'email'			: r_email.email,
								'userName'		: r_email.alias,
								},
			'notifications'	: r_email.get_notifications()
		}
	elif r_owner != None:
		#found user on the basis of username
		return {
			'success'		: True,
			'data'			: {
								'uid'			: enc.encrypt_key(r_owner.key().__str__()),
								'email'			: r_owner.email,
								'userName'		: r_owner.alias,
								},
			'notifications'	: r_owner.get_notifications()
		}
	else:
		return {
			'success'	: False,
			'error': 'Incorrect username, email, or password. Please try again!'
		}

def dealCreate(params,origin,upload_flag=True):
	'''pass in "self"'''
	logging.debug('DEAL CREATE')
	logging.debug(origin)
	logging.debug(params)
	
	logging.debug(upload_flag)
	#init tags list for deal
	tags = []
	
	#business information - never create business unless old phone
		#just want to get tags to store on deal
	#get deal information
	#create deals with appropriate owners
	
	'''

	
	#####merchant_edit
		params = {
				'uid'			#uid is businessOwner
				'business'		#businessID
				'deal'			#dealID
				'deal_description'
				'deal_line1'
				'deal_line2'
				}
		!!! check for uploaded image !!!
		

	#####merchant_create
		params = {
				'uid'			#uid is businessOwner
				'business'
				'deal_line1'
				'deal_line2' 	#optional
				'deal_description'
				'img_key'
				}
		
	#####phone
		params = {
				'uid' 			#uid is ninja
				'business' 
				'deal_description'
				'deal_line1'
				!!! no deal_line2 !!!
				}
	#####oldphone
		params = {
				'uid'			#uid is ninja
				'business_name'
				'geo_point'
				'vicinity'
				'types'
				'deal_description'
				'deal_line1'
				}
	#####admin_pending
		params = {
				'uid'		#uid is ninja
				'deal'		#deal id
				'business'	#business id
				'deal_line1'
				'deal_line2'
				'deal_description'
				'tags'
				'end date'
				!!! other stuff !!!
				}
	'''
	
	
	#==== deal information ====#
	
	
	#==== business stuff ====#
	if origin == 'oldphone':
		#this will soon be deprecated when android is done
		logging.debug('origin is NOT edit or web or phone. running out of options here.')
		
		
		#business name
		business_name = params['business']
		logging.debug("business name: "+str(business_name))
		
		#geo point
		geo_point = params['geo_point']
		geo_point = levr.geo_converter(geo_point)
		logging.debug("geo point: "+str(geo_point))
		
		#vicinity
		vicinity = params['vicinity']
		logging.debug("vicinity: "+str(vicinity))
		
		#types
		types = params['types']
		logging.debug(types)
		types = levr.tagger(types)
		logging.debug(types)
		
		
		#check if business exists - get businessID
		business= levr.Business.gql("WHERE business_name=:1 and geo_point=:2", business_name, geo_point).get()
		
		if not business:
			logging.debug('business doesnt exist')
			#if a business doesn't exist in db, then create a new one
			business = levr.Business()
			logging.debug(business.__str__())
			#add data to the new business
			business.business_name 	= business_name
			business.vicinity 		= vicinity
			business.geo_point		= geo_point
			business.types			= types

			#grab the businesses tags
			tags.extend(business.create_tags())
			
			#put business
			business.put()
			
			#get businessID - not encrypted - from database
			businessID = business.key()
		else:
			logging.debug('business exists')
			#business exists- grab its tags
			tags.extend(business.create_tags())
		
		
		#Create tags
		
		logging.debug('-------------------------------------------')
		logging.debug(tags)
	else:
		#
		logging.debug('not oldphoone')
		
		businessID = params['business']
		businessID	= enc.decrypt_key(businessID)
		businessID	= db.Key(businessID)
		business	= levr.Business.get(businessID)
		
		#get the tags from the business
		tags.extend(business.create_tags())
		
		#grab all the other information that needs to go into the deals
		business_name 	= business.business_name
		geo_point		= business.geo_point
		vicinity		= business.vicinity
		


	#====Deal Information Lines ====#
	#deal line 1
	deal_text	= params['deal_line1']
	logging.debug(deal_text)
	tags.extend(levr.tagger(deal_text))
	logging.info(tags)
	
	#deal line 2
	if origin != 'phone' and origin != 'oldphone':
		secondary_name = params['deal_line2']
		logging.debug(secondary_name)
		if secondary_name:
			#deal is bundled
			logging.debug('deal is bundled')
			tags.extend(levr.tagger(secondary_name))
			logging.info(tags)
			deal_type = 'bundle'
		else:
			#deal is not bundled
			'deal is NOT bundled'
			deal_type = 'single'
	else:
		#phone uploaded deals do not pass deal_line2
		deal_type = 'single'
	
	#description
	description = params['deal_description']
	#truncate description to a length of 500 chars
	logging.debug(description.__len__())
	description = description[:500]
	logging.debug(description)
	tags.extend(levr.tagger(description))
	logging.info(tags)
	
	
	
	
	
	#==== create the deal entity ====#
	if origin	== 'merchant_create':
		#web deals get active status and are the child of the owner
		ownerID = params['uid']
		ownerID = enc.decrypt_key(ownerID)
		
		deal = levr.Deal(parent = db.Key(ownerID))
		deal.deal_status		= "active"
		deal.is_exclusive		= True

	elif origin	=='merchant_edit':
		dealID	= params['deal']
		dealID	= enc.decrypt_key(dealID)
		deal	= levr.Deal.get(dealID)

	elif origin	=='phone' or 'oldphone':
		#phone deals get pending status and are the child of a ninja
		uid = enc.decrypt_key(params['uid'])

		deal = levr.CustomerDeal(parent = db.Key(uid))
		deal.deal_status		= "active"#"pending"
		deal.is_exclusive		= False

	elif origin == 'admin_pending':
		#deal has already been uploaded by ninja - rewriting info that has been reviewed
		dealID = enc.decrypt_key(params['deal'])
		deal = levr.CustomerDeal.get(db.Key(dealID))
		
		deal.deal_status		= "active"
		deal.date_start			= datetime.now()
		deal.date_end			= datetime.now() + timedelta(days=7)
		
		new_tags = params['tags']
		tags.extend(levr.tagger(new_tags))

	
	
	#==== Link deal to blobstore image ====#
	if upload_flag == True:
		#an image has been uploaded, and the blob needs to be tied to the deal
		logging.debug('image uploaded')
		if origin == 'merchant_edit' or origin == 'admin_pending':
			#an image was uploaded, so remove the old one.
			blob = deal.img
			blob.delete()
		#if an image has been uploaded, add it to the deal. otherwise do nothing.
		#assumes that if an image already exists, that it the old one has been deleted elsewhere
		blob_key = params['img_key']
		deal.img= blob_key
	else:
		#an image was not uploaded. do nothing
		logging.debug('image not uploaded')
		pass
	
	
	
	
	
	#add the data
	deal.deal_text 			= deal_text
	deal.deal_type			= deal_type
	deal.description 		= description
	deal.tags				= tags
	deal.business_name		= business_name
	deal.businessID			= businessID.__str__()
	deal.vicinity			= vicinity
	deal.geo_point			= geo_point
	
	#secondary_name
	if deal_type == 'bundle':
		deal.secondary_name = secondary_name
	
	#create the share ID - based on milliseconds since epoch
	milliseconds = int(unix_time_millis(datetime.now()))
	#make it smaller so we get ids with 5 chars, not 6
	shortened_milliseconds = milliseconds % 100000000
	unique_id = converter.dehydrate(shortened_milliseconds)
	
	deal.share_id = unique_id
	
	#log properties
	
	#put the deal
	deal.put()
	
	logging.debug(log_model_props(deal))
	logging.debug(log_model_props(business))
	
	#return share url
	share_url = create_share_url(deal)
	return share_url

def unix_time(dt):
	epoch = datetime.utcfromtimestamp(0)
	delta = dt - epoch
	return delta.total_seconds()
	
def unix_time_millis(dt):
	return unix_time(dt)

def create_share_url(deal_entity):
	#creates a share url for a deal
	if os.environ['SERVER_SOFTWARE'].startswith('Development') == True:
		#we are on the development environment
		URL = 'http://localhost:8080/'
	else:
		#we are deployed on the server
		URL = 'levr.com/'
		
	share_url = URL+deal_entity.share_id
	return share_url

def log_model_props(model,props=None):
	#returns a long multiline string of the model in key: prop
	delimeter = "\n\t\t"
	log_str = delimeter
	if type(props) is list:
		#only display certain keys
		for key in props:
			log_str += str(key)+": "+str(getattr(model,key))+delimeter
	else:
		#display all keys
		for key in model.properties():
			log_str += str(key)+": "+str(getattr(model,key))+delimeter
	
	
	return log_str

def log_dir(obj,props=None):
	#returns a long multiline string of a regular python object in key: prop
	delimeter = "\n\t\t"
	log_str = delimeter
	if type(props) is list:
		#only display certain keys
		for key in props:
			log_str += str(key)+": "+str(getattr(obj,key))+delimeter
	else:
		#display all keys
		for key in dir(obj):
			log_str += str(key)+": "+str(getattr(obj,key))+delimeter
	
	
	return log_str