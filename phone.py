import webapp2
import json
import math
from datetime import datetime
#from datetime import timedelta
#from dateutil.relativedelta import relativedelta
import logging
import levr_classes as levr
import levr_encrypt as enc
import levr_utils
from google.appengine.ext import db
from google.appengine.api import images
#from google.appengine.api import mail
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class phone(webapp2.RequestHandler):
	def post(self):
		#decode the input JSON and pull out the action parameter
		try:
			decoded = json.loads(self.request.body)
			action = decoded["action"]
			
			#switch action
			#***************signup************************************************
			if action == "signup":
				#grab email/password from request body
				email = decoded["in"]["email"]
				alias = decoded["in"]["alias"]
				pw = decoded["in"]["pw"]
				toEcho = levr_utils.signupCustomer(email,alias,pw)
		
			#***************login*************************************************
			elif action == "login":
			#grab email/password from request body
				email_or_owner = decoded["in"]["email_or_owner"]
				pw = decoded["in"]["pw"]
				
				toEcho = levr_utils.loginCustomer(email_or_owner,pw)
#***************dealResults************************************************
			elif action == "dealResults":
				#grab primaryCat from the request body
				primaryCat 	= decoded["in"]["primaryCat"]
					#search term
#				start 		= decoded["in"]["start"]
					#starting index of search results
					#!!!not used
				numResults 	= decoded["in"]["size"]
					#length of search results list
				
				
				#normalize search query
				primaryCat = primaryCat.lower()
				
				
				#build search query
				q = levr.Deal.all()
				#only active deals
				q.filter('deal_status','active')
				#primaryCat will be mapresults to return everything
				if primaryCat == 'all':
					#get all deals - no filter
					logging.debug('all')
				else:
					logging.debug('not all')
					#normalize search query
					primaryCat = primaryCat.lower()
					#otherwise, search based on the tags
					tags = levr.tagger(primaryCat)
					logging.debug(tags)
					#grab all deals where primary_cat is in tags
					for tag in tags:
						q.filter('tags',tag)
				#finally, sort the query
				#sort_property = 'rank'
				#q.order(sort_property)
					
				
				
#				logging.debug(q.__str__())
				logging.debug(q.get().__str__())

				#define an empty "dealResults" LIST, and initialize the counter to 0
				dealResults = []
				resultsPushed = 0
				#initialize isEmpty to 1
				isEmpty = True
				#iterate over the results
				#Want to grab deal information for each category
				for result in q:
					logging.info('Rank: ' + str(result.rank))
					#break if results limit is hit
					if resultsPushed == numResults:
						break
					isEmpty = False
					#trade an object for a phone-formatted dictionary
					deal = levr.phoneFormat(result,'list',primaryCat)
					#indicate that this is not a sentinel
					deal['isSentinel'] = False
					#push the whole dictionary onto a list
					dealResults.append(deal)
					#increment the counter
					resultsPushed += 1

				#if isempty is true, send back suggested searches instead
				if isEmpty == False:
					dealResults.append({"isSentinel":True})
		
				#go get (all) suggested searches
				q = levr.EmptySetResponse.all()
				#sory by index
				q.order('index')
				#loop through and append to data
				for result in q:
					searchObj = {"isSentinel":False,
								"primaryCat":result.primary_cat,
								"imgURL":"http://getlevr.appspot.com/phone?size=emptySet&dealID=" + enc.encrypt_key(result.key())
					} 
					#push to stack
					dealResults.append(searchObj)
				#get notifications
#				ninja = levr.Customer.get(uid)
#				notifications = ninja.get_notifications()
				#echo back success!
				toEcho = {"success":True,"data":dealResults,"isEmpty":isEmpty}#,"notifications":notifications}
			#***************getUserFavs************************************************
			elif action == "getUserFavs":
				'''
				Grabs all of the favorites of a user - only data to show on list
				input : uid
				output: name, description, dealValue, dealType, imgPath, businessName, primaryCat
				'''
				uid = enc.decrypt_key(decoded["in"]["uid"])
			
				#grabs the deal key name and primary category from table
				q1 = levr.Favorite.gql("WHERE ANCESTOR IS :1",uid)
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
					#send to format function - package for phone
					deal_stack = levr.phoneFormat(deal,'list',cats[idx])
