#import webapp2
#import datetime
from google.appengine.ext import db
from google.appengine.ext.db import polymodel
from google.appengine.ext import blobstore
import logging
import sys, traceback
import levr_encrypt as enc

class Customer(db.Model):
#root class
	#key_name is uid
	email 			= db.EmailProperty()
	payment_email	= db.EmailProperty()
	pw 				= db.StringProperty()
	alias			= db.StringProperty(default='')
	#stats
	money_earned	= db.FloatProperty(default = 0.0) #new earning for all deals
	money_available = db.FloatProperty(default = 0.0) #aka payment pending
	money_paid		= db.FloatProperty(default = 0.0) #amount we have transfered
	redemptions		= db.StringListProperty(default = [])	#id's of all of their redeemed deals
	new_redeem_count= db.IntegerProperty(default = 0) #number of unseen redemptions
	
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
	


#deal_redeemed 	= db.ListProperty(str) #list of deal keys
#^^^would need another assoc table 

class Business(db.Model):
#root class
    email 			= db.EmailProperty()
    pw 				= db.StringProperty()
    signup_date 	= db.DateTimeProperty()	#when signed up for our service $$$
    creation_date	= db.DateTimeProperty(auto_now_add=True) #when created organically by user
    business_name 	= db.StringProperty()
    
    address_line1 	= db.StringProperty()
    address_line2 	= db.StringProperty(default='')
    city			= db.StringProperty()
    state 			= db.StringProperty()
    zip_code		= db.StringProperty()
    
    alias 			= db.StringProperty()
    contact_phone 	= db.PhoneNumberProperty()
    geo_point		= db.GeoPtProperty() #latitude the longitude
    
    def dictify(self):
		'''Formats the object into dictionary for review before release'''
		data = {
			"businessID"	: enc.encrypt_key(self.key().__str__()),
			"addressLine1"	: self.address_line1,
			"addressLine2"	: self.address_line2,
			"city"			: self.city,
			"state"			: self.state,
			"zip"			: self.zip_code,
			"businessName"	: self.business_name,
			"geoPoint"		: self.geo_point,
		}
		return data
class Deal(polymodel.PolyModel):
#Child of business OR customer ninja
	#key name is deal id
	#deal information
	img				= blobstore.BlobReferenceProperty()
	businessID 		= db.StringProperty(default='') #CHANGE TO REFERENCEPROPERTY
	business_name 	= db.StringProperty(default='') #name of business
	secondary_name 	= db.StringProperty(default='') #secondary category
	deal_type 		= db.StringProperty(choices=set(["single","bundle"])) #two items or one item
	deal_item		= db.StringProperty(default='') #the item the deal is on - could be primary, secondary, ternery, whattt?
	deal_text		= db.StringProperty()

	description 	= db.StringProperty(multiline=True,default='') #description of deal
	discount_value 	= db.FloatProperty() #number, -1 if free
	discount_type	= db.StringProperty(choices=set(["percent","monetary","free"]))
	date_start 		= db.DateTimeProperty(auto_now_add=False) #start date
	date_uploaded	= db.DateTimeProperty(auto_now_add=True)
	date_end 		= db.DateTimeProperty(auto_now_add=False)
#	img_path		= db.StringProperty()   #string path to image
	city 			= db.StringProperty(default='')  #optional
	count_end 		= db.IntegerProperty()  #max redemptions
	count_redeemed 	= db.IntegerProperty(default = 0) 	#total redemptions
	count_seen 		= db.IntegerProperty(default = 0)  #number seen
	geo_point		= db.GeoPtProperty() #latitude the longitude
	deal_status		= db.StringProperty(choices=set(["pending","active","rejected","expired"]))
	address_string	= db.StringProperty()
	
	def dictify(self):
		'''Dictifies object for viewing its information on the phone - "myDeals" '''
		data = {
			"dealID"		: enc.encrypt_key(self.key().__str__()),
			"img"			: self.img,
			"businessID"	: enc.encrypt_key(self.businessID.__str__()),
			"businessName"	: self.business_name,
			"secondaryName"	: self.secondary_name,
			"deal_type"  	: self.deal_type,
			"deal_item"		: self.deal_item,
			"description"   : self.description,
			"discountValue" : self.discount_value,
			"discountType"  : self.discount_type,
#			"dealOrigin"	: self.deal_origin,
#			"dateStart"		: self.date_start,
			"dateEnd"		: self.date_end,
			"city"			: self.city,
			"endValue"  	: self.count_end,
#			"imgPath"		: self.img_path,
			"countRedeemed"	: self.count_redeemed,
#			"gateRequirement": self.gate_requirement,
#			"gatePaymentPer": self.gate_payment_per,
#			"gateCount"		: self.gate_count,
#			"gateMax"		: self.gate_max,
			"dateUploaded"	: self.date_uploaded,
#			"paymentTotal"	: self.payment_total(),
			"geoPoint"		: str(self.geo_point),
			"dealStatus"	: self.deal_status,
		}
		return data


