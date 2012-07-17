import webapp2
import levr_classes
#import logging
#from google.appengine.ext import db

class MainPage(webapp2.RequestHandler):
    def get(self):
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
        b = levr_classes.Business(key='agtkZXZ-Z2V0bGV2cnIOCxIIQnVzaW5lc3MYNQw')
        b.business_name = 'Shaws'
        b.address_line1 = '1 white house road'
        b.address_line2 = 'box 10'
        b.city 			= 'washington'
        b.state 		= 'DC'
        b.zip_code 		= '10000'
        b.alias = 'Joe'
        b.email 		= 'alonso@getlevr.com'
        b.contact_phone = '603-603-6003'
        b.pw 			= 'alonso'
        b.put()
        
    	#new deal
        d = levr_classes.Deal(parent=b)
        d.business_name 	= 'Shaws'
        d.name_type			= 'specific'
        d.description 		= 'describe me, hun.'
        d.discount_type 	= 'monetary'
        d.discount_value 	= 50.2
        d.rating 			= 50
        d.count_end 		= 101
        d.count_redeemed 	= 42
        d.count_seen 		= 43
        d.img_path 			= './img/bobs-discount-furniture.png'
        d.city 				= 'Qatar'
        d.deal_item			= 'Coat'
        d.deal_status		= 'active'
        d.address_string	= '7 Gardner Terrace, Apt 1, Allston, MA 02134, USA'
        d.put()
        
        #new customer deal
        cd = levr_classes.CustomerDeal(parent=ninja)
        cd.business_name 	= 'Shaws'
        cd.deal_item 		= 'socks'
        cd.name_type		= 'specific'
        cd.description 		= 'describe me, hun.'
        cd.discount_type 	= 'monetary'
        cd.discount_value 	= 50.2
        cd.rating 			= 50
        cd.count_end 		= 101
        cd.count_redeemed 	= 42
        cd.count_seen 		= 43
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
#        f.uid				= str(c.key())
        f.dealID			= str(d.key())
        f.primary_cat	 	= 'Shoes'
        f.put()
        
        

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('I think this means it was a success')

app = webapp2.WSGIApplication([('/new', MainPage)],
                              debug=True)

