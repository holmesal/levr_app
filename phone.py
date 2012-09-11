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
from google.appengine.api import mail
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
				logging.info('signup')
				#grab email/password from request body
				email = decoded["in"]["email"]
				alias = decoded["in"]["alias"]
				pw = decoded["in"]["pw"]
				toEcho = levr_utils.signupCustomer(email,alias,pw)
		
			#***************login*************************************************
			elif action == "login":
				logging.info('login')
			#grab email/password from request body
				email_or_owner = decoded["in"]["email_or_owner"]
				pw = decoded["in"]["pw"]
				
				toEcho = levr_utils.loginCustomer(email_or_owner,pw)
			
			#***************dealResults************************************************
			elif action == "popularItems":
				logging.info('popularItems')
				data = {
					'popularItems' : ['all','pizza','BU','commonwealth']
					}
				toEcho = {'success': True,'data':data}
			
			elif action == "dealResults":
				logging.info('dealResults')
				logging.info(decoded['in'])
				#grab primaryCat from the request body
				primaryCat 	= decoded["in"]["primaryCat"]
					#search term
#				start 		= decoded["in"]["start"]
					#starting index of search results
					#!!!not used
				numResults 	= decoded["in"]["size"]
				logging.debug(numResults)
					#length of search results list
					#should be None if we want all results
				
				
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
						logging.debug('tag: '+str(tag))
						q.filter('tags =',tag)
				#finally, sort the query
				
				#batch get results. here is where we would set the number of results we want and the offset
				results = q.fetch(None)
				
				
				#define an empty "dealResults" LIST, and initialize the counter to 0
				dealResults = []
				resultsPushed = 0
				#initialize isEmpty to 1
				isEmpty = True
				#iterate over the results
				#Want to grab deal information for each category
				for result in results:
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

#				#if isempty is true, send back suggested searches instead
#				if isEmpty == False:
#					dealResults.append({"isSentinel":True})
#		
#				#go get (all) suggested searches
#				q = levr.EmptySetResponse.all()
#				#sory by index
#				q.order('index')
#				#loop through and append to data
#				for result in q:
#					searchObj = {"isSentinel":False,
#								"primaryCat":result.primary_cat,
#								"imgURL": levr_utils.URL+"/phone/img?size=emptySet&dealID=" + enc.encrypt_key(result.key())
#					} 
#					#push to stack
#					dealResults.append(searchObj)
				#get notifications
#				ninja = levr.Customer.get(uid)
#				notifications = ninja.get_notifications()

				#add boundary
				lon = [-71.13128751569184, -71.13747576487495, -71.13221920314751, -71.1315606660475, -71.1309193072284, -71.1297731686955, -71.12886527141396, -71.12773981063141, -71.12726203628873, -71.1216289071829, -71.12121164180434, -71.10497418088163, -71.1040140000405, -71.10267756839711, -71.0946922485677, -71.09243243954906, -71.09227823963506, -71.0950832349529, -71.097815779737, -71.11251814985596, -71.11356954283684, -71.11706884229781, -71.11779512636194, -71.11965434764042, -71.12212678446998, -71.12626327632834, -71.13026582412857]
				lat = [42.35604793867138, 42.3536306062291, 42.35301975662632, 42.35130590336475, 42.35025979303107, 42.34889896173047, 42.3474035881804, 42.34587017442897, 42.3454410032402, 42.34240376898205, 42.34200386027403, 42.34665152547006, 42.34437686280481, 42.34335156373593, 42.34544719585433, 42.34689842049458, 42.35112647889721, 42.35062769794382, 42.35071497934108, 42.35189268933054, 42.35225746246078, 42.35405913476999, 42.35424633071435, 42.35461863217454, 42.35493709975472, 42.35550741935002, 42.35597048179658]
				
				boundary = {"lat":lat,
							"lon":lon}
				
				if primaryCat == 'all':
					#echo back data - include boundary
					toEcho = {"success":True,"data":dealResults,"isEmpty":isEmpty,"boundary":boundary}#,"notifications":notifications}
				else:
					toEcho = {"success":True,"data":dealResults,"isEmpty":isEmpty}#,"notifications":notifications}
			#***************getUserFavs************************************************
			elif action == "getUserFavs":
				'''
				Grabs all of the favorites of a user - only data to show on list
				input : uid
				output: name, description, dealValue, dealType, imgPath, businessName, primaryCat
				'''
				logging.info('getUserFavs')
				#grab inputs
				uid	= enc.decrypt_key(decoded["in"]["uid"])
				
				#grab user entity
				user	= levr.Customer.get(uid)
				
				#grab list of favorties - list of deal keys
				favorites	= user.favorites
				
				#batch grab favorited deals
				deals	= levr.Deal.get(favorites)
				
				#format deals for output to phone
				formatted_deals	= [levr.phoneFormat(deal,'list') for deal in deals]
				
				#assign formatted deals to data list that doesnt follow standards
				data = formatted_deals
				
				#get notifications
				notifications = user.get_notifications()
				
				#output
				toEcho = {"success":True,"data":data,'notifications':notifications}
			#ADD FAVORITE***********************************************************
			elif action == "addFav":
				'''
				User pressed add favorite button = add favorite mapping
				input: dealID,uid,primaryCat
				output: success = bool
				'''
				logging.info('addFav')
				#get inputs
				uid 		= enc.decrypt_key(decoded["in"]["uid"])
				dealID 		= enc.decrypt_key(decoded["in"]["dealID"])
				
				#get user entity
				user		= levr.Customer.get(uid)
				
				#append dealID to favorites property
				user.favorites.append(db.Key(dealID))
				logging.debug(user.favorites)