class CustomerDeal(Deal):
#Sub-class of deal
#A deal that has been uploaded by a user

	gate_requirement= db.IntegerProperty(default = 5) #threshold of redeems that must be passed to earn a gate
	gate_payment_per= db.IntegerProperty(default = 1) #dollar amount per gate
	gate_count		= db.IntegerProperty(default = 0) #number of gates passed so far
	gate_max		= db.IntegerProperty(default = 10) #max number of gates allowed
	earned_total	= db.FloatProperty(default = 0.0) #amount earned by this deal
	paid_out		= db.FloatProperty(default = 0.0) #amount paid out by this deal
	
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
	
	def dictify(self):
		'''Dictifies object for viewing its information on the phone - "myDeals" '''
		data = {
			"dealID"		: enc.encrypt_key(self.key().__str__()),
			"img"			: self.img,
			"businessID"	: enc.encrypt_key(self.businessID.__str__()),
			"businessName"	: self.business_name,
			"secondaryName"	: self.secondary_name,
			"deal_type"  	: self.deal_type,
			"deal_item"		: self.deal_item,
			"description"   : self.description,
			"discountValue" : self.discount_value,
			"discountType"  : self.discount_type,
#			"dealOrigin"	: self.deal_origin,
#			"dateStart"		: self.date_start,
			"dateEnd"		: self.date_end,
			"city"			: self.city,
			"endValue"  	: self.count_end,
#			"imgPath"		: self.img_path,
			"countRedeemed"	: self.count_redeemed,
			"gateRequirement": self.gate_requirement,
			"gatePaymentPer": self.gate_payment_per,
			"gateCount"		: self.gate_count,
			"gateMax"		: self.gate_max,
			"dateUploaded"	: self.date_uploaded,
			"paid_out"		: self.paid_out,
			"geoPoint"		: str(self.geo_point),
			"dealStatus"	: self.deal_status,
		}
		return data


class Category(db.Model):
#Child of deal
#Maps primary categories to deals
	primary_cat		= db.StringProperty()

class Favorite(db.Model):
#child of user
	dealID			= db.StringProperty() #CHANGE TO REFERENCEPROPERTY FOR PRODUCTION
	primary_cat		= db.StringProperty()


class EmptySetResponse(db.Model):
#root class
	primary_cat		= db.StringProperty()
	img				= blobstore.BlobReferenceProperty()
	index			= db.IntegerProperty()
	
class CashOutRequest(db.Model):
#child of ninja
	amount			= db.FloatProperty()
	date_created	= db.DateTimeProperty(auto_now_add=True)
	date_paid		= db.DateTimeProperty()
	status			= db.StringProperty(choices=set(['pending','paid','rejected']))
	payKey			= db.StringProperty()
	money_available_paytime	= db.FloatProperty()
	note			= db.StringProperty()
	