#					deal_stack.update({"primaryCat":cats[idx]})
					data.append(deal_stack)
				#get notifications
				ninja = levr.Customer.get(uid)
				notifications = ninja.get_notifications()
				toEcho = {"success":True,"data":data,'notifications':notifications}
			#ADD FAVORITE***********************************************************
			elif action == "addFav":
				'''
				User pressed add favorite button = add favorite mapping
				input: dealID,uid,primaryCat
				output: success = bool
				'''
				uid 		= enc.decrypt_key(decoded["in"]["uid"])
				dealID 		= enc.decrypt_key(decoded["in"]["dealID"])
				primary_cat	= decoded["in"]["primaryCat"]

				#create new Favorite instance
				fav = levr.Favorite(parent=db.Key(uid))
				#populate data in new favorite
	#			fav.uid 		= uid
				fav.dealID 		= dealID
				fav.primary_cat = primary_cat
				#place in database
				fav.put()
				
				#get notifications
				ninja = levr.Customer.get(uid)
				notifications = ninja.get_notifications()
				toEcho = {"success":True,"notifications":notifications}
			#DELETE FAVORITE********************************************************
			elif action == "delFav":
				'''
				User presses delete favorite button - delete favorite mapping
				input: dealID,uid,primaryCat
				output: success = bool
				'''
				uid 	= enc.decrypt_key(decoded["in"]["uid"])
				dealID 	= enc.decrypt_key(decoded["in"]["dealID"])
				q = levr.Favorite.gql("WHERE ANCESTOR IS :1 and dealID=:2",uid, dealID)
				for fav in q:
					fav.delete()
				#get notifications
				ninja = levr.Customer.get(uid)
				notifications = ninja.get_notifications()
				toEcho = {"success":True,"notificaions":notifications}
			#***************getOneDeal************************************************
			elif action == "getOneDeal":
				'''
				Information to show on the deal information screen.
				input	: primaryCat,dealID
				output	: json object of all information necessary to describe deal
				'''
				#grab input dealID
				dealID 		= enc.decrypt_key(decoded["in"]["dealID"])
				primary_cat = decoded["in"]["primaryCat"]
				#fetch deal
				result = levr.Deal.get(dealID)
				#convert fetched deal into dictionary
				deal = levr.phoneFormat(result,'deal')
				#push the primary onto the dictionary
				deal.update({"primaryCat":primary_cat})
				#echo back success!
				
#				#get notifications
#				ninja = levr.Customer.get(uid)
#				notifications = ninja.get_notifications()
				toEcho = {"success":True,"data":deal}#,"notificaions":notifications}

			elif action == "getMyDeals":
				'''
				returns all of the deals that were uploaded by the ninja
				input	: uid
				output	: list of deal objects
				'''
				uid	= enc.decrypt_key(decoded["in"]["uid"])
				logging.info(uid)
				#grab all deal children of the user
				deals = levr.CustomerDeal.gql("WHERE ANCESTOR IS :1 ORDER BY date_uploaded DESC",uid)
				#format CUSTOMER deals
				data = [levr.phoneFormat(x,'myDeals') for x in deals]
				#I believe this will just return data:None if deals is empty
				
				#flush their notifications
				ninja = levr.Customer.get(uid)
