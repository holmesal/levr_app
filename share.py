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

class ShareHandler(webapp2.RequestHandler):
	def get(self,identifier):
		try:
			logging.debug(identifier)
			deal = levr.Deal.all().filter('share_id =', identifier)
			logging.debug(deal)
			template_values = {
							'deal':deal
							}
			logging.debug(template_values)
			logging.debug(deal.__str__())
			template = jinja_environment.get_template('templates/share.html')
			self.response.out.write(template.render(template_values))
		except:
			levr.log_error()

app = webapp2.WSGIApplication([('/(.*)', ShareHandler)],
								debug=True)
