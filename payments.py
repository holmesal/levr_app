import os, sys
import webapp2
import levr_classes as levr
import levr_utils
from google.appengine.ext import db
import logging
import jinja2

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

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
	def post(self):
		'''
		Currently a mockup for the payment functionality
		Will accurately increment/decrement amounts available and such
		just hook in actual payment service and go get a beer
		'''
		
		#grab payment requests, sort by dollar amount
		
		
		#check for a bunch of stuff - repeated payment requests, multiple requests from the same user, large dollar amounts, redemptions that happen too quickly, etc
		
		#attempt payment
		
		#on success, decrement customer.money_available
		
		

app = webapp2.WSGIApplication([('/payments/view', view), ('/payments/post', post)],debug=True)