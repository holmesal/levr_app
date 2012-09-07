import os
import webapp2
import jinja2
import logging
from google.appengine.api import mail

class landing(webapp2.RequestHandler):
	def get(self):
		#launch the jinja environment
		jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
		
		#check user-agent to see if user is mobile or not
		#get the user-agent
		uastring = str(self.request.headers['user-agent'])
		
		if 'Mobile' in uastring:
			logging.info('THIS IS A MOBILE DEVICE')
			#serve mobile landing page
			template = jinja_environment.get_template('templates/landing_v2_mobile.html')
		else:
			logging.info('THIS IS A DESKTOP DEVICE')
			#serve desktop landing page
			template = jinja_environment.get_template('templates/landing_v2.html')
		
		self.response.out.write(template.render())
		
	def post(self):
			logging.info(self.request.get('email'))
			#message to user
			message = mail.EmailMessage(
				sender	="Levr <beta@levr.com>",
				subject	="Your Levr Beta Request",
				to		=self.request.get('email'))
			logging.debug(message)
			html = '''<html><body style="background-color: #f3f3f3; margin:0; font-family: helvetica, arial,sans-serif;">
	<div style="background-color: white; width: 80%; margin-left: auto; margin-right: auto; height:auto; margin-top: 15px; margin-bottom: 15px;">
		<div style="padding:20px;">
			<p style="font-size: 20pt; font-weight: 300; text-align:center;">Welcome to Levr Beta.</p>
			<p style="font-size: 15pt; font-weight: 300; margin-top: 50px;">On behalf of the Levr team, it's great to have you aboard.</p>
			<p style="font-size: 15pt; font-weight: 300;">We're sending out invitations on a first-come, first-serve basis. We've reserved you a spot in line, and we'll let you know as soon as you can download Levr.</p>
			<p style="font-size: 15pt; font-weight: 300;">In the meantime, feel free to keep up with us via our <a href="http://blog.levr.com">blog</a>, or shout at us on <a href="http://twitter.com/getlevr">twitter</a>.</p>
			<p style="font-size: 15pt; font-weight: 300; margin-top: 50px;">See you soon!</p>
			<p style="font-size: 15pt; font-weight: 300;">-Levr</p>
		</div>
	</div>
</body></html>'''
			message.html = html
			body = '''
			Welcome to Levr Beta.
			
			On behalf of the Levr team, it's great to have you aboard.
			
			We're sending out invitations on a first-come, first-serve basis. We've reserved you a spot in line, and we'll let you know as soon as you can download Levr.
			
			In the meantime, feel free to keep up with us via our blog (http://blog.levr.com), or shout at us on twitter (http://twitter.com/getlevr).
			
			See you soon!
			-Levr'''
			message.body = body
			message.send()
			
			#message to alonso
			message = mail.EmailMessage(
				sender	="Levr <beta@levr.com>",
				subject	="New beta user",
				#to		=self.request.get('email'))
				to		='<beta@levr.com>')
			logging.debug(message)
			body = 'New beta request from email: ' + self.request.get('email')
			message.body = body
			message.send()
			#self.response.out.write(message.body)
	

app = webapp2.WSGIApplication([('/', landing)],debug=True)