#				
				#get notifications
				notifications = user.get_notifications()
				
				#close entity
				user.put()
				
				#output
				toEcho = {"success":True,"notifications":notifications}
			#DELETE FAVORITE********************************************************
			elif action == "delFav":
				'''
				User presses delete favorite button - delete favorite mapping
				input: dealID,uid,primaryCat
				output: success = bool
				'''
				logging.info('delFav')
				#get inputs
				uid 	= enc.decrypt_key(decoded["in"]["uid"])
				dealID 	= enc.decrypt_key(decoded["in"]["dealID"])
				deal_to_delete	= db.Key(dealID)
				logging.debug(deal_to_delete)
				
				#get user entity
				user	= levr.Customer.get(uid)
				logging.debug(levr_utils.log_model_props(user))
				
				#grab favorites list
				favorites	= user.favorites
				logging.debug(favorites)
				
				#generate new favorites list without requested dealID
				new_favorites	= [deal for deal in favorites if deal != deal_to_delete]
				logging.debug(new_favorites)
				
				#reassign user favorites to new list
				user.favorites	= new_favorites
				logging.debug(user.favorites)
				
				#get notifications
				notifications = user.get_notifications()
				
				#close entity
				user.put()
				
				toEcho = {"success":True,"notificaions":notifications}
			#***************getOneDeal************************************************
			elif action == "getOneDeal":
				'''
				Information to show on the deal information screen.
				input	: primaryCat,dealID
				output	: json object of all information necessary to describe deal
				'''
				logging.info('getOneDeal')
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
				logging.info('getMyDeals')
				uid	= enc.decrypt_key(decoded["in"]["uid"])
				logging.debug("encrypted uid: "+str(decoded["in"]["uid"]))
				logging.debug("uid: "+str(uid))
				#grab all deal children of the user
				deals = levr.CustomerDeal.gql("WHERE ANCESTOR IS :1 ORDER BY date_uploaded DESC",uid).fetch(None)
				logging.debug(deals)
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
				logging.info('getMyStats')
				uid = enc.decrypt_key(decoded['in']['uid'])
				#get user information
				user = db.get(uid)
				#format user information
				data = user.get_stats()
				
				#get new notifications
				notifications = user.get_notifications()
				toEcho = {"success":True,"data":data,"notifications":notifications}
				
			elif action == "checkRedeem":
				logging.info('checkRedeem')
				#grab corresponding deal
				uid 	= enc.decrypt_key(decoded['in']['uid'])
				dealID 	= enc.decrypt_key(decoded['in']['dealID'])
				
				#grab the customer
				customer = levr.Customer.get(uid)
				
				#new notifications?
				notifications = customer.get_notifications()
				#don't try and redeem the same deal twice. . .
				if str(dealID) in customer.redemptions:
					toEcho = {"success":False,"data":{"message":"You have already redeemed this deal."},"notifications":notifications}
				else:
					toEcho = {"success":True,"notifications":notifications}
				
				#!!!!!!!!REMOVE THIS WHEN CHECKING IS PUT BACK IN	
#				toEcho = {"success":True,"notifications":notifications}
				
			elif action == "getRedeemScreen":
				logging.info('getRedeemScreen')
				#grab inputs
				dealID 	= enc.decrypt_key(decoded['in']['dealID'])
				
				#grab the deal
				deal = levr.Deal.get(dealID)
				
				#format the deal
				data = levr.phoneFormat(deal,'dealsScreen')
				
				#echo
				toEcho = {"success":True,"data":data}
			
			elif action == "redeem":
				logging.info('redeem')
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
				logging.info('cashOut')
				uid = enc.decrypt_key(decoded['in']['uid'])
