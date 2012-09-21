#import webapp2
#import datetime
from google.appengine.ext import db
from google.appengine.ext.db import polymodel
from google.appengine.ext import blobstore
import re
#import string
import logging
import sys, traceback
import levr_encrypt as enc
import levr_utils

class Customer(db.Model):
#root class
	email 			= db.EmailProperty()
	payment_email	= db.EmailProperty()
	pw 				= db.StringProperty()
	alias			= db.StringProperty(default='')
	group			= db.StringProperty(choices=set(["paid","unpaid"]),default="paid")
	#stats
	money_earned	= db.FloatProperty(default = 0.0) #new earning for all deals
	money_available = db.FloatProperty(default = 0.0) #aka payment pending
	money_paid		= db.FloatProperty(default = 0.0) #amount we have transfered
	redemptions		= db.StringListProperty(default = [])	#id's of all of their redeemed deals
	new_redeem_count= db.IntegerProperty(default = 0) #number of unseen redemptions
	vicinity		= db.StringProperty(default='') #the area of the user, probably a college campus
	favorites		= db.ListProperty(db.Key,default=[])
	date_created	= db.DateTimeProperty(auto_now_add=True)
	date_last_edited= db.DateTimeProperty(auto_now_add=True)
	date_last_login = db.DateTimeProperty(auto_now=True)
	
	def increment_new_redeem_count(self):
		logging.info('incrementing!')
		self.new_redeem_count += 1
		return
	
	def flush_new_redeem_count(self):
		self.new_redeem_count = 0
		return
		
	def get_notifications(self):
		#grab new notifications
		new_redemption = self.new_redeem_count
		#flush notifications
		self.flush_new_redeem_count()
		#return new notification information
		return {
			"newRedemption"	: new_redemption
		}
		
	def get_stats(self):
		data = {
			"alias"				: self.alias,
			"numUploads"		: self.get_num_uploads(),
			"numRedemptions"	: self.redemptions.__len__(),
			"moneyAvailable"	: self.money_available,
			"moneyEarned"		: self.money_earned,
			"new_redeem_count"	: self.new_redeem_count
		}
		return data

	def update_money_earned(self,difference):
		self.money_earned += difference
		
	
	def update_money_available(self,difference):
		self.money_available += difference
		
		
	def get_num_uploads(self):
		'''Returns the number of deal children of user i.e. num they have uploaded'''
		uploads = CustomerDeal.gql("WHERE ANCESTOR IS :1",self.key())
		count = uploads.count()
		return count


	def echo_stats(self):
		logging.info('Customer money earned: ' 		+ str(self.money_earned))
		logging.info('Customer money available: ' 	+ str(self.money_available))
		logging.info('Customer money paid: ' 		+ str(self.money_paid))
		
	
#class Redemption(db.Model):
#child of customer
#	dealID
	


class BusinessOwner(db.Model):
	email 			= db.EmailProperty()
	pw 				= db.StringProperty()
	validated		= db.BooleanProperty(default=False)
	date_created	= db.DateTimeProperty(auto_now_add=True)
	date_last_edited= db.DateTimeProperty(auto_now=True)
	
	#psudoproperty: businesses - see business entity - this is a query for all the businesses that list this owner as the owner

class Business(db.Model):
	#root class
	business_name 	= db.StringProperty()
	vicinity		= db.StringProperty()
	geo_point		= db.GeoPtProperty() #latitude the longitude
	types			= db.ListProperty(str)
	targeted		= db.BooleanProperty(default=False)
	owner			= db.ReferenceProperty(BusinessOwner,collection_name='businesses')
	upload_email	= db.EmailProperty()
	creation_date	= db.DateTimeProperty(auto_now_add=True)
	date_created	= db.DateTimeProperty(auto_now_add=True)
	date_last_edited= db.DateTimeProperty(auto_now=True)
	widget_id		= db.StringProperty(default=levr_utils.create_unique_id())
	foursquare_id	= db.StringProperty()


	def create_tags(self):
		#create tags list
		tags = []
		
		#takes a business, and returns critical properties taggified
		business_name	= tagger(self.business_name)
		tags.extend(business_name)
		vicinity		= tagger(self.vicinity)
		tags.extend(vicinity)
		
		for t in self.types:
			t			= tagger(t)
			tags.extend(t)
		
		
		
		
		
		return tags
	
