import os
import webapp2
import jinja2

class logout(webapp2.RequestHandler):
	def get(self):
		#launch the jinja environment
		jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
		
		#logout the user
		
		#redirect to the landing page for merchants
		template = jinja_environment.get_template('templates/merchantsLanding.html')
		self.response.out.write(template.render())

app = webapp2.WSGIApplication([('/logout', logout)],debug=True)