#				ninja.flush_new_redeem_count()
#				ninja.put()
				#get new notifications
				notifications = ninja.get_notifications()
				
				#Grab their cash out requests, if they exist
				cor_q = levr.CashOutRequest.gql("WHERE ANCESTOR IS :1 AND status=:2",uid,'pending')
				cor = cor_q.get()
				if cor != None:
					notifications["isPendingCashOut"] = True
				else:
					notifications["isPendingCashOut"] = False
				notifications["pendingCashOutAmount"] = ninja.money_available
				toEcho = {"success":True,"data":data,"notifications":notifications}
				
			elif action == "getMyStats":
				'''
				returns the user's statistics
				input	: uid
				output	: 
				'''
				uid = enc.decrypt_key(decoded['in']['uid'])
				#get user information
				user = db.get(uid)
				#format user information
				data = user.get_stats()
				
				#get new notifications
				notifications = user.get_notifications()
				toEcho = {"success":True,"data":data,"notifications":notifications}
				
			elif action == "checkRedeem":
				#grab corresponding deal
				uid 	= enc.decrypt_key(decoded['in']['uid'])
				dealID 	= enc.decrypt_key(decoded['in']['dealID'])
				
				#grab the customer
				customer = levr.Customer.get(uid)
				
				#new notifications?
				notifications = customer.get_notifications()
				#don't try and redeem the same deal twice. . .
				#if dealID in customer.redemptions:
					#toEcho = {"success":False,"data":{"message":"You have already redeemed this deal."},"notifications":notifications}
				#else:
					#toEcho = {"success":True,"notifications":notifications}
				
				#!!!!!!!!REMOVE THIS WHEN CHECKING IS PUT BACK IN	
				toEcho = {"success":True,"notifications":notifications}
				
			elif action == "getRedeemScreen":
				#grab inputs
				dealID 	= enc.decrypt_key(decoded['in']['dealID'])
				
				#grab the deal
				deal = levr.Deal.get(dealID)
				
				#format the deal
				data = levr.phoneFormat(deal,'dealsScreen')
				
				#echo
				toEcho = {"success":True,"data":data}
			
			elif action == "redeem":
				#grab corresponding deal
				uid 	= enc.decrypt_key(decoded['in']['uid'])
				dealID 	= enc.decrypt_key(decoded['in']['dealID'])
				
				#grab the deal
				deal = levr.Deal.get(dealID)
				#grab the customer
				customer = levr.Customer.get(uid)
			
				#don't try and redeem the same deal twice. . .
				#if dealID in customer.redemptions:
					#raise Exception('Cannot redeem a deal more than once')
				#increment deal "redeemed" count by 1
				deal.count_redeemed += 1
				#add deal to "redeemed" for the customer
				customer.redemptions.append(dealID)
				###get customer new_redemptions if they are a ninja
				notifications = customer.get_notifications()
				#update customer
				customer.put()
				
				#Is this a deal uploaded by a ninja? If so, do ninja things
				if type(deal) is levr.CustomerDeal:
					#update deal ninjaStats
					deal.gate_count = int(math.floor(deal.count_redeemed / deal.gate_requirement))
					if deal.gate_count > deal.gate_max:
						#reset if over
						deal.gate_count = deal.gate_max
					#update deal.earned_total
					difference = deal.update_earned_total()
					#put deal
					deal.put()
					#get the ninja
					ninjaKey = deal.key().parent()
					ninja = levr.Customer.get(ninjaKey)
					
					#update the ninja's earned amount
					ninja.update_money_earned(difference)
					
					#update the ninja's available amount
					ninja.update_money_available(difference)
					
					#notify the ninja of new redemptions
					ninja.increment_new_redeem_count()
					
					#echo stats
					ninja.echo_stats()
					deal.echo_stats()

					#update ninja
					ninja.put()
				else:
					#deal is owned by a business - FOR THE FUTURE!
					logging.info('Business!')
					pass	
			
				toEcho = {"success":True,"notifications":notifications}
			elif action == "cashOut":
				uid = enc.decrypt_key(decoded['in']['uid'])
			
				#grab the ninja
				ninja = levr.Customer.get(uid)
				#delete any current cashOutRequests
				q = levr.CashOutRequest.gql('WHERE ANCESTOR IS :1 AND status=:2',ninja.key(),'pending')
				for result in q:
					result.delete()
				#create a new cashOut request
				cor = levr.CashOutRequest(parent=ninja)
				cor.amount = ninja.money_available
				#get notifications
				notifications = ninja.get_notifications()
				if cor.amount == 0:
					toEcho = {"success":False,"data":{"message":"You need to earn something before you can cash out!","notifications":notifications}}
				else:
					cor.status = 'pending'
					cor.date_created = datetime.now()
					cor.put()
					toEcho = {"success":True,"notifications":notifications}
			
			elif action == "getTargetedBusinesses":
				#get businesses that have property targeted = True
				businesses = levr.Business.gql('WHERE targeted = True').fetch(None) #fetches all of them
				
				data = []
				for business in businesses:
					data.append({
						"businessName"	: business.business_name,
						"geoPoint"		: business.geo_point,
						"vicinity"		: business.vicinity
					})
				
				toEcho = {"success":True,"data":data}
			
			elif action == "fetchUploadURL":
				upload_url = blobstore.create_upload_url('/phone/uploadDeal')
				logging.debug(upload_url)
				toEcho = {"success":True, "data":{"url":upload_url}}

			elif action == "checkBounty":
				where = "College campuses in Boston, MA"
				what = "Offers on food, drink, clothing, and entertainment"
				toEcho = {"success":True,"data":{"where":where,"what":what}}

			else:
				raise Exception('Unrecognized action')
			############ END OF ACTION FILE PART!!! JSONIFY!!!
		except:
			levr.log_error(self.request.body)
			toEcho = {"success":False}
		finally:
			try:
				logging.info(json.dumps(toEcho))
				self.response.out.write(json.dumps(toEcho))
			except:
				#catches the case where toEcho cannot be parsed as json
				self.response.out.write(json.dumps({"success":False}))
				levr.log_error('json is not parseable')


