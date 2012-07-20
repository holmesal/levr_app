import os, sys
import webapp2
import levr_classes as levr
import levr_utils
from google.appengine.ext import db
import logging
import jinja2

from gaesessions import get_current_session

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class share(webapp2.RequestHandler):
	def get(self):
		#grab refKey
		dealID = self.request.get('id')
		logging.info(dealID)
		error = self.request.get('error')
		success = self.request.get('success')
		
		#propogate user-entered values
		email_or_owner = self.request.get('email_or_owner')
		email = self.request.get('email')
		username = self.request.get('username')
		
		#grab deal from datastore
		try:
			deal = levr.Deal.get(dealID)
		except:
			logging.error('Could not grab deal. id passed: ' + dealID)
			sys.exit()
			
		if deal:
			#check loginstate
			headerData = levr_utils.loginCheck(self,False)
			
			#get alias from parent (ninja)
			ninja = levr.Customer.get(deal.key().parent())
			alias = ninja.alias
			
			#format deal
			dealFormatted = levr.phoneFormat(deal,'list')
			
			template_values = {
				'headerData' : headerData,
				'title' : 'Share',
				'deal'	: deal,
				'dealID': dealID,
				'alias'	: alias,
				'dealText'	: dealFormatted['dealText'],
				'dealTextExtra'	: dealFormatted['dealTextExtra'],
				'description'	: deal.description,
				'error'			: error,
				'success'		: success,
				'email_or_owner'	: email_or_owner,
				'email'	: email,
				'username'	: username
			}
			
			#jinja2
			template = jinja_environment.get_template('templates/share.html')
			self.response.out.write(template.render(template_values))

			
			
			
		else:
			self.redirect('/error')
		logging.info(deal.__dict__)
		
		
class loginFav(webapp2.RequestHandler):
	def post(self):
		#login, then add
		email_or_owner = self.request.get('email_or_owner')
		pw = self.request.get('pw')
		
		session = get_current_session()
		
		dealID = self.request.get('id')
		
		#attempt login
		response = levr_utils.loginCustomer(email_or_owner,pw)
		logging.info(response)
		if response['success'] == True:
			#grab customer
			customer = levr.Customer.get(response['uid'])
			#if matched, pull properties and set loginstate to true
			session['uid'] = customer.key()
			session['alias'] = customer.alias
			session['loggedIn'] = True
			#add deal to fav
			fav = levr.Favorite(parent=customer.key())
			fav.dealID = dealID
			fav.put()
			#redirect to success page
			self.redirect('/share/deal?id=' + dealID + '&success=1')
		else:
			#show login page again, with login error
			self.redirect('/share/deal?id='+dealID+'&error=login&email_or_owner='+email_or_owner)
			
	
class signupFav(webapp2.RequestHandler):
	def post(self):
		#pull signup info from post
		email = self.request.get('email')
		alias = self.request.get('alias')
		pw = self.request.get('pw')
		
		dealID = self.request.get('id')
		
		logging.info(len(pw))
		logging.info(type(len(pw)))
		
		if len(pw) < 6:
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
				session['uid'] = customer.key()
				session['alias'] = customer.alias
				session['loggedIn'] = True
				
				self.redirect('/share/deal?id=' + dealID + '&success=1')
			else:
				self.redirect('/share/deal?id='+dealID+'&error='+response['field']+'&email='+email+'&username='+alias)

class loggedInFav(webapp2.RequestHandler):
	def get(self):
		dealID = self.request.get('id')
		
		session = get_current_session()
		
		customerKey = session['uid']
		
		customer = levr.Customer.get(customerKey)
		
		fav = levr.Favorite(parent=customer.key())
		fav.dealID = dealID
		fav.put()
		
		self.redirect('/share/deal?id=' + dealID + '&success=1')
	
class success(webapp2.RequestHandler):
	def get(self):
		print('success!')

app = webapp2.WSGIApplication([('/share/deal.*', share),('/share/success', success),('/share/signupFav', signupFav),('/share/loginFav', loginFav), ('/share/loggedInFav', loggedInFav)],debug=True)
