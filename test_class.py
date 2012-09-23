#from __future__ import with_statement
#from google.appengine.api import files
import webapp2
import levr_classes as levr
import logging
import levr_encrypt as enc
import levr_utils
import base_62_converter as converter
#import geo.geohash as geohash
import geo.geohash as geohash
from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from datetime import datetime
from random import randint


class MainPage(webapp2.RequestHandler):
	def get(self):
		logging.info('!!!')
		upload_url = blobstore.create_upload_url('/new/upload')
		logging.info(upload_url)
		# The method must be "POST" and enctype must be set to "multipart/form-data".
		self.response.out.write('<html><body>')
		self.response.out.write('<form action="%s" method="POST" enctype="multipart/form-data">' % upload_url)
		self.response.out.write('''Upload File: <input type="file" name="img"><br> <input type="submit"
		name="submit" value="Create!"> </form></body></html>''')

class DatabaseUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		#get uploaded image
		upload = self.get_uploads()[0]
#		upload = self.request.get('img')
#		upload = blobstore.Blob(upload)
		blob_key= upload.key()
		img_key = blob_key
		logging.info(upload)
		
		# new customer
#		c = levr.Customer(key='agtkZXZ-Z2V0bGV2cnIOCxIIQ3VzdG9tZXIYEgw')
		c = levr.Customer()
		c.email	= 'ethan@getlevr.com'
		c.payment_email = c.email
		c.pw 	= enc.encrypt_password('ethan')
		c.alias	= 'alonso'
		c.favorites	= []
		c.put()
		
		#new ninja
#		ninja = levr.Customer(key='agtkZXZ-Z2V0bGV2cnIOCxIIQ3VzdG9tZXIYCww')
		ninja = levr.Customer()
		ninja.email	= 'santa@getlevr.com'
		ninja.payment_email = c.email
		ninja.pw 	= enc.encrypt_password('ethan')
		ninja.alias	= 'ninja'
		ninja.favorites = []
		ninja.put()
		
		
		b = levr.Business.all(keys_only=True).get()
		
		
#		params = {
#					'uid'				: enc.encrypt_key(c.key()),
#					'business'			: enc.encrypt_key(str(b)),
#					'deal_description'	: 'description!!!',
#					'deal_line1'		: 'DEAL LINE!',
#					'img_key'			: img_key
#					}
		params = {
					'uid'				: enc.encrypt_key(c.key()),
					'business'			: enc.encrypt_key(str(b)),
					'business_name'		: 'Alamos',
					'geo_point'			: '42.2,-71.2',
					'vicinity'			: '10 Buick St',
					'types'				: 'aaa,type_o_negative',
					'deal_description'	: 'description!!!',
					'deal_line1'		: 'DEAL LINE!',
					'img_key'			: img_key
					}
		
		(share_url,dealID) = levr_utils.dealCreate(params,'phone_existing_business')
		logging.debug(share_url)
		logging.debug(dealID)
		
		
#		#new business
##		b = levr.Business(key='agtkZXZ-Z2V0bGV2cnIOCxIIQnVzaW5lc3MYBAw')
#		b = levr.Business()
#		b.email 		= 'alonso@getlevr.com'
#		b.pw 			= enc.encrypt_password('alonso')
#		b.business_name = 'Shaws'
#		b.vicinity		= '260 Everett St East Boston, MA'
#		b.alias 		= 'Joe'
#		b.contact_phone = '603-603-6003'
#		b.geo_point		= levr.geo_converter("15.23213,60.2342")
#		b.types			= ['tag1','tag2']
#		b.put()


