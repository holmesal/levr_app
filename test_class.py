#from __future__ import with_statement
#from google.appengine.api import files
import webapp2
import levr_classes
import logging
import levr_encrypt as enc
import levr_utils
import base_62_converter as converter
#from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers
from datetime import datetime

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
		logging.info(upload)
		
		# new customer
#		c = levr_classes.Customer(key='agtkZXZ-Z2V0bGV2cnIOCxIIQ3VzdG9tZXIYEgw')
		c = levr_classes.Customer()
		c.email	= 'ethan@getlevr.com'
		c.payment_email = c.email
		c.pw 	= enc.encrypt_password('ethan')
		c.alias	= 'alonso'
		c.favorites	= []
		c.put()
		
		#new ninja
#		ninja = levr_classes.Customer(key='agtkZXZ-Z2V0bGV2cnIOCxIIQ3VzdG9tZXIYCww')
		ninja = levr_classes.Customer()
		ninja.email	= 'santa@getlevr.com'
		ninja.payment_email = c.email
		ninja.pw 	= enc.encrypt_password('ethan')
		ninja.alias	= 'ninja'
		ninja.favorites = []
		ninja.put()
		
		

		#new business
#		b = levr_classes.Business(key='agtkZXZ-Z2V0bGV2cnIOCxIIQnVzaW5lc3MYBAw')
		b = levr_classes.Business()
		b.email 		= 'alonso@getlevr.com'
		b.pw 			= enc.encrypt_password('alonso')
		b.business_name = 'Shaws'
		b.vicinity		= '260 Everett St East Boston, MA'
		b.alias 		= 'Joe'
		b.contact_phone = '603-603-6003'
		b.geo_point		= levr_classes.geo_converter("15.23213,60.2342")
		b.types			= ['tag1','tag2']
		b.put()


		#new deal
		d = levr_classes.Deal(parent=b)
		d.img				= upload.key()
		d.businessID		= str(b.key())
		d.business_name 	= 'Shaws'
		d.secondary_name	= 'second name'
		d.deal_text			= '50% off booze'
		d.deal_type			= 'bundle'
		d.description 		= 'describe me, hun.'
		d.rating 			= 50
		d.count_end 		= 101
		d.count_redeemed 	= 0
		d.count_seen 		= 43
		d.img_path 			= './img/bobs-discount-furniture.png'
		d.city 				= 'Qatar'
		d.deal_status		= 'active'
		d.vicinity			= '7 Gardner Terrace, Allston, MA'
		d.tags				= ['alonso','pat','ethan']
		d.deal_status		= 'pending'
		d.rank				= 5
		
		#create the share ID - based on milliseconds since epoch
		milliseconds = int(levr_utils.unix_time_millis(datetime.now()))
		#make it smaller so we get ids with 5 chars, not 6
		shortened_milliseconds = milliseconds % 100000000
		unique_id = converter.dehydrate(shortened_milliseconds)
		d.share_id = unique_id
		d.put()

		#new customer deal
		cd = levr_classes.CustomerDeal(parent=ninja)
		cd.businessID		= 'ahNkZXZ-bGV2ci1wcm9kdWN0aW9uchMLEg1CdXNpbmVzc093bmVyGAEM'#str(b.key())
		cd.img				= upload.key()
		cd.business_name 	= 'Shaws'
		cd.deal_text		= '40% of sijo'
		cd.deal_type		= 'single'
		cd.description 		= 'describe me, hun.'
		cd.rating 			= 50
		cd.count_end 		= 101
		cd.count_redeemed 	= 0
		cd.count_seen 		= 43
		cd.new_redeem_count	= 0
		cd.deal_status		= 'pending'
		cd.geo_point		= levr_classes.geo_converter('-80.,70.')
		cd.vicinity			= '1234 Cherry Lane, Boston, MA 02134, USA'
		cd.tags				= ['alonso','pat','ethan']
		cd.rank				= 10
		#create the share ID - based on milliseconds since epoch
		milliseconds = int(levr_utils.unix_time_millis(datetime.now()))
		#make it smaller so we get ids with 5 chars, not 6
		shortened_milliseconds = milliseconds % 100000000
		unique_id = converter.dehydrate(shortened_milliseconds)
		cd.share_id = unique_id
		
		cd.put()


		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write('/phone/img?dealID='+enc.encrypt_key(str(cd.key()))+"&size=dealDetail")
		self.response.out.write('     I think this means it was a success')
#		self.redirect('/phone/img?dealID='+str(cd.key())+"&size=dealDetail")
		

app = webapp2.WSGIApplication([('/new', MainPage),
								('/new/upload.*', DatabaseUploadHandler)
								],debug=True)


