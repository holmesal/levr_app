import os
import webapp2
import jinja2

class landing(webapp2.RequestHandler):
	def get(self):
		#launch the jinja environment
		jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
		
		#serve up the landing page html
		template = jinja_environment.get_template('templates/landing.html')
		self.response.out.write(template.render())

app = webapp2.WSGIApplication([('/', landing)],debug=True)