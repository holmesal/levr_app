import webapp2
import os
import logging

from gaesessions import get_current_session

def loginCheck(self):
	session = get_current_session()
	logging.info(session)
	if session.has_key('loggedIn') == False or session['loggedIn'] == False:
		#not logged in, bounce to login page
		logging.error('Bouncing!')
		self.redirect('/login')
	return