import os
import webapp2
import levr_classes as levr
#from google.appengine.ext import db
#from google.appengine.api import images
import logging
import jinja2

class Pending(webapp2.RequestHandler):
	def get(self):
		#grab all the deals with current status == pending
		deal = levr.CustomerDeal.gql('WHERE deal_status=:1','pending').get()
		#dictify deal
		template_values = deal.format_pending_deal()
		#dealID, business_name, deal_address, geo_location
		
		
		#get the first matching entity and parse into template values
		self.response.headers['Content-Type'] = 'image/png'
		self.response.out.write(deal.img)
		self.response.headers['Content-Type'] = 'text/html'	
		
		
		
		template_values.update({
			'image_key'				: deal.key().__str__(),
		})
		
		logging.info(template_values)
		
		jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
		template = jinja_environment.get_template('templates/admin_pending.html')
		self.response.out.write(template.render(template_values))
		
	def post(self):
		#pahaha
		pass

class Approve(webapp2.RequestHandler):
	#insert into database and redirect to Pending for next pending deal
	pass
class PendingImage(webapp2.RequestHandler):
	def get(self):
		logging.info(self.request.get('key'))
		
class AllImages(webapp2.RequestHandler):
	def get(self):
		q = levr.Deal.gql('WHERE deal_status=:1','pending')
		for result in q:
			logging.info(result.img)
			self.response.headers['Content-Type'] = 'image/png'
			self.response.out.write(result.img)

app = webapp2.WSGIApplication([('/admin/pending', Pending),
								('/admin/pendingImage', PendingImage),
								('/admin/allImages', AllImages),
								('/admin/approve', Approve)],
								debug=True)
