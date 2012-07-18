import os
import webapp2
import levr_classes as levr
from google.appengine.ext import db
#from google.appengine.api import images
import logging
import jinja2
from datetime import datetime


class Pending(webapp2.RequestHandler):
	def get(self):
		
		#grab all the deals with current status == pending
		deal = levr.CustomerDeal.gql('WHERE deal_status=:1','pending').get()
		#dictify deal
		if deal:
			deal = deal.dictify()
			#get the first matching entity and parse into template values
			self.response.headers['Content-Type'] = 'text/html'	
			
			business = levr.Business.get(deal['businessID'])
			business = business.dictify()
			template_values = {
				"deal"		: deal,
				"business"	: business
			}
			jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
			template = jinja_environment.get_template('templates/admin_pending.html')
			self.response.out.write(template.render(template_values))
		else:
			self.response.out.write('No pending deals!')
	

class Approve(webapp2.RequestHandler):
	#insert into database and redirect to Pending for next pending deal
	def post(self):
		#create alias for self.request.get
		inputs = self.request.get
		#dealID is pulled from admin/approve?dealID=dealID
		dealID = inputs('dealID')
		#grabs deal object from database and updates information
		deal 					= db.get(dealID)
		deal.businessID			= inputs('businessID')
		deal.business_name		= inputs('businessName')
		deal.deal_status		= 'active'
		deal.gate_requirement	= int(inputs('gateRequirement'))
		deal.gate_payment_per	= int(inputs('gatePaymentPer'))
		deal.gate_max			= int(inputs('gateMax'))
		deal.geo_point			= levr.geo_converter(inputs('geoPoint'))
		
		##new properties
		deal.discount_type	= inputs('discountType')
		deal.discount_value	= float(inputs('discountValue'))
		deal.city			= inputs('city')
		deal.secondary_name	= inputs('name') #### check name!!!
		deal.date_start		= datetime.now()
		deal.date_end		= datetime.strptime(inputs('dateEnd'),'%Y-%m-%d')
		
		logging.info(deal.__dict__)
		deal.put()
		
		#grab all of the primary cats and put
		tags = inputs('tags')
		tags = tags.split(',')
		tags = [tag.strip() for tag in tags]
		for tag in tags:
			category 			 = levr.Category(parent=db.Key(dealID))
			category.primary_cat = tag
			category.put()
		self.response.out.write('<a href="/admin/pending">Success</a>')
#		self.redirect('/admin/pending')
		
class Reject(webapp2.RequestHandler):
	def post(self):
		inputs = self.request.get
		dealID = inputs('dealID')
		deal = levr.CustomerDeal.get(key=dealID)
		deal.deal_status = 'rejected'
		deal.put()
		
class PendingImage(webapp2.RequestHandler):
	def get(self):
		inputs = self.request.get
		dealID = inputs('dealID')
		deal = db.get(dealID)
		self.response.headers['Content-Type'] = 'image/png'
		self.response.out.write(deal.img)
#		key = self.request.get('key')
#		img = levr.CustomerDeal.get(key)
		
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