#		#new deal
#		d = levr.Deal(parent=b)
#		d.img				= upload.key()
#		d.businessID		= str(b)
#		d.business_name 	= 'Shaws'
#		d.secondary_name	= 'second name'
#		d.deal_text			= '50% off booze'
#		d.deal_type			= 'bundle'
#		d.description 		= 'describe me, hun.'
#		d.img_path 			= './img/bobs-discount-furniture.png'
#		d.city 				= 'Qatar'
#		d.deal_status		= 'active'
#		d.vicinity			= '7 Gardner Terrace, Allston, MA'
#		d.tags				= ['alonso','pat','ethan']
#		d.deal_status		= 'pending'
#		d.rank				= 5
#		
#		#create the share ID - based on milliseconds since epoch
#		milliseconds = int(levr_utils.unix_time_millis(datetime.now()))
#		#make it smaller so we get ids with 5 chars, not 6
#		shortened_milliseconds = milliseconds % 100000000
#		unique_id = converter.dehydrate(shortened_milliseconds)
#		d.share_id = unique_id
#		d.put()
#
#		#new customer deal
#		cd = levr.CustomerDeal(parent=ninja)
#		cd.businessID		= str(b)
#		cd.img				= upload.key()
#		cd.business_name 	= 'Shaws'
#		cd.deal_text		= '40% of sijo'
#		cd.deal_type		= 'single'
#		cd.description 		= 'describe me, hun.'
#		cd.rating 			= 50
#		cd.count_end 		= 101
#		cd.count_redeemed 	= 0
#		cd.count_seen 		= 43
#		cd.new_redeem_count	= 0
#		cd.deal_status		= 'pending'
#		cd.geo_point		= levr.geo_converter('-80.,70.')
#		cd.vicinity			= '1234 Cherry Lane, Boston, MA 02134, USA'
#		cd.tags				= ['alonso','pat','ethan']
#		cd.rank				= 10
#		#create the share ID - based on milliseconds since epoch
#		milliseconds = int(levr_utils.unix_time_millis(datetime.now()))
#		#make it smaller so we get ids with 5 chars, not 6
#		shortened_milliseconds = milliseconds % 100000000
#		unique_id = converter.dehydrate(shortened_milliseconds)
#		cd.share_id = unique_id
#		
#		cd.put()


		self.response.headers['Content-Type'] = 'text/plain'
#		self.response.out.write('/phone/img?dealID='+enc.encrypt_key(str(c.key()))+"&size=dealDetail")
		self.response.out.write('     I think this means it was a success')
#		self.redirect('/phone/img?dealID='+str(cd.key())+"&size=dealDetail")
		
#class UpdateUsersHandler(webapp2.RequestHandler):
#	def get(self):
#		#query
#		users = levr.Customer.all().fetch(None)
#			
#			
#		for user in users:
#			#generate random number to decide what split test group they are in
#			choice = randint(10,1000)
#			decision = choice%2
#			if decision == 1:
#				group = 'paid'
#			else:
#				group = 'unpaid'
#			logging.debug(levr_utils.log_model_props(user))
#			user.group = group
#			logging.debug(levr_utils.log_model_props(user))
#			
#		db.put(users)
class StoreGeohashHandler(webapp2.RequestHandler):
	def get(self):
		#pull all of the businesses
		#grab each of their geo_points
		#has geo_points into geo_hash
		#store geo_hash
		business_keys	= levr.Deal.all(keys_only=True).fetch(None)
		businesses		= levr.Deal.get(business_keys)
		for b in businesses:
			geo_point	= b.geo_point
			logging.debug(geo_point)
			geo_hash	= geohash.encode(geo_point.lat,geo_point.lon)
			logging.debug(geo_hash)
			b.geo_hash	= geo_hash
#			
		db.put(businesses)
			
@staticmethod
def get_by_geo_box(bot_left,bot_right):
	
	hash_min = geohash.encode(bot_left.lat,bot_left.lon,precision=10)
	hash_max = geohash.encode(top_right.lat,top_right.lon,precision=10)
	
	businesses = levr.Business.all().filter('geo_hash >=',hash_min).filter('geo_hash <=',hash_max).fetch(None)
	logging.debug(businesses.__len__())
	return businesses
	

