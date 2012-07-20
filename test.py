import webapp2
from datetime import datetime
from datetime import timedelta
#from dateutil.relativedelta import relativedelta
import time
import logging
import levr_classes as levr
from google.appengine.ext import db
from google.appengine.api import images

class Im(db.Model):
	gar = db.StringProperty(default='asdas')
	img = db.BlobProperty()
	date = db.DateTimeProperty()
	d = db.DateTimeProperty()

class Test(webapp2.RequestHandler):
	def get(self):
		try:
			a = db.get('nhoiniosdf')
		except:
			levr.log_error()
		self.response.out.write(a)
#		plus = datetime.now()+datetime.timedelta(days=+1)
#		m = TestClass.gql("WHERE now_date <:1",plus)
#		logging.info(m.count())
#		t = TestClass()
#		t.now_date = datetime.now()+relativedelta(days=+7)
#		t.put()
#		x = db.get(t.key())
#		a = datetime.now()+ relativedelta(days=+7)
#		b = datetime.now()
#		logging.info(a)
#		self.response.out.write(b)
#		self.response.out.write("<br/>")
#		self.response.out.write(a)
#		self.response.out.write("<br/>")
#		self.response.out.write(x.auto_date)
		
#		i = Im()
#		i.d = datetime.now() + timedelta(days=7)
#		logging.info(datetime.now())
#		logging.info(i.d)
#		
#		i.date = datetime.strptime('2012-07-18 18:09:27.432510','%Y-%m-%d %H:%M:%S.%f')
#		logging.info(i.date)
#		i.put()
#		logging.info(i)
app = webapp2.WSGIApplication([('/sandbox', Test)],
                              debug=True)

#def divide(x,y):
#	try:
#		r = x/y
#	except err:
#		print "error: ",err
#	else:
#		print "no error, result ", r
#	finally:
#		print "final statement"

