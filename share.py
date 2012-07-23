import os
import webapp2
import levr_classes as levr
import levr_encrypt as enc
import levr_utils
#from google.appengine.ext import db
import logging
import jinja2

from gaesessions import get_current_session

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class share(webapp2.RequestHandler):
	def get(self):
		try:
			#grab refKey
			logging.info(self.request.get('id'))
			dealID = enc.decrypt_key(str(self.request.get('id')))
			logging.info(str(dealID))
			error = self.request.get('error')
			success = self.request.get('success')
		
			#propogate user-entered values
			email_or_owner = self.request.get('email_or_owner')
			email = self.request.get('email')
			username = self.request.get('username')
			
			deal = levr.Deal.get(dealID)
			#grab deal from datastore
#			try:
#				
#			except:
#				logging.error('Could not grab deal. id passed: ' + dealID)
#				sys.exit()
#			
			if deal:
				#check loginstate
				headerData = levr_utils.loginCheck(self,False)
			
				#get alias from parent (ninja)
				###!!!! This is only valid if dealis a customer deal
				ninja = levr.Customer.get(deal.key().parent())
				alias = ninja.alias
			
				#format deal
				dealFormatted = levr.phoneFormat(deal,'list')
			
				template_values = {
					'headerData' 	: headerData,
					'title' 		: 'Share',
					'deal'			: deal,
					'dealID'		: enc.encrypt_key(dealID),
					'alias'			: alias,
					'dealText'		: dealFormatted['dealText'],
					'dealTextExtra'	: dealFormatted['dealTextExtra'],
					'description'	: deal.description,
					'error'			: error,
					'success'		: success,
					'email_or_owner': email_or_owner,
					'email'			: email,
					'username'		: username
				}
			
				#jinja2
				template = jinja_environment.get_template('templates/share.html')
				self.response.out.write(template.render(template_values))
			else:
				self.redirect('/error')
			logging.info(deal.__dict__)
		except:
			levr.log_error()
		
class loginFav(webapp2.RequestHandler):
	def post(self):
		try:
			logging.info('!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!')
			#login, then add
			email_or_owner = self.request.get('email_or_owner')
			logging.info(email_or_owner)
			pw = self.request.get('pw')
			logging.info(pw)
			logging.info(enc.encrypt_password(pw))
			session = get_current_session()
		
			dealID = enc.decrypt_key(self.request.get('id'))
			logging.info(dealID)
			#attempt login
			response = levr_utils.loginCustomer(email_or_owner,pw)
			logging.info(response)
			if response['success'] == True:
				#grab customer
				customer = levr.Customer.get(enc.decrypt_key(response['uid']))
				#if matched, pull properties and set loginstate to true
				session['uid'] = enc.encrypt_key(customer.key())
				session['alias'] = customer.alias
				session['loggedIn'] = True
				#add deal to fav
				fav = levr.Favorite(parent=customer.key())
				fav.dealID = dealID
				fav.put()
				#redirect to success page
				dealID = enc.encrypt_key(dealID)
				self.redirect('/share/deal?id=' + dealID + '&success=1')
			else:
				dealID = enc.encrypt_key(dealID)
				#show login page again, with login error
				self.redirect('/share/deal?id='+dealID+'&error=login&email_or_owner='+email_or_owner)
		except:
			levr.log_error()
	
class signupFav(webapp2.RequestHandler):
	def post(self):
		try:
			#pull signup info from post
			email = self.request.get('email')
			alias = self.request.get('alias')
			pw = self.request.get('pw')
		
			dealID = enc.decrypt_key(self.request.get('id'))
		
			logging.info(len(pw))
			logging.info(type(len(pw)))
		
			if len(pw) < 5:
				dealID = enc.encrypt_key(dealID)
				self.redirect('/share/deal?id='+dealID+'&error=password'+'&email='+email+'&username='+alias)
			else:

				session = get_current_session()
			
				response = levr_utils.signupCustomer(email,alias,pw)
			
				if response['success']:
					#add to favorites
					customer = levr.Customer.get(response['uid'])
					fav = levr.Favorite(parent=customer.key())
					fav.dealID = dealID
					fav.put()
					#login user
					session['uid'] = enc.encrypt_key(customer.key())
					session['alias'] = customer.alias
					session['loggedIn'] = True
					dealID = enc.encrypt_key(dealID)
					self.redirect('/share/deal?id=' + dealID + '&success=1')
				else:
					dealID = enc.encrypt_key(dealID)
					self.redirect('/share/deal?id='+dealID+'&error='+response['field']+'&email='+email+'&username='+alias)
		except:
			levr.log_error()
class loggedInFav(webapp2.RequestHandler):
	def get(self):
		try:
			dealID = enc.decrypt_key(self.request.get('id'))
		
			session = get_current_session()
		
			customerKey = enc.decrypt_key(session['uid'])
		
			customer = levr.Customer.get(customerKey)
		
			fav = levr.Favorite(parent=customer.key())
			fav.dealID = dealID
			fav.put()
		
			dealID = enc.encrypt_key(dealID)
			self.redirect('/share/deal?id=' + dealID + '&success=1')
		except:
			levr.log_error()
class success(webapp2.RequestHandler):
	def get(self):
		print('success!')

app = webapp2.WSGIApplication([('/share/deal.*', share),
								('/share/success', success),
								('/share/signupFav', signupFav),
								('/share/loginFav', loginFav), 
								('/share/loggedInFav', loggedInFav)],
								debug=True)
