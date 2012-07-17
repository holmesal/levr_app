#import webapp2
#import datetime
from google.appengine.ext import db
from google.appengine.ext.db import polymodel

class Customer(db.Model):
#root class
	#key_name is uid
	email 			= db.EmailProperty()
	payment_email	= db.EmailProperty()
	pw 				= db.StringProperty()
	alias			= db.StringProperty()
	#stats
	money_earned	= db.FloatProperty()
	money_paid		= db.FloatProperty()
	

	def format_stats(self):
		data = {
			"alias"			: self.alias,
			"money_earned"	: self.money_earned,
			"money_saved"	: self.money_saved
		}
		return data
	def update_total_earned(self):
		'''Updates the total amount that the user has earned'''
		pass
	def update_total_paid(self):
		'''Updates the total amount that the user has cashed out'''
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
    creation_date	= db.DateTimeProperty() #when created organically by user
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
			"address_line1"	: self.address_line1,
			"address_line2"	: self.address_line2,
			"city"			: self.city,
			"state"			: self.state,
			"zip_code"		: self.zip_code,
			"business_name"	: self.business_name,
			"geo_point"		: self.geo_point,
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
	name_type 		= db.StringProperty() #category or single item
	description 	= db.StringProperty(multiline=True) #description of deal
	discount_value 	= db.FloatProperty() #number, -1 if free
	discount_type	= db.StringProperty(choices=set(["percent","monetary","free"]))
	deal_origin		= db.StringProperty(choices=set(["internal","external"]))
	
	date_start 		= db.DateProperty() #start date
	date_end 		= db.DateProperty()
#	img_path		= db.StringProperty()   #string path to image
	city 			= db.StringProperty()  #optional
	count_end 		= db.IntegerProperty()  #max redemptions
	count_redeemed 	= db.IntegerProperty() 	#total redemptions
	count_seen 		= db.IntegerProperty()  #number seen
	geo_point		= db.GeoPtProperty() #latitude the longitude
	
	deal_status		= db.StringProperty(choices=set(["pending","active","rejected","expired"]))
	
	def dictify(self):
		'''Dictifies object for viewing its information on the phone - "myDeals" '''
		data = {
			"dealID"		: self.parent().key().__str__(),
			"img"			: self.img,
			"businessID"	: self.businessID.__str__(),
			"businessName"	: self.business_name,
			"name"  		: self.secondary_name,
			"nameType"  	: self.name_type,
			"description"   : self.description,
			"dealValue" 	: self.discount_value,
			"dealType"  	: self.discount_type,
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
#			"dateUploaded"	: self.date_uploaded,
#			"paymentTotal"	: self.payment_total(),
			"geoPoint"		: self.geo_point,
			"dealStatus"	: self.deal_status,
		}
		return data
	def increment_redeem(self):
		''' write what this does'''
		pass


class CustomerDeal(Deal):
#Sub-class of deal
#A deal that has been uploaded by a user

	gate_requirement= db.IntegerProperty()
	gate_payment_per= db.IntegerProperty()
	gate_count		= db.IntegerProperty() #+1 when count_redeemed increases to gate_requirement
	gate_max		= db.IntegerProperty()
	date_uploaded	= db.DateProperty()
	cashed_out		= db.BooleanProperty()
	
	def payment_total(self):
		return "$"+str(self.gate_count*self.gate_payment_per)
	
	def dictify(self):
		'''Dictifies object for viewing its information on the phone - "myDeals" '''
		data = {
			"dealID"		: self.parent().key().__str__(),
			"img"			: self.img,
			"businessID"	: self.businessID.__str__(),
			"businessName"	: self.business_name,
			"name"  		: self.secondary_name,
			"nameType"  	: self.name_type,
			"description"   : self.description,
			"dealValue" 	: self.discount_value,
			"dealType"  	: self.discount_type,
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
			"paymentTotal"	: self.payment_total(),
			"geoPoint"		: self.geo_point,
			"dealStatus"	: self.deal_status,
			"cashedOut"		: self.cashed_out
		}
		return data


class Category(db.Model):
#Child of deal
#Maps primary categories to deals
	primary_cat		= db.StringProperty()
#	dealID 			= db.ReferenceProperty()

class Favorite(db.Model):
#child of user
	dealID			= db.StringProperty() #CHANGE TO REFERENCEPROPERTY FOR PRODUCTION
	primary_cat		= db.StringProperty()


class EmptySetResponse(db.Model):
#root class
	primary_cat		= db.StringProperty()
	img				= db.BlobProperty()
	index			= db.IntegerProperty()
	
#functions!
def phoneDealFormat(deal):
	#map object properties to dictionary
	data = {"businessID"	: str(deal.businessID),
			"businessName"	: deal.business_name,
			"dealID"		: str(deal.parent().key()),
			"nameType"  	: deal.name_type,
			"name"  		: deal.secondary_name,
			"description"   : deal.description,
			"dealType"  	: deal.discount_type,
			"dealValue" 	: deal.discount_value,
			"endValue"  	: deal.count_end,
			"imgPath"		: deal.img_path,
			"dealOrigin"	: deal.deal_origin}
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

def phone_my_deal_format(deal):
	data = {
		
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
		"name_type"		: deal.name_type,
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
