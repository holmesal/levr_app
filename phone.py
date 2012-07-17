import webapp2
import json
import sys
import math
from datetime import datetime
#from dateutil.relativedelta import relativedelta
import logging
import levr_classes as levr
import levr_utils
from google.appengine.ext import db
from google.appengine.api import images

class phone(webapp2.RequestHandler):
	def post(self):
		
		#decode the input JSON and pull out the action parameter
		try:
			decoded = json.loads(self.request.body)
		except:
			logging.error("Could not parse input JSON. Input passed: " + self.request.body)
			sys.exit()
			
		#pull out the action parameter
		try:
			action = decoded["action"]
		except KeyError:
			logging.error("Could not parse action. Input passed: " + self.request.body)
			sys.exit()
		#switch action
		#***************signup************************************************
		if action == "signup":
			#grab email/password from request body
			try:
				email = decoded["in"]["email"]
				alias = decoded["in"]["alias"]
				pw = decoded["in"]["pw"]
			except:
				logging.error("Could not grab email/password/alias. Input passed: " + self.request.body)
				sys.exit()
				
			#attempt signup
			toEcho = levr_utils.signupCustomer(email,alias,pw)
		
		#***************login************************************************
		elif action == "login":
			#grab email/password from request body
			try:
				email_or_owner = decoded["in"]["email_or_owner"]
				pw = decoded["in"]["pw"]
			except:
				logging.error("Could not grab email/password. Input passed: " + self.request.body)
				
			#check for matches
			toEcho = levr_utils.loginCustomer(email_or_owner,pw)
			'''toEcho = {"success":False,"error":"Incorrect email or password"}
			q = levr.Customer.gql("WHERE email = :email AND pw = :pw",email = email,pw=pw)
			for result in q:
				toEcho = {"success":True,"uid":result.key().__str__()}'''
			
		#***************autoCompleteList************************************************
		elif action == "autoCompleteList":
			cats = ['shirt','coat','bonobos','apples']
			toEcho = {"success":True,"data":cats}
		
		#***************dealResults************************************************
		elif action == "dealResults":
			
			#grab primaryCat from the request body
			try:
				primaryCat = decoded["in"]["primaryCat"]
				start = decoded["in"]["start"]
				numResults = decoded["in"]["size"]
			except:
				logging.error("Could not grab primary category. Input passed: " + self.request.body)
			
			#query the database for all deals with a matching primaryCat
			q = levr.Category.gql("WHERE primary_cat=:1",primaryCat).fetch(int(numResults),offset=int(start))
#			logging.info(q.count())
			#define an empty "dealResults" LIST, and initialize the counter to 0
			dealResults = []
			resultsPushed = 0
			#initialize isEmpty to 1
			isEmpty = 1
			#iterate over the results
			#Want to grab deal information for each category
			for category in q:
				#set isEmpty to 1
				
				#break if results limit is hit
				if resultsPushed == numResults:
					break
				#grab the parent deal key so we can grab the info from it
				d = category.parent().key()
				#grab the appropriate deal parent
				result = levr.Deal.get(d)
				if result.deal_status == 'active':
					isEmpty = 0
					#trade an object for a phone-formatted dictionary
					deal = levr.phoneFormat(result,'list')
					#push the primary onto the dictionary
					deal['primaryCat'] = category.primary_cat
					#push the whole dictionary onto a list
					dealResults.append(deal)
					#increment the counter
					resultsPushed += 1
				else:
					pass
			#if isempty is true, send back suggested searches instead
			if isEmpty == 1:
				#go get (all) suggested searches
				q = levr.EmptySetResponse.all()
				#sory by index
				q.order('index')
				#loop through and append to data
				for result in q:
					searchObj = {"primaryCat":result.primary_cat,"img_key":result.key()}
					#push to stack
					dealResults.append(searchObj)
					
			#else, isempty is false, append some related deals
			else:
				#THIS WILL BE REPLACED WITH A STANDARD RESPONSE
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
						result = levr.Deal.get(category.parent().key())
						#trade an object for a phone-formatted dictionary
						deal = levr.phoneFormat(result,'list')
						#push the primary onto the dictionary
						deal['primaryCat'] = category.primary_cat
						#push the whole dictionary onto a list
						dealResults.append(deal)
						#increment the counter
						resultsPushed += 1
			#echo back success!
			toEcho = {"success":True,"data":dealResults,"isEmpty":isEmpty}
			
		#***************getUserFavs************************************************
		elif action == "getUserFavs":
			'''
			Grabs all of the favorites of a user - only data to show on list
			input : uid
			output: name, description, dealValue, dealType, imgPath, businessName, primaryCat
			'''
			uid = decoded["in"]["uid"]
			#grabs the deal key name and primary category from table
			q1 = levr.Favorite.gql("WHERE ANCESTOR IS :1",uid)
