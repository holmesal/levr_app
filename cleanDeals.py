#import webapp2
#import levr_classes as levr
#from datetime import datetime
#from dateutil.relativedelta import relativedelta
##import logging
#from google.appengine.ext import db



#class Cleaner(webapp2.RequestHandler):
#	def get(self):
#		now = datetime.now()+relativedelta(days=+20)
#		expired = levr.CustomerDeal("WHERE date_end <:1",now)
#		logging.info("FLAG!")
#		logging.info(expired.count())
#app = webapp2.WSGIApplication([('/cleanDeals', Cleaner)],
#                              debug=True)
