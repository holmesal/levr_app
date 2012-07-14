import webapp2
import levr_classes
#import logging
from google.appengine.ext import db

class MainPage(webapp2.RequestHandler):
    def get(self):
    	# new customer
        c = levr_classes.Customer()
        c.name	= 'alonso'
        c.user 	= 'ethan@getlevr.com'
        c.pw 	= 'ethan'
        c.put()
        
    	#new business
        b = levr_classes.Business(key='agtkZXZ-Z2V0bGV2cnIOCxIIQnVzaW5lc3MYHQw')
        b.business_name = 'Shaws'
        b.address_line1 = '1 white house road'
        b.address_line2 = 'box 10'
        b.city 			= 'washington'
        b.state 		= 'DC'
        b.zip_code 		= '10000'
        b.contact_owner = 'Joe'
        b.email 		= 'alonso@getlevr.com'
        b.contact_phone = '603-603-6003'
        b.pw 			= 'alonso'
        b.put()
        
        
    	#new deal
        d = levr_classes.Deal(parent=db.Key('agtkZXZ-Z2V0bGV2cnIOCxIIQnVzaW5lc3MYNQw'))
        #d.businessID 		= b.key()
        d.business_name 	= 'Shaws'
        d.secondary_name 	= 'jeggings'
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
        d.put()
        
        #new Category
        cat = levr_classes.Category(parent=d)
        cat.primary_cat 	= 'Socks'
        #cat.dealID			= d.key()
        cat.put()
        
        #new favorite
        f = levr_classes.Favorite(parent=c)
#        f.uid				= str(c.key())
        f.dealID			= str(d.key())
        f.primary_cat	 	= 'Toe Socks'
        f.put()
#        cust = f.parent()
#        self.response.out.write(cust.children())
        
        q = levr_classes.Deal.gql('WHERE ANCESTOR IS :1','agtkZXZ-Z2V0bGV2cnIOCxIIQnVzaW5lc3MYHQw')
        for result in q:
        	self.response.out.write(result)
        
#        id = 'agtkZXZ-Z2V0bGV2cnIbCxIIQnVzaW5lc3MiDTMyMjIyMjIyMjIyMjIM'
#        result = db.get(id)
#        self.response.out.write(result)

        self.response.headers['Content-Type'] = 'text/plain'
        self.response.out.write('I think this means it was a success')

app = webapp2.WSGIApplication([('/new', MainPage)],
                              debug=True)