#			q1 = levr.Favorite.gql("WHERE uid=:1",uid)
			#init key,cats list
			logging.info(q1)
			deal_keys,cats = [],[]
			#grab deal keys from each favorite
			for fav in q1:
#				logging.info(fav)
				deal_keys.append(fav.dealID)
				cats.append(fav.primary_cat)
			
			#grab all the deal data with the keys
			deals = levr.Deal.get(deal_keys)
			
			#data is deal obj array
			data = []
			#grab data from each deal
			for idx,deal in enumerate(deals):
				self.response.out.write(deal.__dict__)
				#send to format function - package for phone
				deal_stack = levr.phoneFormat(deal,'list')
				deal_stack.update({"primaryCat":cats[idx]})
				data.append(deal_stack)
#				data[idx]['primaryCat'] = cats[idx]
#			self.response.out.write(data)
			toEcho = {"success":True,"data":data}
		#ADD FAVORITE***********************************************************
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
			fav = levr.Favorite(parent=db.Key(uid))
			#populate data in new favorite
#			fav.uid 		= uid
			fav.dealID 		= dealID
			fav.primary_cat = primary_cat
			#place in database
			fav.put()
			
			toEcho = {"success":True}
		#DELETE FAVORITE********************************************************
		elif action == "delFav":
			'''
			User presses delete favorite button - delete favorite mapping
			input: dealID,uid,primaryCat
			output: success = bool
			'''
			uid = decoded["in"]["uid"]
			dealID = decoded["in"]["dealID"]
			primary_cat = decoded["in"]["primaryCat"]
			q = levr.Favorite.gql("WHERE ANCESTOR IS :1 and dealID=:2 and primary_cat=:3",uid, dealID, primary_cat)
			#fav_to_delete = levr.Favorite.gql("WHERE uid=:u,dealID=:d, primary_cat=:p",u=uid,d=dealID,p=primary_cat)
			
			for fav in q:
				fav.delete()
			
			toEcho = {"success":True}
		#***************getOneDeal************************************************
		elif action == "getOneDeal":
			'''
			Information to show on the deal information screen.
			input	: primaryCat,dealID
			output	: json object of all information necessary to describe deal
			'''
			#grab input dealID
			try:
				dealID 		= decoded["in"]["dealID"]
				primary_cat = decoded["in"]["primaryCat"]
			except:
				logging.error("Could not grab dealID AND/OR primaryCat. Input passed: " + self.request.body)
			#fetch deal
			result = levr.Deal.get(dealID)
			#convert fetched deal into dictionary
			deal = levr.phoneFormat(result,'deal')
			#push the primary onto the dictionary
			deal.update({"primaryCat":primary_cat})
			#echo back success!
			toEcho = {"success":True,"data":deal}

		elif action == "getMyDeals":
			'''
			returns all of the deals that were uploaded by the ninja
			input	: uid
			output	: list of deal objects
			'''
			try:
				uid	= decoded["in"]["uid"]
			except:
				logging.error("could not grab uid. Input passed: "+self.request.body)
			
			#grab all deal children of the user
			deals = levr.CustomerDeal.gql("WHERE ANCESTOR IS :1",uid)
			#format CUSTOMER deals
			data = [x.dictify() for x in deals]
			#I believe this will just return data:None if deals is empty
			toEcho = {"success":True,"data":data}
		elif action == "getMyStats":
			'''
			returns the user's statistics
			input	: uid
			output	: 
			'''
			try:
				uid = decoded['in']['uid']
			except:
				logging.error("could not grab uid. Input passed: "+self.request.body)
			#get user information
			user = db.get(uid)
			#format user information
			data = user.dictify()
			
			toEcho = {"success":False,"data":data}
		elif action == "redeem":
			#grab corresponding deal
			try:
				uid = decoded['in']['uid']
				dealID = decoded['in']['dealID']
			except:
				logging.error("could not grab uid/dealID. Input passed: "+self.request.body)
				sys.exit()
			
			#grab the deal
			deal = levr.Deal.get(dealID)
			#grab the customer
			customer = levr.Customer.get(uid)
			
			#don't try and redeem the same deal twice. . .
			#if dealID in customer.redemptions:
				#sys.exit()
			#increment deal "redeemed" count by 1
			deal.count_redeemed += 1
			#add deal to "redeemed" for the customer
			
			#Is this a deal uploaded by a ninja? If so, do ninja things
			if type(deal) is levr.CustomerDeal:
				#update deal ninjaStats
				deal.gate_count = int(math.floor(deal.count_redeemed / deal.gate_requirement))
				if deal.gate_count > deal.gate_max:
					#reset if over
					deal.gate_count = deal.gate_max
				#update deal.earned_total
				deal.update_earned_total()
				#put deal
				deal.put()
				#get the ninja
				ninjaKey = deal.key().parent()
				ninja = levr.Customer.get(ninjaKey)
				ninja.echo_stats()
				#update the ninja's earned amount
				ninja.update_money_earned()
				
				#update the ninja's available amount
				ninja.update_money_available()
				
				#echo stats
				ninja.echo_stats()
				deal.echo_stats()
				
				#update ninja
				ninja.put()
				
			#add to customer's redemption list
			customer.redemptions.append(dealID)
			#update customer
			customer.put()
			
			toEcho = {"success":True,"data":"some data!"}
		elif action == "cashOut":
			try:
				uid = decoded['in']['uid']
			except:
				logging.error("could not grab uid/dealID. Input passed: "+self.request.body)
				sys.exit()
			
			#grab the ninja
			ninja = levr.Customer.get(uid)
			#delete any current cashOutRequests
			q = levr.CashOutRequest.gql('WHERE ANCESTOR IS :1',ninja.key())
			for result in q:
				result.delete()
			#create a new cashOut request
			cor = levr.CashOutRequest(parent=ninja)
			cor.amount = ninja.money_available
			cor.status = 'pending'
			cor.put()
			toEcho = {"success":True}
		else:
			logging.error("Unrecognized action. Input passed: " + action)
			sys.exit()
		
		#write the response
		self.response.out.write(json.dumps(toEcho))
		
