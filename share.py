import os, sys
import webapp2
import levr_classes as levr
import levr_utils
from google.appengine.ext import db
from google.appengine.api import images
import logging
import jinja2

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class share(webapp2.RequestHandler):
	def get(self):
		#grab refKey
		refKey = self.request.get('refKey')
		logging.info(refKey)
		#grab deal from datastore
		try:
			deal = levr.Deal.get(refKey)
		except:
			logging.error('Could not grab deal. refKey passed: ' + refKey)
			sys.exit()
		
		if deal:
			logging.info('found!')
		else:
			logging.info('empty!')
		logging.info(refKey)
		logging.info(deal.__dict__)
		
		#check loginstate
		headerData = levr_utils.loginCheck(self,False)
		
		template_values = {
			'headerData' : headerData,
			'title' : 'Share',
			'deal'	: deal,
			'refKey': refKey
		}
		
		#jinja2
		template = jinja_environment.get_template('templates/share.html')
		self.response.out.write(template.render(template_values))

class loginFav(webapp2.RequestHandler):
	def post(self):
		#login, then add
		email = self.request.get('email_or_owner')
		pw = self.request.get('pw')
		
		logging.info(self.request.headers)
		
		session = get_current_session()
		
		#attempt login
		response = levr_utils.loginCustomer()
		#query database for matching email and pw
		q = levr.Customer.gql("WHERE email = :email and pw = :pw",email=email,pw=pw)
		customer = q.get()
		logging.info(customer)
		if customer != None:
			#if matched, pull properties and set loginstate to true
			session['uid'] = customer.key()
			session['alias'] = customer.alias
			session['loggedIn'] = True
			#add deal to fav
			fav = levr.Favorite()
			fav.uid = customer.key().__str__()
			
			#redirect to success page
			self.redirect('/share/success')
		else:
			#show login page again
			pass
			
	
class signupFav(webapp2.RequestHandler):
	def post(self):
		#pull signup info from post
		email = self.request.get('email')
		alias = self.request.get('alias')
		pw = self.request.get('pw')
		
		response = levr_utils.signupCustomer(email,alias,pw)
		
		if response['success']:
			self.response.out.write(response)
			self.redirect('/share/success')
		else:
			self.response.out.write('Not okay!')
			self.response.out.write(response)
			
		
	
class success(webapp2.RequestHandler):
	def get(self):
		print('success!')

app = webapp2.WSGIApplication([('/share/deal.*', share),('/share/success', success),('/share/signupFav', signupFav)],debug=True)
