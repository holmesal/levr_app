import os
import webapp2
import levr_classes as levr
from google.appengine.ext import db
from google.appengine.api import images
import logging
import jinja2

class pending(webapp2.RequestHandler):
	def get(self):
		#grab all the deals with current status == pending
		q = levr.Deal.gql('WHERE deal_status=:1','pending')
		
		#get the first matching entity and parse into template values
		
		
		result = q.get()
		
		#self.response.headers['Content-Type'] = 'image/png'
		#self.response.out.write(result.img)
			
		
		template_values = {
			'image_key'				: result.key().__str__(),
			'business_name'			: result.business_name,
			'secondary_name'		: result.secondary_name
		}
		
		logging.info(template_values)
		
		jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
		template = jinja_environment.get_template('templates/admin_pending.html')
		self.response.out.write(template.render(template_values))
		
	def post(self):
		#pahaha
		pass
		
class pendingImage(webapp2.RequestHandler):
	def get(self):
		logging.info(self.request.get('key'))
		
class allImages(webapp2.RequestHandler):
	def get(self):
		q = levr.Deal.gql('WHERE deal_status=:1','pending')
		for result in q:
			logging.info(result.img)
			self.response.headers['Content-Type'] = 'image/png'
			self.response.out.write(result.img)

app = webapp2.WSGIApplication([('/admin/pending', pending),('/admin/pendingImage', pendingImage),('/admin/allImages', allImages)],debug=True)
