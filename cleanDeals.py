#import webapp2
#import levr_classes as levr
#from datetime import datetime
#from dateutil.relativedelta import relativedelta
##import logging
#from google.appengine.ext import db



#class Cleaner(webapp2.RequestHandler):
#	def get(self):
#		now = datetime.now()+relativedelta(days=+20)
#		expired = levr.CustomerDeal.gql("WHERE date_end <:1",now)
#		logging.info("FLAG!")
#		logging.info(expired.count())
#		#grab all associations
#		for deal in expired:
#			deal_key = deal.key()
#			deal_parent = deal_key.parent()
#			categories = levr.Category.gql("WHERE ANCESTOR IS :1",deal_key)
#			deal.delete()
#			#create new expired deal entity
#			e = levr.ExpiredDeal(parent=deal_parent,key=deal_key)
##			business_name
##			secondary_name
##			deal_type
##			deal_item
##			description
##			discount_value
##			discount_type
##			date_start
##			#date_uploaded
##			date_end
#			
#			
#			
#app = webapp2.WSGIApplication([('/cleanDeals', Cleaner)],
#                              debug=True)
