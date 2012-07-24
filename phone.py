import webapp2
import json
import math
from datetime import datetime
from datetime import timedelta
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
				primaryCat = decoded["in"]["primaryCat"]
				start = decoded["in"]["start"]
				numResults = decoded["in"]["size"]
				
				#query the database for all deals with a matching primaryCat
				q = levr.Category.gql("WHERE primary_cat=:1",primaryCat).fetch(int(numResults),offset=int(start))
	#			logging.info(q.count())
				#define an empty "dealResults" LIST, and initialize the counter to 0
				dealResults = []
				resultsPushed = 0
				#initialize isEmpty to 1
				isEmpty = True
				#iterate over the results
				#Want to grab deal information for each category
				for category in q:
					#set isEmpty to 1
					logging.debug(category)
					logging.debug(dir(category))
					#break if results limit is hit
					if resultsPushed == numResults:
						break
					#grab the parent deal key so we can grab the info from it
					d = category.key().parent()
					#logging.debug("Key: %s",str(d))
					#grab the appropriate deal parent
					result = levr.Deal.get(d)
					#logging.debug(result)
					if result.deal_status == 'active':
						isEmpty = False
						#trade an object for a phone-formatted dictionary
						deal = levr.phoneFormat(result,'list',primaryCat)
						#push the primary onto the dictionary
						deal['primaryCat'] = category.primary_cat
						#push the whole dictionary onto a list
						dealResults.append(deal)
						#increment the counter
						resultsPushed += 1
					else:
						pass
				#if isempty is true, send back suggested searches instead
				if isEmpty == False:
					dealResults.append(None)
		
				#go get (all) suggested searches
				q = levr.EmptySetResponse.all()
				#sory by index
				q.order('index')
				#loop through and append to data
				for result in q:
					searchObj = {"primaryCat":result.primary_cat,
									"imgURL":'http://getlevr.appspot.com/phone/emptySetImg?img_key=' + enc.encrypt_key(result.key().__str__())}
					#push to stack
					dealResults.append(searchObj)
				#echo back success!
				toEcho = {"success":True,"data":dealResults,"isEmpty":isEmpty}
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
				toEcho = {"success":True,"data":data}
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
				
				toEcho = {"success":True,}
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
				toEcho = {"success":True}
					
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
				toEcho = {"success":True,"data":deal}

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
				ninja.flush_new_redeem_count()
				ninja.put()
				#get new notifications
				notifications = ninja.get_notifications()
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
					#raise Exception('')
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
				if cor.amount == 0:
					toEcho = {"success":False}
				else:
					cor.status = 'pending'
					cor.date_created = datetime.now()
					cor.put()
					toEcho = {"success":True}
			
			elif action == "fetchUploadURL":
				upload_url = blobstore.create_upload_url('/phone/uploadDeal')
				logging.debug(upload_url)
				toEcho = {"success":True, "data":{"url":upload_url}}
				
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
		toEcho = {"success":False}
		try:
			logging.debug(self.request.headers)
			logging.debug('Body is next!')
		
			#create alias for self.request.get
			inputs			= self.request.get
			#grab existing business
			business_name	= inputs('businessName')
			geo_point		= inputs('geoPoint')
			logging.debug(geo_point)
			geo_point		= levr.geo_converter(geo_point)
			logging.debug(geo_point)
			business = levr.Business.gql("WHERE business_name=:1 and geo_point=:2", business_name, geo_point).get()
			#if a business doesn't exist in db, then create a new one
			if not business:
				business = levr.Business(email='email@getlevr.com')
		
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
		
		
			uid 				= enc.decrypt_key(inputs('uid'))
			logging.debug(uid)
			#create new deal object as child of the uploader Customer
			deal				= levr.CustomerDeal(parent=db.Key(uid))
			#fetch blobstore_info object of the uploaded image
			logging.debug(self.get_uploads())
			upload				= self.get_uploads()[0]
			logging.debug(upload)
			blob_key			= upload.key()
			#rest of the stuff stuff
			deal.img			= blob_key
			deal.businessID		= business.key().__str__()
			deal.business_name	= business_name
			deal.deal_text		= inputs('dealText') #### check name!!!
			deal.deal_status	= 'pending'
			deal.geo_point		= geo_point
#			deal.deal_text		= inputs('dealText')
			deal.description	= inputs('description')
			#set expiration date to one week from now
			#only need date, not time for this
			deal.date_end		= datetime.now() + timedelta(days=7)
	#		date_uploaded		= automatic
		
			#put in DB
			deal.put()
		
			#return deal id and shareURL
			dealID = enc.encrypt_key(deal.key())
			toEcho = {"success":True,"dealID":dealID,"shareURL":'http://getlevr.com/share/deal?id='+dealID}
		
		
			#send mail to the admins to notify of new pending deal
#			mail.send_mail(sender="Pending Deal <feedback@getlevr.com>",
#							to="Patrick Walsh <patrick@getlevr.com>",
#							subject="New pending deal",
#							body="""
#							Another dealdebeast has been caught by one of your
#							faithful ninjas! Heed your call to arms and approve the 
#							dealdebeast before it gets away!
#							""").send()
		except:
			levr.log_error(self.request.body)
		finally:
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
			deal = levr.Deal.get(dealID)

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
				aspect_ratio	= float(img_width)/float(img_height)
				output_width	= float(img_width)
	#			self.response.out.write(deal.img)
			elif size == 'webShare':
				aspect_ratio	= 4.
				output_width	= 600.
			elif size == 'facebook':
				aspect_ratio 	= 1.
				output_width	= 250.
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
			logging.debug(output_img)
		except:
			levr.log_error(self.request.body)
			output_img = None
		finally:
			try:
				self.response.headers['Content-Type'] = 'image/jpeg'
				self.response.out.write(output_img)
			except:
				levr.log_error()
			
class EmptySetImg(webapp2.RequestHandler):
	def get(self):
		#grab input data
		img_key = enc.decrypt_key(self.request.get("img_key"))
		
		#grab image from datastore
		result = levr.EmptySetResponse.get(img_key)
		
		self.response.headers['Content-Type'] = 'image/png'
		self.response.out.write(result.img)
		
app = webapp2.WSGIApplication([('/phone', phone),
								('/phone/log', phone_log),
								('/phone/uploadDeal', uploadDeal),
								('/phone/img.*', img),
								('/phone/emptySetImg.*', EmptySetImg)],
								debug=True)
