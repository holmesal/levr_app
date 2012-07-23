import webapp2
import levr_classes
import logging
#from google.appengine.ext import db
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

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
#		upload = self.get_uploads()[0]
		upload = self.request.get('img')
		upload = blobstore.Blob(upload)
		logging.info(upload)
		

    	# new customer
        c = levr_classes.Customer(key='agtkZXZ-Z2V0bGV2cnIPCxIIQ3VzdG9tZXIYtQIM')
        c.alias	= 'alonso'
        c.email	= 'ethan@getlevr.com'
        c.payment_email = c.email
        c.pw 	= 'ethan'
        c.money_earned = 0.0
        c.money_paid = 0.0
        c.put()
        
        #new ninja
        ninja = levr_classes.Customer(key='agtkZXZ-Z2V0bGV2cnIOCxIIQ3VzdG9tZXIYAQw')
        ninja.alias	= 'ninja'
        ninja.email	= 'santa@getlevr.com'
        ninja.payment_email = c.email
        ninja.pw 	= 'ethan'
        ninja.money_earned = 0.0
        ninja.money_paid = 0.0
        ninja.put()
        



		#new business
		b = levr_classes.Business(key='agtkZXZ-Z2V0bGV2cnIOCxIIQnVzaW5lc3MYBAw')
		b.email 		= 'alonso@getlevr.com'
		b.pw 			= 'alonso'
		b.business_name = 'Shaws'
		b.address_line1 = '1 white house road'
		b.address_line2 = 'box 10'
		b.city 			= 'washington'
		b.state 		= 'DC'
		b.zip_code 		= '10000'
		b.alias 		= 'Joe'
		b.contact_phone = '603-603-6003'
		b.geo_point		= levr_classes.geo_converter("15.23213,60.2342")
		b.put()


		#new deal
		d = levr_classes.Deal(parent=b)
		d.img				= upload.key()
		d.businessID		= str(b.key())
		d.business_name 	= 'Shaws'
		d.secondary_name	= 'second name'
		d.deal_type			= 'single'
		d.deal_item			= 'Coat'
		d.description 		= 'describe me, hun.'
		d.discount_type 	= 'monetary'
		d.discount_value 	= 50.2
		d.rating 			= 50
		d.count_end 		= 101
		d.count_redeemed 	= 0
		d.count_seen 		= 43
		d.img_path 			= './img/bobs-discount-furniture.png'
		d.city 				= 'Qatar'
		d.deal_status		= 'active'
		d.address_string	= '7 Gardner Terrace, Apt 1, Allston, MA 02134, USA'
		d.put()

		#new customer deal
		cd = levr_classes.CustomerDeal(parent=ninja)
		cd.img				= upload.key()
        cd.businessID		= str(b.key())
		cd.business_name 	= 'Shaws'
		cd.deal_item 		= 'socks'
		cd.name_type		= 'specific'
		cd.description 		= 'describe me, hun.'
		cd.discount_type 	= 'monetary'
		cd.discount_value 	= 50.2
		cd.rating 			= 50
		cd.count_end 		= 101
		cd.count_redeemed 	= 0
		cd.count_seen 		= 43
		cd.new_redeem_count	= 0
		cd.img_path 		= './img/bobs-discount-furniture.png'
		cd.city 			= 'Qatar'
		cd.deal_status		= 'active'
		cd.geo_point		= levr_classes.geo_converter('-80.,70.')
		cd.address_string	= '1234 Cherry Lane, Boston, MA 02134, USA'
		cd.put()


		#new Category
		cat = levr_classes.Category(parent=d)
		cat.primary_cat 	= 'Socks'
		cat.deal_status		= 'active'
		cat.put()

		#new favorite
		f = levr_classes.Favorite(parent=c)
#       f.uid				= str(c.key())
		f.dealID			= str(d.key())
		f.primary_cat	 	= 'Shoes'
		f.put()

		self.response.headers['Content-Type'] = 'text/plain'
		self.response.out.write('/phone/img?dealID='+str(cd.key())+"&size=dealDetail")
		self.response.out.write('     I think this means it was a success')
		self.redirect('/phone/img?dealID='+str(cd.key())+"&size=dealDetail")
		

app = webapp2.WSGIApplication([('/new', MainPage),
								('/new/upload', DatabaseUploadHandler)
								],debug=True)

