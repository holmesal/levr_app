import webapp2
import levr_classes as levr
from datetime import datetime
import urllib2
from google.appengine.api import urlfetch
import logging
from google.appengine.ext import db



class LoadTest(webapp2.RequestHandler):
	def get(self):
		try:
			url 	= "http://getlevr.appspot.com/phone"
			actions = [ 'dealResults',	#0
						'getUserFavs',	#1
						'addFav',		#2
						'delFav',		#3
						'getOneDeal',	#4
						'getMyDeals',	#5
						'getMyStats',	#6
						'redeem']		#7
			action = actions[4]
#			inp = {
#				''
#			}
			
			
		except:
			levr.log_error()
		finally:
			logging.info('Load hath been tested')
			
app = webapp2.WSGIApplication([('/test/run_load_test',RunTest),
								('/test/dealResults', DealResults),
								('/test/getUserFavs',GetUserFavs),
								('/test/addFav', AddFav),
								('/test/delFav', DelFav),
								('/test/getOneDeal', GetOneDeal),
								('/test/getMyDeals', GetMyDeals),
								('/test/getMyStats', GetMyStats),
								('/test/redeem', Redeem)],
                              debug=True)
