import os
import webapp2
import jinja2

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
		
		if pw == 'secret':
			session['loggedIn'] = True
			template = jinja_environment.get_template('templates/merchantsLanding.html')
			self.response.out.write(template.render())
		else:
			#show login page again
			template = jinja_environment.get_template('templates/login.html')
			self.response.out.write(template.render())

app = webapp2.WSGIApplication([('/login', login)],debug=True)