#				uid = 'ahNkZXZ-bGV2ci1wcm9kdWN0aW9ucg8LEghDdXN0b21lchiYAQw'
				#grab the ninja
				ninja = levr.Customer.get(uid)
				#delete any current cashOutRequests
				q = levr.CashOutRequest.gql('WHERE ANCESTOR IS :1 AND status=:2',ninja.key(),'pending').fetch(None)
				for result in q:
					result.delete()
				#create a new cashOut request
				cor = levr.CashOutRequest(parent=ninja)
				cor.amount = ninja.money_available
				cor.money_available_paytime = cor.amount
				#get notifications
				notifications = ninja.get_notifications()
				if cor.amount == 0:
					toEcho = {"success":False,"data":{"message":"You need to earn something before you can cash out!","notifications":notifications}}
				else:
					cor.status = 'pending'
					cor.date_created = datetime.now()
					cor.put()
					toEcho = {"success":True,"notifications":notifications}
				
				
				
				
				
				
					## ====== SPOOF ACCEPTANCE FOR BETA TEST ====== ##
				
				
				
				
				
					logging.debug(levr_utils.log_model_props(ninja))
					logging.debug(levr_utils.log_model_props(cor))
					
					#get corID
					#get cor
					#get the larger amount if money available at paytime is different
					if cor.amount != cor.money_available_paytime:
						amount = cor.money_available_paytime
						cor.note = 'The money available at paytime was greater than when the COR was created, so the paytime balance was used.'
					else:
						amount = cor.amount
					#get payment email
					receiver_email = ninja.email
				
					#set cor to "paid"
					cor.status = "paid"
					cor.date_paid = datetime.now()
					cor.payKey = 'this is a pay key'
				
					cor.put()
				
					#for each deal, make paid_out == earned_total
					q = levr.CustomerDeal.gql('WHERE ANCESTOR IS :1',ninja.key())
					for deal in q:
						deal.paid_out = deal.earned_total
						deal.put()
				
					#are number consistent?
					logging.debug(cor.amount)
					logging.debug(cor.money_available_paytime)
					if cor.amount != cor.money_available_paytime:
						#remember to encrypt the key if this is being used for anything
						#other than just error logging
						logging.error('PAY MISMATCH AT UID:' + ninja.key().__str__())
						#send email here later
				
					#set ninja money_available back to 0
					ninja.money_available = 0.0
				
					#increment money_paid for the customer
					ninja.money_paid += amount
					
					#update ninja
					ninja.put()
					logging.info('Payment completed!')
					logging.debug(levr_utils.log_model_props(ninja))
					logging.debug(levr_utils.log_model_props(cor))
					#send email to the ninja confirming their cashout!
					message = mail.EmailMessage(
						sender	="LEVR <beta@levr.com>",
						subject	="Levr Cash Out",
						to		=receiver_email)
					logging.debug(message)
					body = 'Hey Beta Tester,\n\n'
					body += "You submitted a request to be paid for uploading deals to the Levr platform.\n\n"
					body += "If this were real life, this email would be letting you know that you were about to be paid via paypal an amount of $"+str(amount)+". "
					body += "Unfortunately your reality is being simulated. "
					body += "\n\nThanks for helping us test.\nSincerely,\nThe Levr Team"
					message.body = body
					logging.debug(body)
					message.send()
				
			elif action == "getTargetedBusinesses":
				#get businesses that have property targeted = True
				logging.info('getTargetedBusinesses')
				businesses = levr.Business.all().filter('targeted =',True).order('-business_name').fetch(None)
				
				data = {
					'targetedBusinesses':[]
					}
				
				for business in businesses:
					data['targetedBusinesses'].append({
						"businessName"	: business.business_name,
						"geoPoint"		: str(business.geo_point),
						"vicinity"		: business.vicinity,
						"businessID"	: enc.encrypt_key(business.key())
					})
				
				toEcho = {"success":True,"data":data}
			
			elif action == "fetchUploadURL":
				logging.info('fetchUploadURL')
				upload_url = blobstore.create_upload_url('/phone/uploadDeal')
				logging.debug(upload_url)
				toEcho = {"success":True, "data":{"url":upload_url}}

			elif action == "checkBounty":
				logging.info('fetchUploadURL')
				where = "College campuses in Boston, MA"
				what = "Offers on food, drink, clothing, and entertainment"
				toEcho = {"success":True,"data":{"where":where,"what":what}}
			elif action == "reportDeal":
				#user reports a deal
				logging.info('reportDeal')
				uid = enc.decrypt_key(decoded['in']['uid'])
				dealID = enc.decrypt_key(decoded['in']['dealID'])
				
