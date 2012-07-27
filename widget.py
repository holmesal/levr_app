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
#dealtype - bundle or 
#dealitem -

class RemoteHandler(webapp2.RequestHandler):
	def get(self):
		'''Creates a list of deal objects to put plugged into an iframe'''
		try:
			#identify the business who is requesting their deals
			businessID 	= self.request.get('id')
			logging.debug(businessID)
			businessID 	= enc.decrypt_key(businessID)
			logging.debug(businessID)
			action		= self.request.get('action')
			
			if action != 'success':
				'''Action is to show list of deals'''
				action = 'show'
				#grab the deals for the business
				deals = levr.Deal.gql("WHERE ANCESTOR IS :1", businessID)
				logging.debug(deals)
				if not deals:
					#business does not have any deals
					self.response.out.write('No deals!')
					plugs = []
				else:
					#grab/format the necessary information for each deal
					plugs = [levr.phoneFormat(deal,'widget') for deal in deals]
			else:
				plugs = []		
			#check loginstate of user viewing the deal
			headerData = levr_utils.loginCheck(self,False)
			headerData['loggedIn'] = False
#			self.response.out.write(headerData)
			template_values = {
				'headerData'	: headerData,
				'businessID'	: enc.encrypt_key(businessID),
				'deals'			: plugs,
				'action'		: action
			}
			
			logging.debug(template_values)
		
			jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
			template = jinja_environment.get_template('templates/widget.html')
			self.response.out.write(template.render(template_values))
			
		except:
			levr.log_error()

class LoggedInFavHandler(webapp2.RequestHandler):
	def get(self):
		try:
			dealID		= enc.decrypt_key(self.request.get('deal'))
			businessID	= self.request.get('id') #do not decrypt
			session		= get_current_session()
			customer_key= enc.decrypt_key(session['uid'])
			customer	= levr.Customer.get(customer_key)
			fav			= levr.Favorite(parent=customer.key())
			fav.dealID	= dealID
			fav.put()
			self.redirect('/widget/remote?action=success')
		except:
			levr.log_error()
			self.redirect('/widget/remote?success=False')
class LocalPageHandler(webapp2.RequestHandler):
	def get(self):
		dealID 	= enc.decrypt_key(self.request.get('id'))
		deal	= levr.Deal.get(dealID)
		business= levr.Business.get(deal.businessID)
		deal	= levr.phoneFormat(deal,'list')
		headerData = levr_utils.loginCheck(self,False)
		headerData['loggedIn'] = False
		template_values = {
			'headerData': headerData,
			'deal'		: deal,
			'business'	: business
		}
		jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
		template = jinja_environment.get_template('templates/widget-welcome.html')
		self.response.out.write(template.render(template_values))
		
		
app = webapp2.WSGIApplication([('/widget/remote', RemoteHandler),
								('/widget/add', LoggedInFavHandler),
								('.widget/welcome', LocalPageHandler)
								], debug=True)
