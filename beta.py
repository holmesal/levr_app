import os
import webapp2
import levr_classes as levr
#import levr_encrypt as enc
#import levr_utils
#from google.appengine.ext import db
import logging
import jinja2

#from gaesessions import get_current_session

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MerchantBetaHandler(webapp2.RequestHandler):
	def get(self):
		try:
				template = jinja_environment.get_template('templates/merchantBeta.html')
				self.response.out.write(template.render())
		except:
			levr.log_error()
	
	def post(self):
		logging.info(self.request.body)
		#store somewhere
		confirm = '''<!DOCTYPE html>
<html>
	<head>
		<link href="../css/merchantBeta.css" rel="stylesheet">
		<title>Welcome to Levr.</title>
		<link rel="icon" type="image/png" href="img/favicon.png">
	</head>
	<body>
		<p id="headerText">Welcome to Levr.</p>
		<p id="subtitle">Great! We'll confirm your information and email you instructions on how to get started.</p>
	</body>
</html>'''
		self.response.out.write(confirm)
		
		#send an email to notify of a business signup
		
	

app = webapp2.WSGIApplication([('/beta/merchant', MerchantBetaHandler)],
								debug=True)
