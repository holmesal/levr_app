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

class MainHandler(webapp2.RequestHandler):
	def get(self):
		'''Creates a list of deal objects to put plugged into an iframe'''
		try:
			#identify the business who is requesting their deals
			businessID 	= self.request.get('id')
			logging.debug(businessID)
			businessID 	= enc.decrypt_key(businessID)
			logging.debug(businessID)
			action		= self.request.get('action')
			
			if action == 'login':
				'''Action is login. only grab a single deal'''
				dealID 		= self.request.get('deal')
				businessID	= self.request.get('businessID') #do not decrypt
				username	= self.request.get('username')
				email		= self.request.get('email')
				error		= self.request.get('error')
				template_values = {
					"dealID"	: dealID,
					"businessID": businessID, #not encrypted
					"username"	: username,
					"email"		: email,
					"error"		: error,
					"action"	: action
				}
			else:
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
					plugs = [levr.phoneFormat(deal,'plug') for deal in deals]
						
				#check loginstate of user viewing the deal
				headerData = levr_utils.loginCheck(self,False)
				self.response.out.write(headerData)
				headerData['loggedIn'] = False
				template_values = {
					'headerData'	: headerData,
					'businessID'	: enc.encrypt_key(businessID),
					'deals'			: plugs,
					'action'		: action
				}
			
			logging.debug(template_values)
		
			jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
			template = jinja_environment.get_template('templates/plug.html')
			self.response.out.write(template.render(template_values))
			
		except:
			levr.log_error()

class LoggedInFavHandler(webapp2.RequestHandler):
	def get(self):
		dealID		= enc.decrypt_key(self.request.get('id'))
		businessID	= self.request.get('b') #do not decrypt
		session		= get_current_session()
		customer_key= enc.decrypt_key(session['uid'])
		customer	= levr.Customer.get(customer_key)
		fav			= levr.Favorite(parent=customer.key())
		fav.dealID	= dealID
		fav.put()
		self.redirect('/plug/show?id='+businessID)

class LoginFavHandler(webapp2.RequestHandler):
	def post(self):
		try:
			logging.info('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
			#inputs from login or signup form
			email_or_owner = self.request.get('email_or_owner')
			pw	 		= self.request.get('pw')
			session 	= get_current_session()
			dealID		= enc.decrypt_key(self.request.get('deal'))
			businessID	= self.request.get('id') #do not encrypt
			#attempt login
			response = levr_utils.loginCustomer(email_or_owner,pw)
			logging.info(response)
			if response['success'] == True:
				#grab customer
				customer = levr.Customer.get(enc.decrypt_key(response['uid']))
				#set cookie parameters for user
				session['uid'] 		= enc.encrypt_key(customer.key())
				session['alias'] 	= customer.alias
				session['loggedIn'] = True
				#add deal to customer's favorite
				fav = levr.Favorite(parent=customer.key())
				fav.dealID = dealID
				fav.put()
				#redirect to widget homepage
				dealID 		= enc.encrypt_key(dealID)
				businessID 	= enc.encrypt_key(businessID)
				self.redirect('/plug/show?id=' + businessID + '&success=1')
			else:
				dealID = enc.encrypt_key(dealID)
				#show login page again, with login error
				self.redirect('/plug/show?id='+dealID+'&error=login&email_or_owner='+email_or_owner+'&action=login')
		except:
			levr.log_error()
class SignupFavHandler(webapp2.RequestHandler):
	def post(self):
		try:
			#pull signup info from post
			email 	= self.request.get('email')
			alias 	= self.request.get('alias')
			pw 		= self.request.get('pw')
		
			dealID 		= enc.decrypt_key(self.request.get('deal'))
			businessID	= self.request.get('id')
			logging.info(len(pw))
			logging.info(type(len(pw)))
		
			if len(pw) < 5:
				dealID = enc.encrypt_key(dealID)
				self.redirect('/plug/show?deal='+dealID+'&id='+businessID+ '&error=password'+'&email='+email+'&username='+alias+'&action=login')
			else:
				session = get_current_session()
				response = levr_utils.signupCustomer(email,alias,pw)
				if response['success']:
					#add to favorites
					uid = enc.decrypt_key(response['uid'])
					customer = levr.Customer.get(uid)
					fav = levr.Favorite(parent=customer.key())
					fav.dealID = dealID
					fav.put()
					#login user
					session['uid'] = enc.encrypt_key(customer.key())
					session['alias'] = customer.alias
					session['loggedIn'] = True
					dealID = enc.encrypt_key(dealID)
					self.redirect('/plug/show?deal='+dealID+'&id='+businessID+ '&action=show')
				else:
					dealID = enc.encrypt_key(dealID)
					self.redirect('/plug/show?deal='+dealID+'&id='+businessID+'&error='+response['field']+'&email='+email+'&username='+alias+'&action=login')
		except:
			levr.log_error()
app = webapp2.WSGIApplication([('/plug/show', MainHandler),
								('/plug/add', LoggedInFavHandler),
								('/plug/login', LoginFavHandler),
								('/plug/signup', SignupFavHandler)
								], debug=True)
