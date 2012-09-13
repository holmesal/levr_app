import os
import webapp2
import levr_classes as levr
#import levr_encrypt as enc
#import levr_utils
#from google.appengine.ext import db
import logging
import jinja2
from google.appengine.api import mail

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
		message = mail.EmailMessage(
			sender	="Levr <beta@levr.com>",
			subject	="New beta user",
			#to		=self.request.get('email'))
			to		="beta@levr.com")
			
		body = 'New beta request from: ' + self.request.get('business_name') + 'Name: ' + self.request.get('contact_name') + 'Email: ' + self.request.get('contact_email') + 'Phone: ' + self.request.get('contact_phone')
		message.body = body
		message.send()
		
		b = levr.BusinessBetaRequest()
		b.business_name = self.request.get('business_name')
		b.contact_name = self.request.get('contact_name')
		b.contact_email = self.request.get('contact_email')
		b.contact_phone = self.request.get('contact_phone')
		b.put()
		
class SendMailHandler(webapp2.RequestHandler):
	def get(self):
	
		targetArr = ["alonso@levr.com","beta@levr.com","patrick@levr.com"]
		
		for rec in targetArr:
			
			logging.info("target is: " + rec)
			
			message = mail.EmailMessage(
				sender	="Levr <beta@levr.com>",
				subject	="Your Levr Beta Request",
				#to		=self.request.get('email'))
				to		=rec)
			
			#check out http://www.campaignmonitor.com/css/ for styles that are allowed in email
			
			html = '''<html>
	<body style="background-color: #f3f3f3; margin:0; font-family: helvetica, arial,sans-serif;">
	
		
	
		<div style="background-color: white; width: 80%; margin-left: auto; margin-right: auto; height:auto; margin-top: 15px; margin-bottom: 15px; color: #333333;">
			<div id="image" style="width: 100%;height: 200px;overflow:hidden;text-align:center;"><img src='../img/boston_300.jpg'></div>
			<div style="padding:20px;">
				<p style="font-size: 20pt; font-weight: 700;">Cheap, easy advertising that works.</p>
				<p style="font-size: 15pt; font-weight: 300; margin-top: 50px;">Levr is a location-based advertising network for your business.</p>
				<p style="font-size: 15pt; font-weight: 300;">Use offers you already run in-store, or create new ones online in seconds.</p>
				<p style="font-size: 15pt; font-weight: 300;">Reach a broad local audience that is actively trying to buy what you sell.</p>
				<p style="font-size: 16pt; font-weight: 700; margin-top: 40px;">Join during the trial phase, and get Levr for free. For life.</p>
				<a id="trialbutton" href="http://www.levr.com/beta/merchant" class="button green" style="display: inline-block;   outline: none;   cursor: pointer;   text-align: center;   text-decoration: none;   font: 20px/100% Arial, Helvetica, sans-serif;   padding: .5em 2em .55em;   text-shadow: 0 1px 1px rgba(0,0,0,.3);   -webkit-border-radius: .5em;    -moz-border-radius: .5em;   border-radius: .5em;   -webkit-box-shadow: 0 1px 2px rgba(0,0,0,.2);   -moz-box-shadow: 0 1px 2px rgba(0,0,0,.2);   box-shadow: 0 1px 2px rgba(0,0,0,.2);		color: #e8f0de;   border: solid 1px #538312;   background: #64991e;   background: -webkit-gradient(linear, left top, left bottom, from(#7db72f), to(#4e7d0e));   background: -moz-linear-gradient(top,  #7db72f,  #4e7d0e);   filter:  progid:DXImageTransform.Microsoft.gradient(startColorstr='#7db72f', endColorstr='#4e7d0e');">Get Levr for free</a>
				<a id="learnButton" href="http://www.levr.com/merchants" class="button blue" style="display: inline-block;   margin-left: 50px; outline: none;   cursor: pointer;   text-align: center;   text-decoration: none;   font: 20px/100% Arial, Helvetica, sans-serif;   padding: .5em 2em .55em;   text-shadow: 0 1px 1px rgba(0,0,0,.3);   -webkit-border-radius: .5em;    -moz-border-radius: .5em;   border-radius: .5em;   -webkit-box-shadow: 0 1px 2px rgba(0,0,0,.2);   -moz-box-shadow: 0 1px 2px rgba(0,0,0,.2);   box-shadow: 0 1px 2px rgba(0,0,0,.2);		color: #d9eef7;   border: solid 1px #0076a3;   background: #0095cd;   background: -webkit-gradient(linear, left top, left bottom, from(#00adee), to(#0078a5));   background: -moz-linear-gradient(top,  #00adee,  #0078a5);   filter:  progid:DXImageTransform.Microsoft.gradient(startColorstr='#00adee', endColorstr='#0078a5');">Learn more</a>
			</div>
		</div>
	</body>
	</html>'''
			
			message.html = html
			
			body = '''Cheap, easy advertising that works.
			
			Levr is a location-based advertising network for your business.
			
			Use offers you already run in-store, or create new ones online in seconds.
			
			Reach a broad local audience that is actively trying to buy what you sell.
			
			Join during the trial phase, and get Levr for free. For life.
			
			Get Levr for free at http://www.levr.com/beta/merchant'''
			
			message.body = body
			message.send()
		
		self.response.out.write('Email sent to: ' + targetArr.__str__() + ' Now go unset this so there are no duplicate sends!')
	
		self.response.out.write(message.html)
		
		
app = webapp2.WSGIApplication([('/beta/merchant', MerchantBetaHandler),
								('/beta/sendMail', SendMailHandler)],
								debug=True)