#				uid = 'ahNkZXZ-bGV2ci1wcm9kdWN0aW9ucg8LEghDdXN0b21lchiRAQw'
#				dealID = 'ahNkZXZ-bGV2ci1wcm9kdWN0aW9uchoLEghCdXNpbmVzcxiTAQwLEgREZWFsGJQBDA'
#				dealID = 'ahNkZXZ-bGV2ci1wcm9kdWN0aW9uchoLEghDdXN0b21lchiSAQwLEgREZWFsGJUBDA'
#				dateTime = enc.decrypt_key(decoded['in']['dateTime'])

				#create report Entity
				report = levr.ReportedDeal(
										uid = db.Key(uid),
										dealID = db.Key(dealID)
										).put()
				
				#get human readable info for email
				deal = levr.Deal.get(dealID)
				business_name = deal.business_name
				logging.debug(business_name)
				
				if deal.deal_type == "single":
					deal_text = deal.deal_text
				else:
					deal_text = deal.deal_text +" with purchase of "+deal.secondary_name
				
				user = levr.Customer.get(uid)
				alias = user.alias
				
				deal_class = str(deal.class_name())
				if deal_class == 'CustomerDeal':
					deal_kind = "Ninja Deal"
				elif deal_class == 'Deal':
					deal_kind = "Business Deal"
				else:
					raise ValueError('deal class_name not recognized')
				
				logging.debug(report)
				
				#send notification via email
				message = mail.EmailMessage(
					sender	="LEVR AUTOMATED <patrick@levr.com>",
					subject	="New Reported Deal",
					to		="patrick@levr.com")
				
				logging.debug(message)
				body = 'New Reported Deal\n\n'
				body += 'reporter uid: '  +str(uid)+"\n\n"
				body += 'reporter alias: ' +str(alias)+"\n\n"
				body += 'Business name: '+str(business_name)+"\n\n"
				body += "Deal: "+str(deal_text)+"\n\n"
				body += "Deal Kind: "+deal_kind+"\n\n"
				body += "dealID: "+str(dealID)+"\n\n"
				message.body = body
				logging.debug(message.body)
				message.send()
				
				notifications = user.get_notifications()
				toEcho = {"success":True,"notifications":notifications}
			elif action == 'ninjaHasShared':
				logging.info(action)
				uid = enc.decrypt_key(decoded['in']['uid'])
				dealID = enc.decrypt_key(decoded['in']['dealID'])
				
				
				keys = [dealID,uid]
				#pull deal and user
				entities = db.get(keys)
				deal = entities[0]
				user = entities[1]
				
				logging.debug(levr_utils.log_model_props(deal,['deal_text','business_name','gate_max','has_been_shared']))
				
				deal.share_deal()
				deal.put()
				
				logging.debug(levr_utils.log_model_props(deal,['gate_max','has_been_shared']))

				
				notifications = user.get_notifications()
				toEcho = {"success":True,"notifications":notifications}
			else:
				raise Exception('Unrecognized action')
			############ END OF ACTION FILE PART!!! JSONIFY!!!
		except:
			levr.log_error(self.request.body)
			toEcho = {"success":False}
		finally:
			try:
				logging.debug(levr_utils.log_dict(toEcho))
				logging.debug(json.dumps(toEcho))
				self.response.out.write(json.dumps(toEcho))
			except:
				#catches the case where toEcho cannot be parsed as json
				self.response.out.write(json.dumps({"success":False}))
				levr.log_error('json is not parseable')


class uploadDeal(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		try:
			logging.info('uploadDeal')
			#make sure than an image is uploaded
			logging.debug(self.get_uploads())
			if self.get_uploads(): #will this work?
				upload	= self.get_uploads()[0]
				blob_key= upload.key()
				img_key = blob_key
			else:
				raise Exception('Image was not uploaded')
			
			
			#screen for businessID to determine which mode of upload we are receiving
			if self.request.get('businessID'):
				logging.debug('iphone')
				#we are on iphone
				params = {
					'uid'				: self.request.get('uid'),
					'business'			: self.request.get('businessID'),
					'deal_description'	: self.request.get('deal_description'),
					'deal_line1'		: self.request.get('deal_line1'),
					'img_key'			: img_key
					}
				
				share_url = levr_utils.dealCreate(params,'phone')
			else:
				logging.debug('android')
				#we are on android
				params = {
					'uid'				: self.request.get('uid'),
					'business_name'		: self.request.get('business_name'),
					'geo_point'			: self.request.get('geo_point'),
					'vicinity'			: self.request.get('vicinity'),
					'types'				: self.request.get('types'),
					'deal_description'	: self.request.get('deal_description'),
					'deal_line1'		: self.request.get('deal_line1'),
					'img_key'			: img_key
					}
				(share_url,dealID) = levr_utils.dealCreate(params,'oldphone')
			toEcho = {"success":True,"data":{"shareURL":share_url,"dealID":dealID}}
			self.response.out.write(json.dumps(toEcho))
		except:
			levr.log_error(levr_utils.log_dir(self.request))
			toEcho = {"success":False}#,"data":{"shareURL":share_url}}
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
			logging.info('img')
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
