import webapp2
import levr_classes as levr
from datetime import datetime
#import logging
from google.appengine.ext import db



class Cleaner(webapp2.RequestHandler):
	def get(self):
		try:
			now = datetime.now()+relativedelta(days=+20)
			expired = levr.CustomerDeal.gql("WHERE deal_status=:'active' AND date_end <:1",now)
			for x in expired:
				x.deal_status = "expired"
				x.push()
			
		except:
			levr.log_error()
		else:
			logging.info('Deals have been cleaned')
			
app = webapp2.WSGIApplication([('/tasks/cleanDeals', Cleaner)],
                              debug=True)
