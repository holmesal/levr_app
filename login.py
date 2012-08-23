import os
import webapp2
import jinja2
import logging
import levr_classes as levr
import levr_encrypt as enc
from google.appengine.ext import db
from gaesessions import get_current_session

#launch the jinja environment
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class login(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('templates/login.html')
		self.response.out.write(template.render())
		
	def post(self):
		try:
			email = self.request.get('email')
			logging.debug(email)
			email = db.Email(email)
			logging.debug(self.request.get('password'))
			pw = enc.encrypt_password(self.request.get('password'))
			logging.debug(email)
			logging.debug(pw)
			
			#query database for matching email and pw
	#		q = levr.Business.gql("WHERE email = :email and pw = :pw",email=email,pw=pw)
	#		business = q.get()
			owner = levr.BusinessOwner.all().filter('email =',email).filter('pw =',pw).get()
			logging.debug(owner)
				#search for owner
			if owner != None:
					#owner exists in db, and can login
				business = levr.Business.all().ancestor(owner).get()
				logging.debug(business)
				if business != None:
					
					session = get_current_session()
					#if matched, pull properties and set loginstate to true
					session['businessID'] = enc.encrypt_key(business.key())
					session['alias'] 	= business.business_name
					session['loggedIn'] = True
					session['validated']= owner.validated
					self.redirect('/merchants/manage')
				else:
					levr.log_error()
			else:
				#show login page again
				template = jinja_environment.get_template('templates/login.html')
				self.response.out.write(template.render())
		except:
			levr.log_error()
app = webapp2.WSGIApplication([('/login', login)],debug=True)
