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
from random import randint 
import geo.geohash as geohash

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
		
		#generate random number to decide what split test group they are in
		choice = randint(10,1000)
		decision = choice%2
		if decision == 1:
			group = 'paid'
		else:
			group = 'unpaid'
		
		#set a/b test group to customer entity
		c.group = group
		
		#put
		c.put()
		return {
			'success'	:True,
			'uid'		:enc.encrypt_key(c.key().__str__()),
			'email'		:email,
			'userName'	:alias,
			'group'		:group
			}
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
		
		#automatically update last login
		r_email.put()
		return {
			'success'		: True,
			'data'			: {
								'uid'			: enc.encrypt_key(r_email.key().__str__()),
								'email'			: r_email.email,
								'userName'		: r_email.alias,
								'group'			: r_email.group
								},
			'notifications'	: r_email.get_notifications()
		}
	elif r_owner != None:
		#found user on the basis of username
		
		#automatically update last_login
		r_owner.put()
		
		return {
			'success'		: True,
			'data'			: {
								'uid'			: enc.encrypt_key(r_owner.key().__str__()),
								'email'			: r_owner.email,
								'userName'		: r_owner.alias,
								'group'			: r_owner.group
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
	
	logging.debug("origin: "+str(origin))
	logging.debug(log_dict(params))
	
	
	logging.debug("image was uploaded: "+str(upload_flag))
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
		
	#####phone_existing_business
		params = {
				'uid' 			#uid is ninja
				'business' 
				'deal_description'
				'deal_line1'
				!!! no deal_line2 !!!
				}
	#####phone_new_business
		params = {
				'uid'			#uid is ninja
				'business_name'
				'geo_point'
				'vicinity'
				'types'
				'deal_description'
				'deal_line1'
				}
	#####admin_review
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
	if origin == 'phone_new_business':
		#The business to which a deal is being uploaded is not targeted
		logging.debug('origin is phone, new business being added')
		
		
		#business name
		if 'business_name' in params:
			business_name = params['business_name']
			logging.debug("business name: "+str(business_name))
		else:
			raise KeyError('business_name not in params')
		#geo point
		
		if 'geo_point' in params:
			geo_point = params['geo_point']
			geo_point = levr.geo_converter(geo_point)
			logging.debug("geo point: "+str(geo_point))
		else:
			raise KeyError('geo_point not in params')
		
		#vicinity
		if 'vicinity' in params:
			vicinity = params['vicinity']
			logging.debug("vicinity: "+str(vicinity))
		else:
			raise KeyError('vicinity not in params')
		
		#types
		if 'types' in params:
			types = params['types']
			logging.debug('start types')
			logging.debug(types)
			logging.debug(type(types))
			types = levr.tagger(types)
			logging.debug(types)
			logging.debug('end types')
		else:
			raise KeyError('types not in params')
		#check if business exists - get businessID
#		business= levr.Business.gql("WHERE business_name=:1 and geo_point=:2", business_name, geo_point).get()
		business = levr.Business.all().filter('business_name =',business_name).filter('vicinity =',vicinity).get()
		logging.debug('start business info')
		logging.debug(log_model_props(business))
		logging.debug('end business info')
		
		if not business:
			logging.debug('business doesnt exist')
			#if a business doesn't exist in db, then create a new one
			business = levr.Business()
			logging.debug(log_model_props(business))
			
			#create geohash from geopoint
			geo_hash = geohash.encode(geo_point.lat,geo_point.lon)
			
			#add data to the new business
			business.business_name 	= business_name
			business.vicinity 		= vicinity
			business.geo_point		= geo_point
			business.types			= types
			business.geo_hash		= geo_hash
			
			#put business
			business.put()
			
			
		else:
			logging.debug('business exists')
			#business exists- grab its tags
		
		
		#grab the businesses tags
		tags.extend(business.create_tags())
		#get businessID - not encrypted - from database
		businessID = business.key()
		logging.debug("businessID: "+str(businessID))
		
		#Create tags
		
		logging.debug('-------------------------------------------')
		logging.debug(tags)
	else:
		#BusinessID was passed, grab the business
		logging.debug('not oldphoone')
		
		if 'business' in params:
			businessID = params['business']
			businessID	= enc.decrypt_key(businessID)
			businessID	= db.Key(businessID)
			business	= levr.Business.get(businessID)
		else:
			raise KeyError('business not passed in params')
		#get the tags from the business
		tags.extend(business.create_tags())
		
		#grab all the other information that needs to go into the deals
		business_name 	= business.business_name
		geo_point		= business.geo_point
		vicinity		= business.vicinity
		geo_hash		= business.geo_hash
		

	logging.debug('!!!!!')
	#====Deal Information Lines ====#
	#deal line 1
	if 'deal_line1' in params:
		deal_text	= params['deal_line1']
		logging.debug(deal_text)
		tags.extend(levr.tagger(deal_text))
		logging.info(tags)
	else:
		raise KeyError('deal_line1 not passed in params')
	
	#deal line 2
	if origin != 'phone_existing_business' and origin != 'phone_new_business':
		if 'deal_line2' in params:
			secondary_name = params['deal_line2']
		else:
			secondary_name = False
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
	if 'deal_description' in params:
		description = params['deal_description']
		#truncate description to a length of 500 chars
		logging.debug(description.__len__())
		description = description[:500]
		logging.debug(description)
		tags.extend(levr.tagger(description))
		logging.info(tags)
	else:
		raise KeyError('deal_description not passed in params')
	
	
	
	
	#==== create the deal entity ====#
	if origin	== 'merchant_create':
		#web deals get active status and are the child of the owner
		ownerID = params['uid']
		ownerID = enc.decrypt_key(ownerID)
		
		deal = levr.Deal(parent = db.Key(ownerID))
		deal.is_exclusive		= True

	elif origin	=='merchant_edit':
		dealID	= params['deal']
		dealID	= enc.decrypt_key(dealID)
		deal	= levr.Deal.get(dealID)

	elif origin	=='phone_existing_business' or origin == 'phone_new_business':
		#phone deals are the child of a ninja
		logging.debug('STOP!')
		uid = enc.decrypt_key(params['uid'])

		deal = levr.CustomerDeal(parent = db.Key(uid))
		deal.is_exclusive		= False
		
		
		deal.date_end			= datetime.now() + timedelta(days=7)

	elif origin == 'admin_review':
		#deal has already been uploaded by ninja - rewriting info that has been reviewed
		dealID = enc.decrypt_key(params['deal'])
		deal = levr.CustomerDeal.get(db.Key(dealID))
		deal.been_reviewed		= True
		deal.date_start			= datetime.now()
		days_active				= int(params['days_active'])
		deal.date_end			= datetime.now() + timedelta(days=days_active)
		
		new_tags = params['extra_tags']
		tags.extend(levr.tagger(new_tags))
		logging.debug('!!!!!!!!!!!!')
		logging.debug(tags)
	
	
	#==== Link deal to blobstore image ====#
	if upload_flag == True:
		#an image has been uploaded, and the blob needs to be tied to the deal
		logging.debug('image uploaded')
		if origin == 'merchant_edit' or origin == 'admin_review':
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
	
	
	
	#put the deal
	deal.put()
	
	#dealput is the deal key i.e. dealID
	logging.debug(log_model_props(deal))
	logging.debug(log_model_props(business))
	
	share_url = create_share_url(deal)
	
	if origin == 'phone_existing_business' or origin =='phone_new_business':
		#needs share url and dealID
		return share_url,deal
	else:
		#return share url
		return share_url

def create_unique_id():
	#create the share ID - based on milliseconds since epoch
	milliseconds = int(unix_time_millis(datetime.now()))
	#make it smaller so we get ids with 5 chars, not 6
	shortened_milliseconds = milliseconds/10 % 1000000000
	unique_id = converter.dehydrate(shortened_milliseconds)
	return unique_id

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

def get_deals_in_area(tags,request_point,precision=5):
	'''
	tags = list of tags that are strings
	request point is db.GeoPt format
	precision is int
	'''
	request_point = levr.geo_converter('42.35,-71.110')
	logging.debug(precision)
	center_hash = geohash.encode(request_point.lat,request_point.lon,precision=precision)
	logging.debug(center_hash)
	hash_set = geohash.expand(center_hash)
	logging.debug(hash_set)
	
	
	ref_query = levr.Deal.all(keys_only=True).filter('deal_status =','active')
	for tag in tags:
		ref_query.filter('tags =',tag)
	logging.info("total number of deals: "+str(ref_query.fetch(None).__len__()))
	
	
	####build search query
	#only grabbing deal keys, then batch get array
	deal_keys = []
	for query_hash in hash_set:
		#only grab keys for deals that have active status
		q = levr.Deal.all(keys_only=True).filter('deal_status =','active')
		#grab all deals where primary_cat is in tags
		for tag in tags:
			#all is a special keyword
			if tag != 'all':
				logging.debug('tag: '+str(tag))
				q.filter('tags =',tag)
		#filter by geohash
		q.filter('geo_hash >=',query_hash).filter('geo_hash <=',query_hash+"{") #max bound
#					logging.debug(q)
#					logging.debug(levr_utils.log_dict(q.__dict__))
		
		#get all keys for this neighborhood
		fetched_deals = q.fetch(None)
		logging.info('From: '+query_hash+", fetched: "+str(fetched_deals.__len__()))
		
		deal_keys.extend(fetched_deals)
#					logging.debug(deal_keys)
	
	#batch get results. here is where we would set the number of results we want and the offset
	deals = levr.Deal.get(deal_keys)
	return deals


def log_model_props(model,props=None):
	#returns a long multiline string of the model in key: prop
	delimeter = "\n\t\t"
	log_str = delimeter
	try:
		if type(props) is list:
			#only display certain keys
			for key in props:
				log_str += str(key)+": "+str(getattr(model,key))+delimeter
		else:
			#display all keys
			key_list = []
			for key in model.properties():
				key_list.append(key)
			key_list.sort()
			for key in key_list:
				log_str += str(key)+": "+str(getattr(model,key))+delimeter
	except Exception,e:
		logging.warning('There was an error in log_model_props %s',e)
	finally:
		return log_str

def log_dir(obj,props=None):
	#returns a long multiline string of a regular python object in key: prop
	delimeter = "\n\t\t"
	log_str = delimeter
	try:
		if type(props) is list:
			logging.debug('log some keys')
			#only display certain keys
			key_list = []
			for key in props:
				key_list.append(key)
			key_list.sort()
			for key in key_list:
				log_str += str(key)+": "+str(getattr(obj,key))+delimeter
		else:
			logging.debug('log all keys')
			#display all keys
			for key in dir(obj):
				log_str += str(key)+": "+str(getattr(obj,key))+delimeter
	except:
		logging.warning('There was an error in log_dir')
	finally:
		return log_str

def log_dict(obj,props=None):
	#returns a long multiline string of a regular python object in key: prop
	delimeter = "\n\t\t"
	log_str = delimeter
	try:
		if type(props) is list:
			#only display certain keys
			for key in props:
				log_str += str(key)+": "+str(obj[key])+delimeter
		else:
			#display all keys
			key_list = []
			for key in obj:
				key_list.append(key)
			key_list.sort()
			for key in key_list:
				log_str += str(key)+": "+str(obj[key])+delimeter
	except:
		logging.warning('There was an error in log_dict')
	finally:
		return log_str
