import os
import webapp2
import levr_classes as levr
#import levr_encrypt as enc
#import levr_utils
#from google.appengine.ext import db
import logging
import jinja2
from google.appengine.api import urlfetch
import json

#CASES:

#1 - User checks in, we don't have that business in our database
	#Response: Hey, there are 10 offers near you (deeplink to dealResults)
	#Response: Hey, you should be the first to upload an offer (only for some types of establishments) (deeplink to deal upload)
#2 - User checks in, we have the business, we don't have any deals there
	#Response: same as above
#3 - User checks in, we have the business, we have one deal there
	#Response: Hey check out this deal! {{DEALTEXT}}(deeplink to dealDetail)
#4 - User checks in, we have the business, we have more than one deal there
	#Response: Hey, check out {{DEALTEXT}}(deeplink to dealDetail) and 5 more deals(deeplink to dealResults)


class AuthorizeHandler(webapp2.RequestHandler):
	def get(self):
		pass


class PushHandler(webapp2.RequestHandler):
	def post(self):
		logging.debug('Foursquare push request received!')
		checkin = self.request.get('checkin')
		secret = self.request.get('secret')
		checkin2 = json.loads(checkin)
		logging.debug(checkin)
		logging.debug(checkin2)
		logging.debug(secret)
		
		#verify that the secret passed matches ours
		secret = 'LB3J4Q5VQWZPOZATSMOAEDOE5UYNL5P44YCR0FCPWFNXLR2K'
		if secret != body.secret:
			#raise an exception
			logging.debug('SECRETS DO NOT MATCH')
		
		'''#go look in our database for a matching foursquare venue id
		business = levr.Business.gql('WHERE foursquare_id IS :1',checkin.venue.id).get()
		
		#initialize the response object
		reply = {
			CHECKIN_ID		: checkin.id,
			text			: '',
			url				: '',
			contentID		: ''
		}
		
		if business:	#business found
			#for deal in levr.Deal().all().filter('businessID =', str(business.key())).run():
			q = levr.Deal.gql("WHERE businessID = :1 AND status = :2 ORDER BY count_redeemed DESC",str(business.key()),'active')
			numdeals = q.count()
			if numdeals > 1:	#many deals found
				topdeal = q.get()
				reply.text = "There are deals here! "+topdeal.deal_text + ". Click to see all "+numdeals+" deals."
				reply.url = '' #deeplink into dealResults screen
			elif numdeals == 1:	#only one deal found
				topdeal = q.get()
				reply.text = "There's a deal here! "+topdeal.deal_text+". Click to redeem."
				reply.url = '' #deeplink into dealDetail screen
			else:	#no deals found
				reply.text = "There aren't any deals here - maybe you'll be the first to add one? Click to upload."
				reply.url = '' #deeplink into deal upload screen
		else:			#no business found
			reply.text = "There aren't any deals here - maybe you'll be the first to add one? Click to upload."
			reply.url = '' #deeplink into deal upload screen
			
		'''
		
		reply = {
			CHECKIN_ID		: checkin.id,
			text			: 'hi there!',
			url				: 'http://www.levr.com',
			contentID		: ''
		}
			
		url = 'https://api.foursquare.com/v2/checkins/CHECKIN_ID/reply'
		result = urlfetch.fetch(url=url,
								payload=reply,
								method=urlfetch.POST)
		logging.debug(response)
		
		
app = webapp2.WSGIApplication([('/foursquare/push', PushHandler),
								('/foursquare/authorize', AuthorizeHandler)],
								debug=True)
