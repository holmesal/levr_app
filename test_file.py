#import webapp2
#from datetime import datetime
#from datetime import timedelta
##from dateutil.relativedelta import relativedelta
#import time
#import logging
#import levr_classes as levr
#from google.appengine.ext import db
#from google.appengine.api import images

#class Im(db.Model):
#	gar = db.StringProperty(default='asdas')
#	img = db.BlobProperty()
#	date = db.DateTimeProperty()
#	d = db.DateTimeProperty()

#class Test(webapp2.RequestHandler):
#	def get(self):
##		plus = datetime.now()+datetime.timedelta(days=+1)
##		m = TestClass.gql("WHERE now_date <:1",plus)
##		logging.info(m.count())
##		t = TestClass()
##		t.now_date = datetime.now()+relativedelta(days=+7)
##		t.put()
##		x = db.get(t.key())
##		a = datetime.now()+ relativedelta(days=+7)
##		b = datetime.now()
##		logging.info(a)
##		self.response.out.write(b)
##		self.response.out.write("<br/>")
##		self.response.out.write(a)
##		self.response.out.write("<br/>")
##		self.response.out.write(x.auto_date)

#		i = Im()
#		i.d = datetime.now() + timedelta(days=7)
#		logging.info(datetime.now())
#		logging.info(i.d)
#		
#		i.date = datetime.strptime('2012-07-18 18:09:27.432510','%Y-%m-%d %H:%M:%S.%f')
#		logging.info(i.date)
#		i.put()
#		logging.info(i)
#app = webapp2.WSGIApplication([('/test', Test)],
#                              debug=True)

def go(x,y):
	try:
		raise Exception('ggg')
		try:
			pass#z = 1/0
		except Exception, err:
			print "else error ", err
	except Exception as e:
		print "error: ", e.args
	else:
		print "else"
	finally:
		print "final statement"

