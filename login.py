import os
import webapp2
import jinja2

#launch the jinja environment
jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class login(webapp2.RequestHandler):
	def get(self):
		#show login page
		template = jinja_environment.get_template('templates/login.html')
		self.response.out.write(template.render())
		
	def post(self):
		email = self.request.get('email')
		pw = self.request.get('password')
		
		if pw == 'secret':
			
			template = jinja_environment.get_template('templates/merchantsLanding.html')
			self.response.out.write(template.render())
		else:
			#show login page again
			template = jinja_environment.get_template('templates/login.html')
			self.response.out.write(template.render())

app = webapp2.WSGIApplication([('/login', login)],debug=True)