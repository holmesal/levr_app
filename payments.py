import os, sys
import webapp2
import levr_classes as levr
import levr_utils
from google.appengine.ext import db
import logging
import jinja2

class cashOut(webapp2.RequestHandler):
	def post(self):
		'''
		Currently a mockup for the payment functionality
		Will accurately increment/decrement amounts available and such
		just hook in actual payment service and go get a beer
		'''
		
		

app = webapp2.WSGIApplication([('/payments/cashOut', cashOut)],debug=True)