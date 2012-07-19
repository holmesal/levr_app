#import webapp2
#import datetime
from google.appengine.ext import db
from google.appengine.ext.db import polymodel
import logging
import sys, traceback

class Customer(db.Model):
#root class
	#key_name is uid
	email 			= db.EmailProperty()
	payment_email	= db.EmailProperty()
	pw 				= db.StringProperty()
	alias			= db.StringProperty()
	#stats
	money_earned	= db.FloatProperty(default = 0.0) #new earning for all deals
	money_available = db.FloatProperty(default = 0.0) #aka payment pending
	money_paid		= db.FloatProperty(default = 0.0) #amount we have transfered
	redemptions		= db.StringListProperty()	#id's of all of their redeemed deals
	redemptions_count= db.IntegerProperty(default = 0) #number of unseen redemptions
	
	def increment_redemptions_count(self):
		self.redemptions_count += 1
		return
	def flush_redemptions_count(self):
		del self.redemptions_count[:]
		return

	def get_stats(self):
		data = {
			"alias"			: self.alias,
			"numUploads"	: self.get_num_uploads(),
			"numRedemptions": self.redemptions.__len__(),
			"moneyAvailable": self.money_available,
			"moneyEarned"	: self.money_earned,
			"redemptions_count": self.redemptions_count
		}
		return data

	def update_money_earned(self,difference):
		self.money_earned = self.money_earned + difference
		
		'''Updates the total amount that the user has earned'''
		'''#grab all deals that are children, add payment_total from each
		q = CustomerDeal.gql('WHERE ANCESTOR IS :1',self.key())
		cashmoneys = 0
		for deal in q:
			logging.info(deal.__dict__)
			cashmoneys = cashmoneys + deal.earned_total
			
		if cashmoneys < self.money_earned:
			logging.error('Something strange is happening with the payment total calculation. Money is going down. Its a recession! MY GOD.')
		else:
			self.money_earned = cashmoneys
			logging.info('Total earned: ' + str(self.money_earned))'''
	
	def update_money_available(self,difference):
		self.money_available = self.money_available + difference
		
		'''#grab all child deals, sum (total_earned - paid_out)
		q = CustomerDeal.gql('WHERE ANCESTOR IS :1',self.key())
		available = 0
		for deal in q:
			available = available + (deal.earned_total-deal.paid_out)
		if available < self.money_available:
			logging.info('The amount of available money has somehow decreased. Has the user cashed out?')
		self.money_available = available
		logging.info('Money available: ' + str(self.money_available))'''
	
	def get_num_uploads(self):
		'''Returns the number of deal children of user i.e. num they have uploaded'''
		uploads = CustomerDeal.gql("WHERE ANCESTOR IS :1",self.key())
		count = uploads.count()
		return count


	def echo_stats(self):
		logging.info('Customer money earned: ' + str(self.money_earned))
		logging.info('Customer money available: ' + str(self.money_available))
		logging.info('Customer money paid: ' + str(self.money_paid))
		
	
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
    address_line2 	= db.StringProperty()
    city			= db.StringProperty()
    state 			= db.StringProperty()
    zip_code		= db.StringProperty()
    
    alias 	= db.StringProperty()
    contact_phone 	= db.PhoneNumberProperty()
    geo_point		= db.GeoPtProperty() #latitude the longitude
    
    def dictify(self):
		'''Formats the object into dictionary for review before release'''
		data = {
			"businessID"	: self.key().__str__(),
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
	img				= db.BlobProperty()
	businessID 		= db.StringProperty() #CHANGE TO REFERENCEPROPERTY
	business_name 	= db.StringProperty() #name of business
	secondary_name 	= db.StringProperty() #secondary category
	deal_type 		= db.StringProperty(choices=set(["single","bundle"])) #two items or one item
	deal_item		= db.StringProperty() #the item the deal is on - could be primary, secondary, ternery, whattt?
	description 	= db.StringProperty(multiline=True,default='') #description of deal
	discount_value 	= db.FloatProperty() #number, -1 if free
	discount_type	= db.StringProperty(choices=set(["percent","monetary","free"]))
	date_start 		= db.DateTimeProperty(auto_now_add=False) #start date
	date_uploaded	= db.DateTimeProperty(auto_now_add=True)
	date_end 		= db.DateTimeProperty(auto_now_add=False)
#	img_path		= db.StringProperty()   #string path to image
	city 			= db.StringProperty()  #optional
	count_end 		= db.IntegerProperty()  #max redemptions
	count_redeemed 	= db.IntegerProperty(default = 0) 	#total redemptions
	count_seen 		= db.IntegerProperty(default = 0)  #number seen
	geo_point		= db.GeoPtProperty() #latitude the longitude
	deal_status		= db.StringProperty(choices=set(["pending","active","rejected","expired"]))
	address_string	= db.StringProperty()
	
	def dictify(self):
		'''Dictifies object for viewing its information on the phone - "myDeals" '''
		data = {
			"dealID"		: self.key().__str__(),
			"img"			: self.img,
			"businessID"	: self.businessID.__str__(),
			"businessName"	: self.business_name,
			"name"  		: self.secondary_name,
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
			"dealID"		: self.key().__str__(),
			"img"			: self.img,
			"businessID"	: self.businessID.__str__(),
			"businessName"	: self.business_name,
			"name"  		: self.secondary_name,
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
	img				= db.BlobProperty()
	index			= db.IntegerProperty()
	
class CashOutRequest(db.Model):
#child of ninja
	amount			= db.FloatProperty()
	date			= db.DateTimeProperty()
	status			= db.StringProperty()
	
#functions!
def phoneFormat(deal,use,primary_cat=None):
	#dealText
	if deal.discount_type == 'free':
		dealText = 'Free ' + deal.deal_item
	elif deal.discount_type == 'percent':
		dealText = '%(discount_value)d%% Off %(deal_item)s' % {"discount_value":deal.discount_value,"deal_item":deal.deal_item}
	elif deal.discount_type == 'monetary':
		dealText = '$%(discount_value)d Off %(deal_item)s' % {"discount_value":deal.discount_value,"deal_item":deal.deal_item}
		
	#dealTextExtra
	if deal.deal_type == 'bundle':
		dealTextExtra = '(with purchase of ' + deal.secondary_name + ')'
	else:
		dealTextExtra = ''
		
	if use == 'list' or use == 'myDeals':
		data = {"dealID"		: str(deal.key()),
				"imgURL"	  	: 'http://getlevr.appspot.com/phone/img?dealID='+str(deal.key())+'&size=list',
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
				"paidOut"			: deal.paid_out,
				"dealStatus"		: deal.deal_status,
				"dateEnd"			: deal.date_end
			})
	elif use == 'deal':
	
		#grab business
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
		data = {"dealID"		: str(deal.key()),
				"imgURL"	  	: 'http://getlevr.appspot.com/phone/img?dealID='+str(deal.key())+'&size=dealDetail',
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

