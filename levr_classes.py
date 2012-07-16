#import webapp2
#import datetime
from google.appengine.ext import db
from google.appengine.ext.db import polymodel

class Customer(db.Model):
#root class
	#key_name is uid
	email 			= db.EmailProperty()
	pw 				= db.StringProperty()
	alias			= db.StringProperty()
	#stats
	money_earned	= db.FloatProperty()
	money_saved		= db.FloatProperty()
	
	def format_stats(self):
		data = {
			"alias"			: self.alias,
			"money_earned"	: self.money_earned,
			"money_saved"	: self.money_saved
		}
		return data
	
#class Redemption(db.Model):
#child of customer
#	dealID
	


#deal_redeemed 	= db.ListProperty(str) #list of deal keys
#^^^would need another assoc table 

class Business(db.Model):
#root class
	#key is businessID
    email 			= db.StringProperty()
    pw 				= db.StringProperty()
    
    businessID		= db.StringProperty()
    signup_date 	= db.DateTimeProperty()
    business_name 	= db.StringProperty()
    
    address_line1 	= db.StringProperty()
    address_line2 	= db.StringProperty()
    city			= db.StringProperty()
    state 			= db.StringProperty()
    zip_code		= db.StringProperty()
    
    alias 	= db.StringProperty()
    contact_phone 	= db.PhoneNumberProperty()
    
    
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
	img_path		= db.StringProperty()   #string path to image
	city 			= db.StringProperty()  #optional
	count_end 		= db.IntegerProperty()  #max redemptions
	count_redeemed 	= db.IntegerProperty() 	#total redemptions
	count_seen 		= db.IntegerProperty()  #number seen


class CustomerDeal(Deal):
#Sub-class of deal
#A deal that has been uploaded by a user
	deal_status		= db.StringProperty(choices=set(["pending","active","expired"]))
	gate_requirement= db.IntegerProperty()
	gate_payment_per= db.IntegerProperty()
	gate_count		= db.IntegerProperty()
	gate_max		= db.IntegerProperty()
	
	def payment_total(self):
		return "$"+str(self.gate_count*self.gate_payment_per)
	
	def format_my_deals(self):
		data = {
			"businessID"	: str(self.businessID),
			"businessName"	: self.business_name,
			"dealID"		: str(self.parent().key()),
			"nameType"  	: self.name_type,
			"name"  		: self.secondary_name,
			"description"   : self.description,
			"dealType"  	: self.discount_type,
			"dealValue" 	: self.discount_value,
			"endValue"  	: self.count_end,
			"imgPath"		: self.img_path,
			"deal_status"	: self.deal_status,
			"gate_requirement": self.gate_requirement,
			"gate_payment_per": self.gate_payment_per,
			"gate_count"	: self.gate_count,
			"gate_max"		: self.gate_max,
			"payment_total"	: self.payment_total()
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