class uploadDeal(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		share_url = levr_utils.dealCreate(self,'phone')
		toEcho = {"success":True,"shareURL":share_url}
		self.response.out.write(json.dumps(toEcho))
class phone_log(webapp2.RequestHandler):
	def post(self):
		pass
		
class img(webapp2.RequestHandler):
	def get(self):
		#get inputs
		'''Returns ONLY an image for a deal specified by dealID
		Gets the image from the blobstoreReferenceProperty deal.img'''
		try:
			dealID 	= enc.decrypt_key(self.request.get('dealID'))
			size 	= self.request.get('size')
			logging.debug(dealID)
			logging.debug(size)
			
			#get deal object
			deal = db.get(dealID)

			#get the blob
			blob_key = deal.img
			
			logging.debug(dir(blob_key.properties))
			#read the blob data into a string !!!! important !!!!
			blob_data = blob_key.open().read()
			
			#pass blob data to the image handler
			img			= images.Image(blob_data)
			#get img dimensions
			img_width	= img.width
			img_height	= img.height
			logging.debug(img_width)
			logging.debug(img_height)
			
			#define output parameters
			if size == 'dealDetail':
				#view for top of deal screen
				aspect_ratio 	= 3. 	#width/height
				output_width 	= 640.	#arbitrary standard
			elif size == 'list':
				#view for in deal or favorites list
				aspect_ratio	= 1.	#width/height
				output_width	= 200.	#arbitrary standard
			elif size == 'fullSize':
				#full size image
				aspect_ratio	= float(img_width)/float(img_height)
				output_width	= float(img_width)
	#			self.response.out.write(deal.img)
			elif size == 'webShare':
				aspect_ratio	= 4.
				output_width	= 600.
			elif size == 'facebook':
				aspect_ratio 	= 1.
				output_width	= 250.
			elif size == 'emptySet':
				aspect_ratio	= 3.
				output_width	= 640.
			elif size == 'widget':
				aspect_ratio	= 1.
				output_width	= 150.
			else:
				raise Exception('invalid size parameter')
				
				##set this to some default for production
			#calculate output_height from output_width
			output_height	= output_width/aspect_ratio
			
			##get crop dimensions
			if img_width > img_height*aspect_ratio:
				#width must be cropped
				w_crop_unscaled = (img_width-img_height*aspect_ratio)/2
				w_crop 	= float(w_crop_unscaled/img_width)
				left_x 	= w_crop
				right_x = 1.-w_crop
				top_y	= 0.
				bot_y	= 1.
			else:
				#height must be cropped
				h_crop_unscaled = (img_height-img_width/aspect_ratio)/2
				h_crop	= float(h_crop_unscaled/img_height)
				left_x	= 0.
				right_x	= 1.
				top_y	= h_crop
				bot_y	= 1.-h_crop
		
			#crop image to aspect ratio
			img.crop(left_x,top_y,right_x,bot_y)
			logging.debug(img)
			
			#resize cropped image
			img.resize(width=int(output_width),height=int(output_height))
			logging.debug(img)
			output_img = img.execute_transforms(output_encoding=images.JPEG)
#			logging.debug(output_img)
		except:
			levr.log_error(self.request.body)
			output_img = None
		finally:
			try:
				self.response.headers['Content-Type'] = 'image/jpeg'
				self.response.out.write(output_img)
			except:
				levr.log_error()

		
app = webapp2.WSGIApplication([('/phone', phone),
								('/phone/log', phone_log),
								('/phone/uploadDeal', uploadDeal),
								('/phone/img.*', img)
								],debug=True)
