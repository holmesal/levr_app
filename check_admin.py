#import webapp2
#import os
import logging
#import jinja2
import levr_classes as levr

from gaesessions import get_current_session

def loginCheck(self,strict):
	'''This is a general-purpose login checking function
	   in "strict" mode (strict=True), this script will bounce to the login page if not logged in
	   if strict=False, headers will be returned that indicate the user isn't logged in, but no bouncing'''
	session = get_current_session()
	logging.info(session)
	if session.has_key('loggedIn') == False or session['loggedIn'] == False:
		if strict == True:
			#not logged in, bounce to login page
			logging.info('Not logged in. . .Bouncing!')
			self.redirect('/login')
		else:
			logging.info('Not logged in. . .Sending back headerData')
			headerData = {
				'loggedIn'	: False
			}
			return headerData
	elif session.has_key('loggedIn') == True and session['loggedIn'] == True:
		#logged in, grab the useful bits
		headerData = {
			'loggedIn'		: session['loggedIn'],
			'alias' : session['alias'],
			'businessID'	: session['businessID']
		}
		#return user metadata.
		return headerData
		#return session['businessID']
	return

def signupCustomer(email,alias,pw):
	'''Check availability of username+pass, create and login if not taken'''
	#check availabilities
	q_email = levr.Customer.gql('WHERE email = :1',email)
	q_alias  = levr.Customer.gql('WHERE alias = :1',alias)
	r_email = q_email.get()
	r_alias = q_alias.get()
	
	if r_email == None and r_alias == None: #nothing found
		c = levr.Customer()
		c.email = email
		c.pw = pw
		c.alias = alias
		#put
		c.put()
		return {'success':True,'uid':c.key().__str__()}
	elif r_email != None:
		return {
			'success': False,
			'field': 'email',
			'error': 'That email is already registered. Try again!'
		}
	elif r_alias != None:
		return {
			'success': False,
			'field': 'alias',
			'error': 'That nickname is already registered. Try again!'
		}
		
def loginCustomer(email_or_owner,pw):
	'''This is passed either an email or a username, so check both'''
	q_email = levr.Customer.gql('WHERE email = :1',email_or_owner)
	q_owner  = levr.Customer.gql('WHERE alias = :1',email_or_owner)
	r_email = q_email.get()
	r_owner = q_owner.get()
	if r_email != None:
		#found user on the basis of email
		return {
			'success'	: True,
			'uid'		: r_email.key().__str__()
		}
	elif r_owner != None:
		#found user on the basis of username
		return {
			'success'	: True,
			'uid'		: r_owner.key().__str__()
		}
	else:
		return {
			'success'	: False
		}
	
