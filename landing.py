#there's probably a more elegant way to serve up a static landing page that doesn't depend on loading jinja2 and then just redirecting instantly. This'll do for now.

import os
import webapp2
import jinja2

class landing(webapp2.RequestHandler):
	def get(self):
		#launch the jinja environment
		jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
		
		#not sure if this can be empty, spoofing till i can test later
		template_values = {}
		
		#serve up the landing page html
		template = jinja_environment.get_template('templates/landing.html')
		self.response.out.write(template.render(template_values))

app = webapp2.WSGIApplication([('/', landing)],debug=True)