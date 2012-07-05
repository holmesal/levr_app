import webapp2
import levr_classes
from google.appengine.api import users
from levr_classes import db

class MainPage(webapp2.RequestHandler):
    def get(self):
    	# new customer
        c = levr_classes.Customer(key_name='2111111111111')
        c.name='alonso'
        c.put()
        
    	#new business
        b = levr_classes.Business(key_name='3222222222222')
        b.business_name = 'Shaws'
        b.address_line1 = '1 white house road'
        b.address_line2 = 'box 10'
        b.city 			= 'washington'
        b.state 		= 'DC'
        b.zip_code 		= '10000'
        b.contact_owner = 'Joe'
        b.contact_email = 'Joe@thebuilder.com'
        b.contact_phone = '603-603-6003'
        b.put()
        
    	#new deal
        d = levr_classes.Deal(key_name='2333333333333')
        d.dealID			= '2333333333333'
        d.businessID 		= '3222222222222'
        d.business_name 	= 'Shaws'
        d.secondary_name 	= 'jeggings'
        d.secondary_is_category = False
        d.description 		= 'describe me, hun.'
        d.deal_type 		= 'monetary'
        d.deal_value 		= 50.2
        d.rating 			= 50
        d.count_max 		= 101
        d.count_redeemed 	= 42
        d.count_seen 		= 43
        d.img_path 			= './img/bobs-discount-furniture.png'
        d.city 				= 'Qatar'
        d.put()

        #new Category
        cat = levr_classes.Category()
        cat.primary_cat 	= 'Socks'
        cat.dealID			= '2333333333333'
        #cat.put()
        
        #new favorite
        f = levr_classes.Favorite()
        f.uid				= '2111111111111'
        f.dealID			= '2333333333333'
        f.primary_cat	 	= 'Toe Socks'
        f.put()

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('I think this means it was a success')

app = webapp2.WSGIApplication([('/new', MainPage)],
                              debug=True)

