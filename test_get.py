import webapp2
import json
import levr_classes as levr
from google.appengine.ext import db

class phone(webapp2.RequestHandler):
	def post(self):
		
		#decode the input JSON and pull out the action parameter
		decoded = json.loads(self.request.body)
		action = decoded["action"]
		
		#switch action
		if action == "autoCompleteList":
			toEcho = {"success":0,"data":"some data!"}
		
		#***************dealResults************************************************
		elif action == "dealResults":
			
			#hard-code the number of results
			numResults = 20;
			
			#grab primaryCat from the request body
			primaryCat = decoded["in"]["primaryCat"]
			#exception if empty
			
			#query the database for all deals with a matching primaryCat
			q = db.GqlQuery("SELECT * FROM Category WHERE primary = :primary",primary=primaryCat)
			#q = db.GqlQuery("SELECT * FROM Category")
			
			#define an empty "dealResults" LIST, and initialize the counter to 0
			dealResults = []
			resultsPushed = 0
			
			#iterate over the results
			for category in q:
				#break if results limit is hit
				if resultsPushed == numResults:
					break
				#grab the appropriate deal
				result = levr.Deal.get_by_key_name(category.deal_key)
				#trade an object for a phone-formatted dictionary
				deal = levr.phoneFormat(result)
				#push the primary onto the dictionary
				deal['primaryCat'] = category.primary
				#push the whole dictionary onto a list
				dealResults.append(deal)
				#increment the counter
				resultsPushed += 1
			#if not 20 yet, continue adding deals up to numResults
			if resultsPushed < numResults:
				#place the null object, to signify to ethan to place a heading
				dealResults.append(None)
				#grab <numResults> random deals, push them one-by-one (for now)
				#later refine this to be actual recommendations
				q = levr.Category.gql("")
				for category in q:
					#break if results limit is hit
					if resultsPushed == numResults:
						break
					#grab the appropriate deal
					result = levr.Deal.get_by_key_name(category.deal_key)
					#trade an object for a phone-formatted dictionary
					deal = levr.phoneFormat(result)
					#push the primary onto the dictionary
					deal['primaryCat'] = category.primary
					#push the whole dictionary onto a list
					dealResults.append(deal)
					#increment the counter
					resultsPushed += 1
			#echo back success!
			toEcho = {"success":1,"data":dealResults}
			
		#***************getUserFavs************************************************
		elif action == "getUserFavs":
			'''
			Grabs all of the favorites of a user - only data to show on list
			input : uid
			output: name, description, dealValue, dealType, imgPath, businessName, primaryCat
			'''
			uid = decoded["in"]["uid"]
			#grabs the deal key name and primary category from table
			q1 = levr.Favorite.gql("WHERE uid=:1",uid)
			#init key,cats list
			keys,cats = [],[]
			#grab deal keys from each favorite
			for fav in q1:
				keys.append(fav.dealID)
				cats.append(fav.primary_cat)
			
			#grab all the deal data with the keys
			deals = levr.Deal.get_by_key_name(keys)
			#data is deal obj array
			data = []
			#grab data from each deal
			for idx,deal in enumerate(deals):
				#print deal.__dict__
				#send to format function - package for phone
				data.append(levr.phoneDealFormat(deal))
				
			toEcho = {"success":0,"data":data}
		elif action == "addFav":
			'''
			User pressed add favorite button = add favorite mapping
			input: dealID,uid,primaryCat
			output: success = bool
			'''
			uid = decoded["in"]["uid"]
			dealID = decoded["in"]["dealID"]
			primary_cat = decoded["in"]["primaryCat"]
			
			#create new Favorite instance
			fav = levr.Favorite()
			#populate data in new favorite
			fav.uid 		= uid
			fav.dealID 		= dealID
			fav.primary_cat = primary_cat
			#place in database
			fav.put()
			
			toEcho = {"success":0}
		elif action == "delFav":
			'''
			User presses delete favorite button - delete favorite mapping
			input: dealID,uid,primaryCat
			output: success = bool
			'''
			uid = decoded["in"]["uid"]
			dealID = decoded["in"]["dealID"]
			primary_cat = decoded["in"]["primaryCat"]
			q = levr.Favorite.gql("WHERE uid=:1 and dealID=:2 and primary_cat=:3",uid, dealID, primary_cat)
			#fav_to_delete = levr.Favorite.gql("WHERE uid=:u,dealID=:d, primary_cat=:p",u=uid,d=dealID,p=primary_cat)
			
			for fav in q:
				print fav.__dict__
				fav.delete()
			
			toEcho = {"success":0,"data":"some data!"}
		elif action == "getOneDeal":
			'''
			Information to show on the deal information screen.
			input	: primaryCat,dealID
			output	: json object of all information necessary to describe deal
			'''
			primaryCat = decoded["in"]["primaryCat"]
			dealID = decoded["in"]["dealID"]
			
			d = levr.Deal.get_by_key_name(dealID)
			if d.secondary_is_category:
				d.cat_or_name = "category"
			else:
				d.cat_or_name = "itemName"
			data = {"businessID"    : d.business_key,
					"nameType"      : d.cat_or_name,
					"secondaryCat"  : "none",
					"name"          : d.secondary_name,
					"description"   : d.description,
					"dealType"      : d.offer_type,
					"dealValue"     : d.offer_value,
					"endValue"      : d.count_end,
					"imgPath"       : d.image,
					"city"          : d.region,
					"dealOrigin"    : "internal",
					"primaryCat"    : primaryCat}
			
			toEcho = {"success":0,"data":data}
		elif action == "getRedeem":
			toEcho = {"success":0,"data":"some data!"}
		elif action == "addRedeem":
			toEcho = {"success":0,"data":"some data!"}
		elif action == "delRedeem":
			toEcho = {"success":0,"data":"some data!"}
		else:
			toEcho = {"success":0,"data":"some data!"}
		
		#write the response
		self.response.out.write(json.dumps(toEcho))

app = webapp2.WSGIApplication([('/get', phone)],debug=True)
