import os
import webapp2
import levr_classes as levr
import levr_encrypt	as enc
import levr_utils
#from google.appengine.ext import db
#from google.appengine.api import images
import logging
import jinja2
from gaesessions import get_current_session
#from datetime import datetime

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class Pending(webapp2.RequestHandler):
	def get(self):
		#grab all the deals with current status == pending
		deal = levr.CustomerDeal.all().filter('deal_status =', 'pending').get()
		
		#dictify deal
		if deal:
			#logging.info(deal['dateEnd'])
			#get the first matching entity and parse into template values
			
			business = levr.Business.get(deal.businessID)
			
			template_values = {
				"deal"		: deal,
				"business"	: business
			}
			logging.debug(template_values)
			
			template = jinja_environment.get_template('templates/admin_pending.html')
			self.response.out.write(template.render(template_values))
		else:
			self.response.out.write('No pending deals!')
	

class Approve(webapp2.RequestHandler):
	#insert into database and redirect to Pending for next pending deal
	def post(self):
		try:
			levr_utils.dealCreate(self,'pending')
			self.response.out.write('<a href="/admin/pending">Success</a>')
#			self.redirect('/admin/pending')
		except:
			levr.log_error(self.request.body)
			self.response.out.write('Upload Unsuccessful. Check error log')

		
class Reject(webapp2.RequestHandler):
	def post(self):
		inputs = self.request.get
		dealID = enc.decrypt_key(inputs('dealID'))
		deal = levr.CustomerDeal.get(dealID)
		deal.deal_status = 'rejected'
		deal.reject_message = self.request.get('reject_message')
		deal.put()
		self.redirect('/admin/pending')
		
class GodLoginHandler(webapp2.RequestHandler):
	def get(self):
		'''This handler allows an admin to log in to any merchants account to manage it'''
		#grab ALLL of the business Owners, sorted alphabetically
		owners = levr.BusinessOwner.all().order('-email').fetch(None)
		data = []
		for o in owners:
			things = {
					"email":o.email,
					"business":o.businesses.get().business_name,
					"id":str(o.key())
					}
			logging.debug(things)
			data.append(things)
		logging.debug(data)
		#grab all of the businesses
		businesses = levr.Business.all().order('-business_name').fetch(None)
		
		template_values = {
						'owners':data,
						'businesses':businesses
						}
		
		template = jinja_environment.get_template('templates/god_login.html')
		self.response.out.write(template.render(template_values))
	def post(self):
		logging.debug(self.request.body)
		owner_id = self.request.get('owner_id')
		
		owner = levr.BusinessOwner.get(owner_id)
		
		session = get_current_session()
		session['ownerID'] = enc.encrypt_key(owner_id)#business.key())
		session['loggedIn'] = True
		session['validated'] = owner.validated
		self.redirect('/merchants/manage')
app = webapp2.WSGIApplication([('/admin/pending', Pending),
								('/admin/approve', Approve),
								('/admin/reject',Reject),
								('/admin/merchants', GodLoginHandler)
								],debug=True)
