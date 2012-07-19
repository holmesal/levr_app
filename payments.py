import os, sys
import webapp2
import levr_classes as levr
import levr_utils
from google.appengine.ext import db
import logging
import jinja2
import urllib2
from google.appengine.api import urlfetch

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def throwFlags(cor,ninja):
	#check for a bunch of stuff - repeated payment requests, multiple requests from the same user, large dollar amounts, redemptions that happen too quickly, etc
	pass

class view(webapp2.RequestHandler):
	def get(self):
		cor = levr.CashOutRequest.gql('WHERE status=:1 ORDER BY amount DESC','pending').get()
		ninja = levr.Customer.get(cor.key().parent())
		
		#count the number of deals from this person
		q = levr.CustomerDeal.gql('WHERE ANCESTOR IS :1',ninja.key())
		numDeals = q.count()
		
		
		template_values = {
			"amount"					: cor.amount,
			"life_paid"					: ninja.money_paid,
			"numDeals"					: numDeals
		}
		
		template = jinja_environment.get_template('templates/payments.html')
		self.response.out.write(template.render(template_values))

class post(webapp2.RequestHandler):
	def get(self):
		'''
		Currently a mockup for the payment functionality
		Will accurately increment/decrement amounts available and such
		just hook in actual payment service and go get a beer
		'''
		
		
		#headers
		headers = {
			"X-PAYPAL-USERID"				: "alonso_1342706801_biz_api1.getlevr.com",
			"X-PAYPAL-SECURITY-PASSWORD"	: "1342706820",
			"X-PAYPAL-SECURITY-SIGNATURE"	: "Ahg-X6mZSS2MSKURJRVuRWFSIDuxAANmXWOAcd2gn4N1rF0KQmzwCfUt",
			"X-PAYPAL-REQUEST-DATA-FORMAT"	: "JSON",
			"X-PAYPAL-RESPONSE-DATA-FORMAT"	: "JSON",
			"X-PAYPAL-APPLICATION-ID"		: "APP-80W284485P519543T"
		}
		
		#headers = {'X-PAYPAL-USERID: alonso_1342706801_biz_api1.getlevr.com', 'X-PAYPAL-SECURITY-PASSWORD: 1342706820', 'X-PAYPAL-SECURITY-SIGNATURE: Ahg-X6mZSS2MSKURJRVuRWFSIDuxAANmXWOAcd2gn4N1rF0KQmzwCfUt', 'X-PAYPAL-REQUEST-DATA-FORMAT: JSON', 'X-PAYPAL-RESPONSE-DATA-FORMAT: JSON', 'X-PAYPAL-APPLICATION-ID: APP-80W284485P519543T'}
		
		#request body
		request_body = {
			"actionType"						: "PAY",
			"senderEmail"						: "alonso_1342706801_biz_api1@getlevr.com",
			"receiverList.receiver(0).email"	: "alonso_1342706914_per@getlevr.com",
			"receiverList.receiver(0).amount"	: 100.00,
			"currencyCode"						: "USD",
			"cancelUrl"							: "getlevr.com",
			"returnUrl"							: "getlevr.com",
			"requestEnvelope.errorLanguage"		: "en_US"
			
		}
		
		url = "https://svcs.sandbox.paypal.com/AdaptivePayments/Pay"
		
		result = urlfetch.fetch(url=url,payload=request_body,headers=headers)
		
		logging.info(result.content)
		
		#PAYPAL ACCOUNT INFORMATION
		userid 			= None		#pretty sure this is the url from which the request is coming, and the url to which it will be returned
		password		= None
		signature		= None
		ipaddress		= None		#pretty sure this is the current IP address, NOT that of the phone. Makes sense, no?
		request_format	= 'JSON'
		response_format = 'JSON'
		app_id			= None
		
		#PAYPAL REQUEST BODY
		
		
		
		
		#attempt payment
		
		#on success, decrement customer.money_available
		
		

app = webapp2.WSGIApplication([('/payments/view', view), ('/payments/post', post)],debug=True)