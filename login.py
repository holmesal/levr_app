import os
import webapp2
import jinja2
import logging
import levr_classes as levr
import levr_encrypt as enc

from gaesessions import get_current_session

#launch the jinja environment
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class login(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('templates/login.html')
		self.response.out.write(template.render())
		
	def post(self):
		email = self.request.get('email')
		logging.debug(self.request.get('password'))
		pw = enc.encrypt_password(self.request.get('password'))
		logging.debug(email)
		logging.debug(pw)
		
		session = get_current_session()
		
		#query database for matching email and pw
		q = levr.Business.gql("WHERE email = :email and pw = :pw",email=email,pw=pw)
		business = q.get()
		logging.debug(business)
		if business != None:
			#if matched, pull properties and set loginstate to true
			session['businessID'] = enc.encrypt_key(business.key())
			session['alias'] = business.alias
			session['loggedIn'] = True
			self.redirect('/merchants/manage')
		else:
			#show login page again
			template = jinja_environment.get_template('templates/login.html')
			self.response.out.write(template.render())

app = webapp2.WSGIApplication([('/login', login)],debug=True)
