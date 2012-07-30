import webapp2
#import json
import logging
import os
import levr_classes as levr
import levr_encrypt as enc
#import levr_utils
import jinja2
from google.appengine.api import mail

class LostPasswordHandler(webapp2.RequestHandler):
	'''presents form to user to enter in their email. email is sent to user
	to rest the password'''
	def get(self):
		try:
			'''template html page for entering lost password info'''
			#email will be false if an invalid email was passed, otherwise will be true
			try:
				success = self.request.get('success')
			except:
				success = 'True'
		
			template_values = {"success":success}
		
			jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
			template = jinja_environment.get_template('templates/lostPassword.html')
			self.response.out.write(template.render(template_values))
		except:
			levr.log_error()

	def post(self):
		'''input:user email
		output: success, sends email to email account'''
		try:
			user_email = self.request.get('email')
			user = levr.Customer.gql('WHERE email=:1',user_email).get()
			logging.debug(user)
			if not user:
				logging.debug('flag not user')
				#redirect
				self.redirect('/password/lost?success=False')
			else:
				logging.debug('flag is user')
				#send mail to the admins to notify of new pending deal
				url ='http://getlevr.appspot.com/password/reset?id=' + enc.encrypt_key(user.key())
				logging.info(url)
				try:
					mail.send_mail(sender="Lost Password<password@getlevr.com>",
									to="Patrick Walsh <patrick@getlevr.com>",
									subject="New pending deal",
									body="""
									Follow this link to reset your password:
									%s
									""" % url).send()
					sent = True
				except:
					sent = False
					logging.error('mail not sent')
			
				template_values={"sent":sent}
				jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
				template = jinja_environment.get_template('templates/lostPasswordEmailSent.html')
				self.response.out.write(template.render(template_values))
		except:
			levr.log_error()
		
class ResetPasswordHandler(webapp2.RequestHandler):
	'''User enters in a new password twice'''
	def get(self):
		pass
		'''Template has uid in url to identify them'''
		
		uid = self.request.get('id')
		#If a false attempt has been made, success will be false, otherwise true
		try:
			success = self.request.get('success')
		except:
			success = 'True'
		
		
		template_values = {"success":success,"uid":uid}
			
		jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
		template = jinja_environment.get_template('templates/resetPassword.html')
		self.response.out.write(template.render(template_values))

	def post(self):
		'''Resets password on the database'''
		password1 = self.request.get('newPassword1')
		password2 = self.request.get('newPassword2')
		uid = self.request.get('id')
		uid = enc.decrypt_key(uid)
		
		if password1 == password2:
			#passwords match
			logging.debug('flag password success')
			encrypted_password = enc.encrypt_password(password1)
			logging.debug(uid)
			user = levr.Customer.get(uid)
			user.pw = encrypted_password
			user.put()
			
			template_values={'success':'True'}
			jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
			template = jinja_environment.get_template('templates/resetPasswordSuccess.html')
			self.response.out.write(template.render(template_values))
		else:
			#passwords do not match
			self.redirect('/password/reset?id=%s&success=False' % enc.encrypt_key(uid))

app = webapp2.WSGIApplication([('/password/lost', LostPasswordHandler),
								('/password/reset', ResetPasswordHandler)
								],debug=True)
