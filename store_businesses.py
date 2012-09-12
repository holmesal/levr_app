import levr_classes as levr
import webapp2
import logging
import levr_utils
from datetime import datetime
from datetime import timedelta
class StoreBusinessesHandler(webapp2.RequestHandler):
	def get(self):
		self.response.out.write('Do not go to this address. ')
#		############################################
#		#FOR DELETING BUSINESSES##
#		time = datetime.now() + timedelta(minutes=-100)
#		logging.debug(time)
#		b = levr.Business.all().filter('date_created >',time).fetch(None)
#		
#		logging.debug(b.__len__())
#		bb = levr.Business.all().fetch(None)
#		logging.debug(bb.__len__())
#		for bus in b:
#			bus.delete()
#			logging.debug(levr_utils.log_model_props(bus, ['business_name','date_created']))
#			
#		
#		##########################################
#		#open file with all businesses
#		f	= open('businesses-other.txt','r')
#		
#		#read whole text file
#		conglomerate	= f.read()
#		logging.debug(conglomerate)
#		#split into business entries
#		businesses_list	= conglomerate.split('\n')
#		
#		
#		logging.debug(businesses_list)
#		#perform on each business entry
#		name_lengths = []
#		for b in businesses_list:
#			if b.__len__() >2:
#				#split entry
#				business	= b.split('\t')
#				logging.debug(business)
#				#grab data from entry
#				name		= business[0]
#				name_lengths.append(name.__len__())
#				vicinity	= business[1]
#				geo_point	= levr.geo_converter(business[2])
#				types		= business[3].split(',')
#				
#				#store as entity
#				b	= levr.Business()
#				b.business_name	= name
#				b.vicinity		= vicinity
#				b.geo_point		= geo_point
#				b.types			= types
#				b.targeted		= True
#				b.put()
#				
#				#confirm storage
#				self.response.out.write(name+" "+vicinity+"<br />")
#		self.response.out.write(max(name_lengths))
#		self.response.out.write(sorted(name_lengths))
app = webapp2.WSGIApplication([('/target', StoreBusinessesHandler)
								], debug=True)