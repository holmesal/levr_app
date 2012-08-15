import os
import webapp2
import levr_classes as levr
import levr_encrypt	as enc
import levr_utils
from google.appengine.ext import db
#from google.appengine.api import images
import logging
import jinja2
from datetime import datetime

#dealtype - bundle or 
#dealitem -

class Pending(webapp2.RequestHandler):
	def get(self):
		#grab all the deals with current status == pending
		deal = levr.CustomerDeal.gql('WHERE deal_status=:1','pending').get()
		#dictify deal
		if deal:
			#logging.info(deal['dateEnd'])
			#get the first matching entity and parse into template values
			self.response.headers['Content-Type'] = 'text/html'	
			
			business = levr.Business.get(deal.businessID)
			business = business.dictify()
			deal = deal.dictify()
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
		try:
			levr_utils.dealCreate(self,'phone')
			self.response.out.write('<a href="/admin/pending">Success</a>')
#			self.redirect('/admin/pending')
		except:
			levr.log_error(self.request.body)
			self.response.out.write('Upload Unsuccessful. Check error log')
			
#		#create alias for self.request.get
#		inputs = self.request.get
#		#dealID is pulled from admin/approve?dealID=dealID
#		dealID = enc.decrypt_key(inputs('dealID'))
#		#grabs deal object from database and updates information
#		deal 					= db.get(dealID)
#		deal.businessID			= enc.decrypt_key(inputs('businessID'))
#		deal.business_name		= inputs('businessName')
#		deal.vicinity			= inputs('vicinity')
#		deal.deal_status		= 'active'
#		deal.gate_requirement	= int(inputs('gateRequirement'))
#		deal.gate_payment_per	= int(inputs('gatePaymentPer'))
#		deal.gate_max			= int(inputs('gateMax'))
#		deal.geo_point			= levr.geo_converter(inputs('geoPoint'))
#		deal.description		= inputs('description')
#		##new properties
#		deal.deal_text		= inputs('deal_text')
#		deal.deal_type		= inputs('deal_type') #single or bundle
#		deal.secondary_name	= inputs('secondaryName') #### check name!!!
#		deal.date_start		= datetime.now()
#		deal.date_end		= datetime.strptime(inputs('dateEnd'),'%Y-%m-%d %H:%M:%S.%f')
#		
#		logging.info(deal.__dict__)
#		
#		#parse tags from all the inputs
#		tags = []
#		tags.extend(levr.tagger(deal.business_name))
#		tags.extend(levr.tagger(deal.description))
#		tags.extend(levr.tagger(deal.secondary_name))
#		tags.extend(levr.tagger(inputs('tags')))
#		
#		#set tags list to the deal object
#		deal.tags = tags
#		deal.put()
		
#		
		
class Reject(webapp2.RequestHandler):
	def post(self):
		inputs = self.request.get
		dealID = enc.decrypt_key(inputs('dealID'))
		deal = levr.CustomerDeal.get(dealID)
		deal.deal_status = 'rejected'
		deal.put()
		self.redirect('/admin/pending')
		

app = webapp2.WSGIApplication([('/admin/pending', Pending),
								('/admin/approve', Approve),
								('/admin/reject',Reject)],
								debug=True)
