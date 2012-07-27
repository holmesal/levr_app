import os
import webapp2
import levr_classes as levr
import levr_encrypt	as enc
import levr_utils
#from google.appengine.ext import db
#from google.appengine.api import images
import logging
import jinja2

#dealtype - bundle or 
#dealitem -

class PopulateHandler(webapp2.RequestHandler):
	def get(self):
		'''Creates a list of deal objects to put plugged into an iframe'''
		try:
			#identify the business who is requesting their deals
			businessID = self.request.get('id')
			logging.debug(businessID+"<br/>")
			businessID = enc.decrypt_key(businessID)
			logging.debug(businessID)
			error = self.request.get('error')
			logging.debug(error)
			success = self.request.get('success')
			logging.debug(success)
			
			#propogate user-entered values
			email_or_owner = self.request.get('email_or_owner')
			email = self.request.get('email')
			username = self.request.get('username')
			
			#check loginstate of user viewing the deal
			headerData = levr_utils.loginCheck(self,False)
			
			#grab the deals for the business
			deals = levr.Deal.gql("WHERE ANCESTOR IS :1", businessID)
			if not deals:
				#business does not have any deals
				self.response.out.write('No deals!')
			else:
				#grab/format the necessary information for each deal
				plugs = [levr.phoneFormat(deal,'plug') for deal in deals]
				template_values = {
					'headerData'	: headerData,
					'title'			: 'Plug',
					'deals'			: plugs,
					'error'			: error,
					'success'		: success,
					'email_or_owner': email_or_owner,
					'email'			: email,
					'username'		: username
				}
				logging.debug(template_values)
			
				jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
				template = jinja_environment.get_template('templates/plug.html')
				self.response.out.write(template.render(template_values))
			
		except:
			levr.log_error()

class ClickHandler(webapp2.RequestHandler):
	def post(self):
		'''Someone has clicked on a deal in the plug'''
		try:
			dealID = self.request.get('id')
			uid = self.request.get('ref')
			logging.debud(uid+" "+dealID)
			# or...
		except:
			levr.log_error()

class ClickResponseHandler(webapp2.RequestHandler):
	def post(self):
		try:
			pass
		except:
			levr.log_error()
app = webapp2.WSGIApplication([('/plug/create', PopulateHandler),
								('/plug/click', ClickHandler)
								], debug=True)