class Deal(polymodel.PolyModel):
#Child of business owner OR customer ninja
	#deal information
	img				= blobstore.BlobReferenceProperty()
	barcode			= blobstore.BlobReferenceProperty()
	businessID 		= db.StringProperty(default='') #CHANGE TO REFERENCEPROPERTY
	business_name 	= db.StringProperty(default='') #name of business
	secondary_name 	= db.StringProperty(default='') #== with purchase of
	deal_type 		= db.StringProperty(choices=set(["single","bundle"])) #two items or one item
	deal_text		= db.StringProperty(default='')
	is_exclusive	= db.BooleanProperty(default=False)
	share_id		= db.StringProperty(default=levr_utils.create_unique_id())
	description 	= db.StringProperty(multiline=True,default='') #description of deal
	date_start 		= db.DateTimeProperty(auto_now_add=False) #start date
	date_end 		= db.DateTimeProperty(auto_now_add=False)
	count_redeemed 	= db.IntegerProperty(default = 0) 	#total redemptions
	count_seen 		= db.IntegerProperty(default = 0)  #number seen
	geo_point		= db.GeoPtProperty() #latitude the longitude
	deal_status		= db.StringProperty(choices=set(["pending","active","rejected","expired"]),default="active")
	been_reviewed	= db.BooleanProperty(default=False)
	reject_message	= db.StringProperty()
	vicinity		= db.StringProperty()
	tags			= db.ListProperty(str)
	rank			= db.IntegerProperty(default = 0)
	has_been_shared	= db.BooleanProperty(default = False)
	date_uploaded	= db.DateTimeProperty(auto_now_add=True)
	date_created	= db.DateTimeProperty(auto_now_add=True)
	date_last_edited= db.DateTimeProperty(auto_now=True)

class CustomerDeal(Deal):
#Sub-class of deal
#A deal that has been uploaded by a user

	gate_requirement= db.IntegerProperty(default = 5) #threshold of redeems that must be passed to earn a gate
	gate_payment_per= db.IntegerProperty(default = 1) #dollar amount per gate
	gate_count		= db.IntegerProperty(default = 0) #number of gates passed so far
	gate_max		= db.IntegerProperty(default = 5) #max number of gates allowed
	earned_total	= db.FloatProperty(default = 0.0) #amount earned by this deal
	paid_out		= db.FloatProperty(default = 0.0) #amount paid out by this deal
	
	def share_deal(self):
		if self.has_been_shared == False:
			#deal has never been shared before
			#flag that it has been shared
			self.has_been_shared = True
			
			#increase the max payment gates the ninja can earn
			self.gate_max += 5
		else:
			#deal has been shared - do nothing
			pass
		return self.has_been_shared
	
	def update_earned_total(self):
		#what was self.earned_total to start with?
		old = self.earned_total
		#update
		self.earned_total = float(self.gate_count*self.gate_payment_per)
		#if changed, find the difference
		difference = 0.0
		if self.earned_total > old:
			difference = self.earned_total - old
			logging.info('Earned ' + difference.__str__() + ' dollar!')
			
		return difference
	
	def echo_stats(self):
		logging.info('Deal money earned: ' + str(self.earned_total))
		logging.info('Deal money paid: ' + str(self.paid_out))

class EmptySetResponse(db.Model):
#root class
	primary_cat		= db.StringProperty()
	img				= blobstore.BlobReferenceProperty()
	index			= db.IntegerProperty()
	date_created	= db.DateTimeProperty(auto_now_add=True)
	date_last_edited= db.DateTimeProperty(auto_now=True)
	
class CashOutRequest(db.Model):
#child of ninja
	amount			= db.FloatProperty()
	date_paid		= db.DateTimeProperty()
	status			= db.StringProperty(choices=set(['pending','paid','rejected']))
	payKey			= db.StringProperty()
	money_available_paytime	= db.FloatProperty()
	note			= db.StringProperty()
	date_created	= db.DateTimeProperty(auto_now_add=True)
	date_last_edited= db.DateTimeProperty(auto_now=True)

class ReportedDeal(db.Model):
	uid				= db.ReferenceProperty(Customer,collection_name='reported_deals')
	dealID			= db.ReferenceProperty(Deal,collection_name='reported_deals')
	date_created	= db.DateTimeProperty(auto_now_add=True)
	date_last_edited= db.DateTimeProperty(auto_now=True)
	
class BusinessBetaRequest(db.Model):
	business_name	= db.StringProperty()
	contact_name	= db.StringProperty()
	contact_email	= db.StringProperty()
	contact_phone	= db.StringProperty()
	date_created	= db.DateTimeProperty(auto_now_add=True)


#functions!
def phoneFormat(deal,use,primary_cat=None):
	#dealID is used in a number of places
	dealID = enc.encrypt_key(str(deal.key()))
