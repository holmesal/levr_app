import os, sys
import webapp2
import json
import levr_classes as levr
from datetime import datetime
import levr_utils
from google.appengine.ext import db
import logging
import jinja2
import urllib,urllib2

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

def throwFlags(cor,ninja):
	#check for a bunch of stuff - repeated payment requests, multiple requests from the same user, large dollar amounts, redemptions that happen too quickly, etc
	pass

class PaypalAdaptivePayment:
	"""
	Paypal Object to initialize and conducting the payments
	"""
	def __init__(self,paypal_sandbox_enabled):
		'''Constructor for the Paypal Api Sets the headers and api credentials which are required for the initialization of the payments'''
		assert paypal_sandbox_enabled, "missing arguments..."
		self.request_data_format = 'JSON'
		self.response_data_format = 'JSON'
		self.paypal_sandbox_enabled = paypal_sandbox_enabled
		if paypal_sandbox_enabled:
			self.paypal_secure_user_id = "alonso_1342706801_biz_api1.getlevr.com"
			self.paypal_secure_password = "1342706820"
			self.paypal_api_signature = "Ahg-X6mZSS2MSKURJRVuRWFSIDuxAANmXWOAcd2gn4N1rF0KQmzwCfUt"
			self.sender_email = "alonso_1342706801_biz@getlevr.com"
			self.request_url =	"https://svcs.sandbox.paypal.com/AdaptivePayments/Pay"
		else:
			self.paypal_secure_user_id = "your live paypal secure user id"
			self.paypal_secure_password = "your live secure password"
			self.paypal_api_signature = "Your live ApI signature"
			self.receiver_email = "Your Live Receiver Email"
			self.request_url =	"https://paypal.com/AdaptivePayments/Pay"
	
	def initialize_payment(self,amount,receiver_email,cancel_url,return_url):
		try:
			header_data = {}
			header_data["X-PAYPAL-SECURITY-USERID"] = self.paypal_secure_user_id
			header_data["X-PAYPAL-SECURITY-PASSWORD"] = self.paypal_secure_password
			header_data["X-PAYPAL-SECURITY-SIGNATURE"] = self.paypal_api_signature
			header_data["X-PAYPAL-REQUEST-DATA-FORMAT"] = self.request_data_format
			header_data["X-PAYPAL-RESPONSE-DATA-FORMAT"] = self.response_data_format
			if self.paypal_sandbox_enabled:
				header_data["X-PAYPAL-APPLICATION-ID"] = "APP-80W284485P519543T"
			else:
				header_data["X-PAYPAL-APPLICATION-ID"] = "Your Live Paypal Application ID"
			params = {'actionType':'PAY', 'receiverList':{'receiver':[{'email':receiver_email,'amount':amount}]}, 'cancelUrl':cancel_url,'requestEnvelope':'', 'errorLanguage':'en_US', 'currencyCode':'USD', 'returnUrl':return_url,'senderEmail':self.sender_email}
			paypal_request_data = json.dumps(params)
			req = urllib2.Request(self.request_url,paypal_request_data,header_data)
			response = urllib2.urlopen(req)
			return json.loads(response.read())
		except:
			levr.log_error("Unable to initialize the payment flow")
#			log.exception("Unable to initialize the payment flow...")
	
	
class view(webapp2.RequestHandler):
	def get(self):
		cor = levr.CashOutRequest.gql('WHERE status=:1 ORDER BY amount DESC','pending').get()
		if cor:
			ninja = levr.Customer.get(cor.key().parent())
		
		
			#count the number of deals from this person
			q = levr.CustomerDeal.gql('WHERE ANCESTOR IS :1',ninja.key())
			numDeals = q.count()
			
			cor.money_available_paytime = ninja.money_available
			cor.put()
			
			template_values = {
				"corID"						: cor.key().__str__(),
				"amount"					: cor.amount,
				"money_available_paytime"	: cor.money_available_paytime,
				"life_paid"					: ninja.money_paid,
				"numDeals"					: numDeals
			}
			
			template = jinja_environment.get_template('templates/payments.html')
			self.response.out.write(template.render(template_values))
		
		else:
			self.response.out.write('No cash-out-requests')

class post(webapp2.RequestHandler):
	def post(self):
		try:
			#to deploy: change paypaladaptivepayment argument to False (takes out of sandbox)
			#remove email override
	
			#get corID
			corID = self.request.get('corID')
			#get cor
			cor = levr.CashOutRequest.get(corID)
			#get the larger amount if money available at paytime is different
			if cor.amount != cor.money_available_paytime:
				amount = cor.money_available_paytime
				cor.note = 'The money available at paytime was greater than when the COR was created, so the paytime balance was used.'
			else:
				amount = cor.amount
			#get ninja
			ninja = levr.Customer.get(cor.key().parent())
			#get payment email
			receiver_email = ninja.payment_email
			receiver_email = "alonso_1342706914_per@getlevr.com"
			#Change to false and enter information in above class to deploy
			paypal_init = PaypalAdaptivePayment(True)
			response = paypal_init.initialize_payment(amount,receiver_email,"http://cancel_url.com","http://return_url.com")
			logging.info(response)
		
			if response['paymentExecStatus'] == 'COMPLETED':
				#set cor to "paid"
				cor.status = "paid"
				cor.date_paid = datetime.now()
				cor.payKey = response['payKey']
			
				cor.put()
			
				#for each deal, make paid_out == earned_total
				q = levr.CustomerDeal.gql('WHERE ANCESTOR IS :1',ninja.key())
				for deal in q:
					deal.paid_out = deal.earned_total
					deal.put()
			
				#are number consistent?
				if cor.amount != cor.money_available_paytime:
					logging.error('PAY MISMATCH AT UID:' + ninja.key().__str__())
					#send email here later
			
				#set ninja money_available back to 0
				ninja.money_available = 0.0
			
				#increment money_paid for the customer
				ninja.money_paid += amount
			
				#update ninja
				ninja.put()
				logging.info('Payment completed!')

			self.response.out.write(self.request.get(corID) + '<p>Payment status: <strong>' + response['paymentExecStatus'] + '</strong></p><p><a href="/payments/view">Next Request</a></p>')
		except:
			levr.log_error()

class reject(webapp2.RequestHandler):
	def post(self):
		#get corID
		corID = self.request.get('corID')
		#grab cor
		cor = levr.CashOutRequest.get(corID)
		#add note
		cor.note = self.request.get('note')
		#change status to rejected
		cor.status = 'rejected'
		#update cor
		cor.put()

app = webapp2.WSGIApplication([('/payments/view', view),
								('/payments/post', post),
								('/payments/reject',reject)],
								debug=True)
