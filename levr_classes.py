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
<<<<<<< HEAD
	#key is businessID
    user 			= db.UserProperty()
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
    contact_email 	= db.EmailProperty()
    contact_phone 	= db.PhoneNumberProperty()
    
=======
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

>>>>>>> Phone login and signup functionality!
class Category(db.Model):
#Maps primary categories to deals
	primary_cat		= db.StringProperty()
	dealID 			= db.StringProperty()

class Favorite(db.Model):
	uid				= db.StringProperty()
	dealID			= db.StringProperty()
	primary_cat		= db.StringProperty()

class Deal(db.Model):
	#key name is deal id
	#deal information
	businessID 		= db.StringProperty() #uid
	dealID			= db.StringProperty()
	business_name 	= db.StringProperty() #name of business

	secondary_name 			= db.StringProperty() #secondary category
	secondary_is_category 	= db.BooleanProperty() #category or single item

	description 	= db.StringProperty(multiline=True) #description of deal

	deal_type 		= db.StringProperty(choices=set(["percent","monetary","free"])) #percent, monetary, free
	deal_value 		= db.FloatProperty() #number, -1 if free
	deal_rating 	= db.RatingProperty() #deal rating
	deal_origin		= db.StringProperty(choices=set(["internal","external"]))

	count_max 		= db.IntegerProperty()  #max redemptions
	count_redeemed 	= db.IntegerProperty() 		#total redemptions
	count_seen 		= db.IntegerProperty()  #number seen

	date_start 		= db.DateProperty() #start date
	date_end 		= db.DateProperty()
	img_path		= db.StringProperty()   #string path to image
	city 			= db.StringProperty()  #optional

#functions!
def phoneDealFormat(deal):
	#check if the secondary parameter is a category or a single item
	if deal.secondary_is_category:
		deal.cat_or_name = "category"
	else:
		deal.cat_or_name = "itemName"
	
	#map object properties to dictionary
	data = {"businessID": deal.businessID,
			"businessName"	: deal.business_name,
			"dealID"		: deal.dealID,
			"nameType"  : deal.cat_or_name,
			"name"  : deal.secondary_name,
			"description"   : deal.description,
			"dealType"  : deal.deal_type,
			"dealValue" : deal.deal_value,
			"endValue"  : deal.count_max,
			"imgPath"		: deal.img_path,
			"dealOrigin": deal.deal_origin}
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