#	logging.info(deal.key())
#	logging.info(dealID)
	#dealText
	dealText = deal.deal_text
		
	#dealTextExtra
	if deal.deal_type == 'bundle':
		logging.debug('flag bundle')
		dealTextExtra = '(with purchase of ' + deal.secondary_name + ')'
	else:
		logging.debug('flag single')
		dealTextExtra = ''
		
	if use == 'list' or use == 'myDeals' or use == 'widget':
		#list is search results
		#mydeals is for the list of a users uploaded deals
		#widget is for the html iframe for merchants
		data = {"dealID"		: dealID,
				"imgURL"		: levr_utils.URL+'/phone/img?dealID='+dealID+'&size=list',
				"imgURLlarge"	: levr_utils.URL+'/phone/img?dealID='+dealID+'&size=dealDetail',
				"geoPoint"		: deal.geo_point,
				"vicinity"		: deal.vicinity,
				"dealText"  	: dealText,
				"dealTextExtra" : dealTextExtra,
				"description"	: deal.description,
				"businessName"	: deal.business_name,
				"primaryCat"	: primary_cat,
				"isExclusive"	: deal.is_exclusive}
		if use == 'myDeals':
			#shows list deal information AND statistics
			deal_parent = db.get(deal.key().parent())
			logging.debug(deal_parent)
			data.update({
				"gateRequirement"	: deal.gate_requirement,						#The number of redemptions needed to earn a dollar on this deal
				"gatePaymentPer"	: deal.gate_payment_per,						#The dollar amount we pay for each gate
				"earnedTotal"		: deal.earned_total, 							#The amount of money that this deal has earned so far
				"paymentMax"		: deal.gate_max*deal.gate_payment_per,			#The most money we will pay them for this deal
				"paidOut"			: deal.paid_out,								#The amount of money that this deal has earned to date
				"dealStatus"		: deal.deal_status,								#active,pending,rejected,expired
				"dateEnd"			: deal.date_end.__str__()[:10],					#The date this deal becomes inactive
				"moneyAvailable"	: deal_parent.money_available,					#The amount of money that the NINJA has available for redemption
				"ninjaMoneyEarned"	: deal_parent.money_paid,						#The amount of money that the ninja has earned to date
				"weightedRedeems"	: deal.count_redeemed % deal.gate_requirement,	#The number of redemptions they need to earn another dollar
				"dealCountRedeemed"	: deal.count_redeemed,							#The number of times that the deal has been redeemed
				"shareURL"			: levr_utils.create_share_url(deal)				#The URL for them to share
			})
		if use == 'widget':
			data.update({
				"description"	: deal.description,
			})
	elif use == 'deal':
		#view deal information screen
		#grab business 
#		logging.info(deal.businessID)
#		b = db.get(deal.businessID)
		#uploaded by a user
		data = {"dealID"		: dealID,
				"imgURL"	  	: levr_utils.URL+'/phone/img?dealID='+dealID+'&size=dealDetail',
				"dealText"  	: dealText,
				"dealTextExtra" : dealTextExtra,
				"businessName"	: deal.business_name,
				"vicinity"		: deal.vicinity,
				"description"	: deal.description,
				"isExclusive"	: deal.is_exclusive}
				
	elif use == 'dealsScreen':
		deal_parent = db.get(deal.key().parent())
		logging.debug(deal_parent.kind())
		if deal_parent.kind() == 'Customer':
			#deal has a ninja parent.
			ninja = deal_parent
			alias = ninja.alias
			logging.debug(ninja)
		else:
#			business = deal_parent
			alias = ''
			
		data = {"barcodeURL"	: levr_utils.URL+'/phone/img?dealID='+dealID+'&size=dealDetail',
				"ninjaName"		: alias,
				"isExclusive"	: deal.is_exclusive}
	elif use == 'manage':
		data = {
			"dealID"		:dealID,
			"dealText"		:dealText,
			"dealTextExtra"	:dealTextExtra,
			"secondaryName"	:deal.secondary_name,
			"businessName"	:deal.business_name,
			"vicinity"		:deal.vicinity,
			"description"	:deal.description,
			"isExclusive"	:deal.is_exclusive,
			"imgURLLarge"	:levr_utils.URL+'/phone/img?dealID='+dealID+'&size=dealDetail',
			"imgURLSmall"	:levr_utils.URL+'/phone/img?dealID='+dealID+'&size=list',

			}
	data.update({'geoPoint':str(deal.geo_point)})
	logging.info(levr_utils.log_dict(data))
	return data

def geo_converter(geo_str):
	if geo_str:
		lat, lng = geo_str.split(',')
		return db.GeoPt(lat=float(lat), lon=float(lng))
	return None

def tagger(text): 
#	parsing function for creating tags from description, etc
	#replace underscores with spaces
	text.replace("_"," ")
	#remove all non text characters
	text = re.sub(r"[^\w\s]", '', text)
	#parse text string into a list of words if it is longer than 2 chars long
	tags = [w.lower() for w in re.findall("[\'\w]+", text) if len(w)>2]


	return tags

def log_error(message=''):
	#called by: levr.log_error(*self.request.body)
	exc_type,exc_value,exc_trace = sys.exc_info()
	logging.error(exc_type)
	logging.error(exc_value)
	logging.error(traceback.format_exc(exc_trace))
	logging.error(message)

