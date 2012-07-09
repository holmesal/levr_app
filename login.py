import os
import webapp2
import jinja2
import logging
import levr_classes as levr

from gaesessions import get_current_session

#launch the jinja environment
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class login(webapp2.RequestHandler):
	def get(self):
			template = jinja_environment.get_template('templates/login.html')
			self.response.out.write(template.render())
		
	def post(self):
		email = self.request.get('email')
		pw = self.request.get('password')
		
		session = get_current_session()
		
		#query database for matching email and pw
		q = levr.Business.gql("WHERE contact_email = :email and pw = :pw",email=email,pw=pw)
		business = q.get()
		
		if business != None:
			#if matched, pull properties and set loginstate to true
			session['businessKey'] = business.key()
			session['businessID'] = business.businessID
			session['contact_owner'] = business.contact_owner
			session['loggedIn'] = True
			self.redirect('/merchants/manage')
		else:
			#show login page again
			template = jinja_environment.get_template('templates/login.html')
			self.response.out.write(template.render())

app = webapp2.WSGIApplication([('/login', login)],debug=True)
