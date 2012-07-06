import webapp2
import os
import logging
import jinja2

from gaesessions import get_current_session

def loginCheck(self):
	session = get_current_session()
	logging.info(session)
	if session.has_key('loggedIn') == False or session['loggedIn'] == False:
		#not logged in, bounce to login page
		logging.info('Not logged in. . .Bouncing!')
		self.redirect('/login')
	elif session.has_key('loggedIn') == True or session['loggedIn'] == True:
		#logged in, grab the useful bits
		headerData = {
			'loggedIn'	: session['loggedIn'],
			'contact_owner' : session['contact_owner']
		}
		#return user metadata.
		return headerData
	return