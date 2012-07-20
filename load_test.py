import webapp2
import json
import levr_classes as levr
from datetime import datetime
import urllib2
from google.appengine.api import urlfetch
import logging
from google.appengine.ext import db
import time

def set_action(action):
	return {
		'signup'	: {
						'action': 'signup',
						'in'	: {
							'email'	: '',
							'alias'	: '',
							'pw'	: ''
						}
		},
		'login'		: {
						'action': 'login',
						'in'	: {
							'email_or_owner': '',
							'pw'			: ''
						}
		},
		'dealResults':{
						'action': 'dealResults',
						'in'	: {
							'primaryCat': 'pat',
							'start'		: '0',
							'size'		: '20'
						}
		},
		'getUserFavs':{
						'action': 'getUserFavs',
						'in'	: {
							'uid'		: '',
							'dealID'	: '',
							'primaryCat': ''
						}
		},
		'addFav'	: {
						'action': 'addFav',
						'in'	: {
							'uid'		: '',
							'dealID'	: '',
							'primaryCat': ''
						}
		},
		'delFav'	: {
						'action': 'dealFav',
						'in'	: {
							'uid'	: '',
							'dealID': ''
						}
		},
		'getOneDeal': {
						'action': 'getOneDeal',
						'in'	: {
							'dealID'	: '',
							'primaryCat': ''
						}
		},
		'getMyDeals': {
						'action': 'getMyDeals',
						'in'	: {
							'uid' 	: ''
						}
		},
		'getMyStats': {
						'action': 'getMyStats',
						'in'	: {
							'uid' 	: ''
						}
		},
		'redeem'	: {
						'action':'redeem',
						'in'	: {
							'uid'	: '',
							'dealID': ''
						}
		},
		'cashOut'	: {
						'action': 'cashOut',
						'in'	: {
							'uid'	: ''
						}
		}
	}[action]

#class LoadTest(webapp2.RequestHandler):
#	def get(self):
try:
#	self.response.out.write("running...")
	url 	= "http://getlevr.appspot.com/phone"
#			url		= "http://0.0.0.0:8080/phone"
	actions = [ 'dealResults',	#0
				'getUserFavs',	#1
				'addFav',		#2
				'delFav',		#3
				'getOneDeal',	#4
				'getMyDeals',	#5
				'getMyStats',	#6
				'redeem']		#7
#			primary_cat = self.request.get('primary_cat')
	action = actions[0]
	data = set_action(action)
	
	
#	code = 200
#	count = 0
#	while int(code) == 200:
#	count += 1
#				self.response.out.write(data)
	data = json.dumps(data)
	result = urlfetch.fetch(url=url,
							payload=data,
							method=urlfetch.POST,
							headers={'Content-Type':'application/json'})
#				logging.info(dir(result))
#	logging.info(count)
	logging.info(result.status_code)
	logging.info(result.content)
	code = result.status_code
	
#	time.sleep(15000)
#				self.response.out.write(count)
	
							
except:
	levr.log_error()
finally:
	logging.info('Load hath been tested')
			
#app = webapp2.WSGIApplication([('/test/run_load_test',LoadTest)],
#                              debug=True)