#functions!
def phoneFormat(deal,use,primary_cat=None):
	#dealID is used in a number of places
	dealID = enc.encrypt_key(str(deal.key()))
	logging.info(deal.key())
	logging.info(dealID)
	#dealText
	if deal.discount_type == 'free':
		dealText = 'Free ' + deal.deal_item
	elif deal.discount_type == 'percent':
		dealText = '%(discount_value)d%% Off %(deal_item)s' % {"discount_value":deal.discount_value,"deal_item":deal.deal_item}
	elif deal.discount_type == 'monetary':
		dealText = '$%(discount_value)d Off %(deal_item)s' % {"discount_value":deal.discount_value,"deal_item":deal.deal_item}
	else:
		#can assume that deal is still pending because discount_type is undefined
		dealText = deal.deal_text
		
	#dealTextExtra
	if deal.deal_type == 'bundle':
		dealTextExtra = '(with purchase of ' + deal.secondary_name + ')'
	else:
		dealTextExtra = ''
		
	if use == 'list' or use == 'myDeals' or use == 'widget':
		
		data = {"dealID"		: dealID,
				"imgURL"	  	: 'http://0.0.0.0:8080/phone/img?dealID='+dealID+'&size=widget',
#				"imgURL"	  	: 'http://getlevr.appspot.com/phone/img?dealID='+dealID+'&size=list',
				"dealText"  	: dealText,
				"dealTextExtra" : dealTextExtra,
				"businessName"	: deal.business_name,
				"primaryCat"	: primary_cat}
		if use == 'myDeals':
			#shows list deal information AND statistics
			data.update({
				"gateRequirement"	: deal.gate_requirement,
				"gatePaymentPer"	: deal.gate_payment_per,
				"earnedTotal"		: deal.earned_total,
				"paymentMax"		: deal.gate_max*deal.gate_payment_per,
				"paidOut"			: deal.paid_out,
				"dealStatus"		: deal.deal_status,
				"dateEnd"			: deal.date_end.__str__()[:10],
				"moneyAvailable"	: db.get(deal.key().parent()).money_available,
				"weightedRedeems"	: deal.count_redeemed % deal.gate_requirement,
				"shareURL"			: 'http://getlevr.appspot.com/share/deal?id='+dealID
			})
		if use == 'widget':
			data.update({
				"description"	: deal.description,
			})
	elif use == 'deal':
	
		#grab business
		logging.info(deal.businessID)
		b = db.get(deal.businessID)
		#view deal information screen
		#uploaded by a user
		#idx = deal.address_string.find(',')
		#displayAddress = deal.address_string[0:idx]
		#uploaded by a business
		#businessID = deal.key().parent()
		#b = Business.get(businessID)
		#displayAddress = b.address_line1 + ', ' + b.address_line2
		#businessAddress = '%(:1)s %(:2)s %(:3)s %(:4)s, %(:5)s %(:6)s' % {deal.business_name, b.address_line1, b.address_line2, b.city, b.state, b.zip_code}
		data = {"dealID"		: dealID,
				"imgURL"	  	: 'http://getlevr.appspot.com/phone/img?dealID='+dealID+'&size=dealDetail',
				"dealText"  	: dealText,
				"dealTextExtra" : dealTextExtra,
				"businessName"	: deal.business_name,
				"gmapsAddress"	: '%(addy1)s %(addy2)s, %(city)s, %(state)s %(zip)s' % {"addy1":b.address_line1,"addy2":b.address_line2,"city":b.city,"state":b.state,"zip":b.zip_code},
				"displayAddress": b.address_line1,
				"description"	: deal.description,
				"city"			: deal.city}
	logging.info(data)
	return data

def phoneBusinessFormat(business):
	'''Format business output from DB for phone use'''
	#map object properties to dictionaries
	data = {"addressLine1"	: business.address_line1,
			"addressLine2"	: business.address_line2,
			"city"			: business.city,
			"state"			: business.state,
			"zip"			: business.zip_code
	}
	return data

def web_edit_account_format(business):
	data = {
		"email"			: business.email,
		"businessName"	: business.business_name,
		"address1"		: business.address_line1,
		"address2"		: business.address_line2,
		"city"			: business.city,
		"state"			: business.state,
		"zipCode"		: business.zip_code,
		"ownerName"		: business.alias,
		"phone"			: business.contact_phone
	}
	return data

def web_edit_deal_format(deal):
	data = {
		"secondary_name": deal.secondary_name,
		"deal_type"		: deal.deal_type,
		"description"	: deal.description,
		"end_value"		: deal.count_end,
		"discount_type"	: deal.discount_type,
		"deal_value"	: deal.discount_value,
		"city"			: deal.city
	}
	return data
def geo_converter(geo_str):
	if geo_str:
		lat, lng = geo_str.split(',')
		return db.GeoPt(lat=float(lat), lon=float(lng))
	return None

def log_error(message=''):
	#called by: levr.log_error(*self.request.body)
	exc_type,exc_value,exc_trace = sys.exc_info()
	logging.error(exc_type)
	logging.error(exc_value)
	logging.error(traceback.format_exc(exc_trace))
	logging.error(message)

