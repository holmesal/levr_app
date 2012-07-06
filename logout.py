import os
import webapp2
import jinja2
import logging

from gaesessions import get_current_session

class logout(webapp2.RequestHandler):
	def get(self):
		#logout the user
		session = get_current_session()
		session['loggedIn'] = False
		session.terminate()
		logging.info(session)
		
		#redirect to the landing page for merchants
		self.redirect('/merchants')

app = webapp2.WSGIApplication([('/logout', logout)],debug=True)