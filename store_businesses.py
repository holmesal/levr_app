import levr_classes as levr
import webapp2
import logging
class StoreBusinessesHandler(webapp2.RequestHandler):
	def get(self):
		#open file with all businesses
		f	= open('businesses.txt','r')
		
		#read whole text file
		conglomerate	= f.read()
		logging.debug(conglomerate)
		#split into business entries
		businesses_list	= conglomerate.split('\n')
		
		#remove the last line which is empty
		businesses_list.pop()
		
		logging.debug(businesses_list)
		#perform on each business entry
		for b in businesses_list:
			#split entry
			business	= b.split('\t')
			logging.debug(business)
			#grab data from entry
			name		= business[0]
			vicinity	= business[1]
			geo_point	= levr.geo_converter(business[2])
			types		= business[3].split(',')
			
			#store as entity
			b	= levr.Business()
			b.business_name	= name
			b.vicinity		= vicinity
			b.geo_point		= geo_point
			b.types			= types
			b.targeted		= True
			b.put()
			
			#confirm storage
			self.response.out.write(str(b.key())+"<br />")

app = webapp2.WSGIApplication([('/target', StoreBusinessesHandler)
								], debug=True)