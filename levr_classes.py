import webapp2
import datetime
from google.appengine.ext import db


class Customer(db.Model):
	#key_name is uid
	uid 			= db.StringProperty()
	email 			= db.EmailProperty()
	pw 				= db.StringProperty()

#deal_redeemed 	= db.ListProperty(str) #list of deal keys
#^^^would need another assoc table 

class Business(db.Model):

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
    
    contact_owner 	= db.StringProperty()
    contact_phone 	= db.PhoneNumberProperty()
    
    
class Customer(db.Model):
	uid				= db.StringProperty()
	email 			= db.EmailProperty()
	pw 				= db.StringProperty()

	signup_date 	= db.DateTimeProperty()
	business_name 	= db.StringProperty()

	address_line1 	= db.StringProperty()
	address_line2 	= db.StringProperty()
	city			= db.StringProperty()
	state 			= db.StringProperty()
	zip_code		= db.StringProperty()

	contact_owner 	= db.StringProperty()
	contact_email 	= db.EmailProperty()
	contact_phone 	= db.PhoneNumberProperty()

class Category(db.Model):
#Maps primary categories to deals
	primary_cat		= db.StringProperty()
	dealID 			= db.ReferenceProperty()

class Favorite(db.Model):
	uid				= db.StringProperty() #CHANGE TO REFERENCEPROPERTY FOR PRODUCTION
	dealID			= db.StringProperty() #CHANGE TO REFERENCEPROPERTY FOR PRODUCTION
	primary_cat		= db.StringProperty()

class Deal(db.Model):
	#key name is deal id
	#deal information
	
	deal_status		= db.StringProperty(choices=set(["pending","active","expired"]))
	img				= db.BlobProperty()
	
	businessID 		= db.ReferenceProperty #uid
	business_name 	= db.StringProperty() #name of business

	secondary_name 	= db.StringProperty() #secondary category
	name_type 		= db.StringProperty(choices=set(["specific","category"])) #category or single item

	description 	= db.StringProperty(multiline=True) #description of deal
	discount_type 		= db.StringProperty(choices=set(["percent","monetary","free"])) #percent, monetary, free
	discount_value 		= db.FloatProperty() #number, -1 if free
	
	deal_origin		= db.StringProperty(choices=set(["internal","external"]))
	count_end 		= db.IntegerProperty()  #max redemptions
	count_redeemed 	= db.IntegerProperty() 		#total redemptions
	count_seen 		= db.IntegerProperty()  #number seen

	date_start 		= db.DateProperty() #start date
	date_end 		= db.DateProperty()
	img_path		= db.StringProperty()   #string path to image
	city 			= db.StringProperty()  #optional

class EmptySetResponse(db.Model):
	primary_cat		= db.StringProperty()
	img				= db.BlobProperty()
	index			= db.IntegerProperty()
	
#functions!
def phoneDealFormat(deal):
	#map object properties to dictionary
	data = {"businessID"	: deal.businessID,
			"businessName"	: deal.business_name,
			"dealID"		: deal.dealID,
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

def webBusinessFormat(business):
	data = {
		"email"			: business.email,
		"password"		: business.pw,
		"businessName"	: business.business_name,
		"address1"		: business.address_line1,
		"address2"		: business.address_line2,
		"city"			: business.city,
		"state"			: business.state,
		"zipCode"		: business.zip_code,
		"ownerName"		: business.contact_owner,
		"phone"			: business.contact_phone
	}
	return data