class FilterGeohashHandler(webapp2.RequestHandler):
	def get(self):
		#take in geo_point
		#set radius, expand, get all deals
		
		
		
		request_point = levr.geo_converter('42.35,-71.110')
		center_hash = geohash.encode(request_point.lat,request_point.lon,precision=6)
		all_squares = geohash.expand(center_hash)
		
		all = levr.Business.all().count()
		self.response.out.write(all)
		self.response.out.write('<br/>')
		
		keys = []
		for query_hash in all_squares:
			q = levr.Business.all(keys_only=True).filter('geo_hash >=',query_hash).filter('geo_hash <=',query_hash+"{")
			keys.extend(q.fetch(None))
		
		self.response.out.write(str(keys.__len__())+"<br/>")
		
		#get all deals
		deals = levr.Business.get(keys)
		logging.debug(deals)
		for deal in deals:
			self.response.out.write(deal.geo_hash+"<br/>")
		
		
		
		
#		businesses = get_by_geo_box(bot_left, bot_right)
#		
#		
#		hash_min = geohash.encode(bot_left_lat,bot_left_lon)
#		hash_max = geohash.encode(top_right_lat,top_right_lon)
#		
#		
#		self.response.out.write(hash_min+", "+hash_max+"<br/>")
#		
##		length_degrees = .1
#		
#		self.response.out.write(levr.Business.all().count())
#		self.response.out.write('<br/>')
#		
#		q = levr.Business.all().filter('geo_hash >=',hash_min).filter('geo_hash <=', hash_max)
#		self.response.out.write(q.count())
#		self.response.out.write("<br/>")
#		businesses = q.fetch(None)
#		for b in businesses:
#			self.response.out.write(str(b.geo_hash)+"<br/>")
		
#		self.response.out.write(str(levr.Business.all().count())+"<br/>")
#		geo_hash = geohash.encode(lat,lon)
#		
#		all_squares = geohash.expand(geo_hash)
#		
#		self.response.out.write(geo_hash+"<br/>")
#		
#		self.response.out.write(all_squares)
#		self.response.out.write("<br/>")
#		businesses = []
#		count = 0
#		for query_hash in all_squares:
#			q = levr.Business.all().filter('geo_hash >=',query_hash).filter('geo_hash <=',query_hash+"{")
#			c = q.count()
#			self.response.out.write(str(c)+"<br/>")
#			count += c
#			bs = q.fetch(None)
#			
#			businesses.extend(bs)
#		self.response.out.write(str(count)+"<br/>")
#		for b in businesses:
#			self.response.out.write(b.geo_hash+"<br/>")
#			self.response.out.write(str(geohash.decode(b.geo_hash))+"<br/>")
			
			
			
			
#		query = levr.Business.all().filter('geo_hash >=',geo_hash).filter('geo_hash <=', geo_hash+"{")
#		count = query.count()
#		self.response.out.write(count)
#		self.response.out.write('<br/>')
#		businesses = query.fetch(None)
#		for b in businesses:
#			self.response.out.write(b.geo_hash)
#			self.response.out.write('<br/>')
		

class FixTagHandler(webapp2.RequestHandler):
	@staticmethod
	def get():
		#get all deals
		deals = levr.Deal.all().fetch(None)
		
		#tags are from business_name, deal_text, description
		#no longer using secondary name
		for deal in deals:
			tags = []
			business_name = levr.tagger(deal.business_name)
			tags.extend(business_name)
			deal_text = levr.tagger(deal.deal_text)
			tags.extend(deal_text)
			description = levr.tagger(deal.description)
			tags.extend(description)
			logging.debug(tags)
			deal.tags = tags
		
		db.put(deals)

class TestHandler(webapp2.RequestHandler):
    def get(self,a):
        self.response.headers['Content-Type'] = 'text/plain'
#        self.response.out.write(self.request.path)
        self.response.out.write(str(a))

#application = webapp.WSGIApplication(
#                                     [('/', MainPage)],
#                                     debug=True)

#application = webapp.WSGIApplication([
#                                    (r'/myapp/(?P<url>\d{4})/$', MainPage)
#                                    ],
#                                     debug=True)

app = webapp2.WSGIApplication([('/new', MainPage),
								('/new/upload.*', DatabaseUploadHandler),
								('/new/geohash', StoreGeohashHandler),
								('/new/find', FilterGeohashHandler),
								('/new/fixTags', FixTagHandler),
								(r'/new/test/(.*)/a', TestHandler)
#								('/new/update' , UpdateUsersHandler)
								],debug=True)


