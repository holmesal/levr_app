import os
import webapp2
import levr_classes as levr
import levr_encrypt	as enc
import levr_utils
#from google.appengine.ext import db
#from google.appengine.api import images
import logging
import jinja2
#from datetime import datetime


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
			logging.debug(template_values)
			jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
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
		

app = webapp2.WSGIApplication([('/admin/pending', Pending),
								('/admin/approve', Approve),
								('/admin/reject',Reject)],
								debug=True)
