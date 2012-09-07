import os
import webapp2
import jinja2
import logging

class ninjas(webapp2.RequestHandler):
	def get(self):
		#launch the jinja environment
		jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
		
		#check user-agent to see if user is mobile or not
		#get the user-agent
		uastring = str(self.request.headers['user-agent'])
		
		if 'Mobile' in uastring:
			logging.info('THIS IS A MOBILE DEVICE')
			#serve mobile landing page
			template = jinja_environment.get_template('templates/ninjas_landing_mobile.html')
		else:
			logging.info('THIS IS A DESKTOP DEVICE')
			#serve desktop landing page
			template = jinja_environment.get_template('templates/ninjas_landing.html')
		
		self.response.out.write(template.render())

app = webapp2.WSGIApplication([('/ninjas', ninjas)],debug=True)