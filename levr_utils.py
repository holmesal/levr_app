#import webapp2
#import os
import logging
#import jinja2

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
	elif session.has_key('loggedIn') == True or session['loggedIn'] == True:
		#logged in, grab the useful bits
		headerData = {
			'loggedIn'		: session['loggedIn'],
			'contact_owner' : session['contact_owner'],
		}
		#return user metadata.
		return headerData
		#return session['businessID']
	return