class uploadDeal(webapp2.RequestHandler):
	def post(self):
		logging.info(self.request.headers)
		logging.info('Body is next!')
#		logging.info(self.request.body)
		
		#create alias for self.request.get
		inputs			= self.request.get
		#grab existing business
		business_name	= inputs('businessName')
		geo_point		= inputs('geoPoint')
		logging.info(geo_point)
		geo_point		= levr.geo_converter(geo_point)
		logging.info(geo_point)
		business = levr.Business.gql("WHERE business_name=:1 and geo_point=:2", business_name, geo_point).get()
		#if a business doesn't exist in db, then create a new one
		if not business:
			business = levr.Business()
		
		#populate entity
		
		business.geo_point		= geo_point
		business.business_name	= business_name
		business.address_line1	= inputs('addressLine1')
		business.city			= inputs('city')
		business.state			= inputs('state')
		business.zip_code		= inputs('zip')
#		put business in db
		business.put()
		logging.info(business)
		
		
		uid = inputs('uid')
		logging.info(uid)
		#create new deal object as child of the uploader Customer
		deal 				= levr.CustomerDeal(parent='agtkZXZ-Z2V0bGV2cnIOCxIIQ3VzdG9tZXIYEQw')
		deal.img			= inputs('img')			#D
		deal.businessID		= business.key().__str__()
		deal.business_name	= business_name
		deal.secondary_name	= inputs('name') #### check name!!!
		deal.deal_status	= 'pending'
		deal.geo_point		= geo_point
		#set expiration date to one week from now
		#only need date, not time for this
		#deal.date_end		= datetime.now().date() + relativedelta(days=+7)
#		date_uploaded		= automatic
		
		#put in DB
		deal.put()
		
		#return deal id
		dealID = deal.key().__str__()
		toEcho = {"success":True,"dealID":dealID}
		self.response.out.write(json.dumps(toEcho))
		
class phone_log(webapp2.RequestHandler):
	def post(self):
		logging.error(self.request.body)
		
class images(webapp2.RequestHandler):
	def get(self):
		#get inputs
		try:
			dealID = self.request.get('dealID')
			size = self.request.get('size')
		except:
			logging.error('could not parse dealID or size. . . you passed:'+self.request.body)
			sys.exit()
		logging.info(dealID)
		logging.info(size)
		#grab deal
		deal = levr.Deal.get(dealID)
		#grab image
		image = deal.img
		
		self.response.headers['Content-Type'] = 'image/png'
		self.response.out.write(image)
		
		#crop to square
		width = image.width
		height = image.height
		loss = height-width
		offset = loss/2
		fractional = offset/height
		image = image.crop(0,(1-fractional),1,fractional)

		self.response.out.write(image)
		
		#resize?
		if size == 'list':
			pass
		else:
			pass
			

app = webapp2.WSGIApplication([('/phone', phone),('/phone/log', phone_log),('/phone/uploadDeal', uploadDeal),('/phone/images.*', images)],debug=True)
