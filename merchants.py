import webapp2
import jinja2
import os
import levr_utils
import logging
import levr_classes as levr

from gaesessions import get_current_session

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class merchantsLanding(webapp2.RequestHandler):
	def get(self):
		#Get headers if user isn't logged in
		headerData = levr_utils.loginCheck(self,False)
		logging.info(headerData)
		template_values = {
			'headerData' : headerData,
			'title' : 'Welcome'
		}
		
		template = jinja_environment.get_template('templates/header.html')
		self.response.out.write(template.render(template_values))

class manage(webapp2.RequestHandler):
	def get(self):
		#Bounce if user is not logged in
		headerData = levr_utils.loginCheck(self,True)
		
		template_values = {
			'headerData' : headerData,
			'title' : 'Manage'
		}

		template = jinja_environment.get_template('templates/header.html')
		self.response.out.write(template.render(template_values))

class new_deal(webapp2.RequestHandler):
	def get(self):
		#Don't bounce if user is not logged in
		headerData = levr_utils.loginCheck(self,False)
		
		template_values = {
			'headerData' : headerData,
			'title' : 'New Deal'
		}
		
		if headerData['loggedIn'] == True:
			template = jinja_environment.get_template('templates/new_deal_existing_user.html')
			self.response.out.write(template.render(template_values))
		else:
			template = jinja_environment.get_template('templates/new_deal_new_user.html')
			self.response.out.write(template.render(template_values))
		
		
	
	def post(self):
		#grab the form data
		formdata = self.request.body
		logging.info(formdata)
		
		
		#create a new deal object (but don't store yet…)
		#this will be the same for both new and existing users
		deal = levr.Deal()
		#map request parameters to deal object parameters
		deal.secondary_name			= 
		deal.secondary_is_category 	= 
		deal.description 			=
		deal.deal_type				=
		deal.deal_value				=
		#(deal_rating)
		deal.deal_origin			=
		deal.count_max				=
		deal.city					=
		
		
		#get session, check loginstate
		session = get_current_session()
		
		if session.has_key('loggedIn') == False or session['loggedIn'] == False:
			#not logged in, create new business
			business = levr.Business()
			#map request parameters to business object
			business.email 			=
			business.pw				=
			business.business_name	=
			business.address_line1	=
			business.address_line2	=
			business.city			=
			business.state			=
			business.zip_code		=
			business.contact_owner	=
			business.contact_phone	=
			
			#check that email is available
			q = business.gql("WHERE email = :email",email=email)
			#if exists, write error page and exit
			for result in q:
				template = jinja_environment.get_template('templates/error.html')
				template_values = {}
				self.response.out.write(template.render(template_values))
				sys.exit()
			
			#create business
			business.put()
			
			#add business properties to deal
			#add businessID, businessName to deal
			deal.businessID = business.key().__str__()
			deal.business_name = business.business_name
				
			
		elif session.has_key('loggedIn') == True or session['loggedIn'] == True:
			#logged in, grab current business info
			
		#put deal into database
		deal.put()
		
		#put 
		
		#businessID
		#businessName
		
		
class edit_deal(webapp2.RequestHandler):
	def get(self):
		#Bounce if user is not logged in
		headerData = levr_utils.loginCheck(self,True)
		
		template_values = {
			'headerData' : headerData,
			'title' : 'Edit Deal'
		}
		
		template = jinja_environment.get_template('templates/header.html')
		self.response.out.write(template.render(template_values))
class account(webapp2.RequestHandler):
	def get(self):
		#Bounce if user is not logged in
		headerData = levr_utils.loginCheck(self,True)
		
		template_values = {
			'headerData' : headerData,
			'title' : 'Account'
		}
		
		template = jinja_environment.get_template('templates/header.html')
		self.response.out.write(template.render(template_values))
class manage(webapp2.RequestHandler):
	def get(self):
		##get logged in state
		headerData	= levr_utils.loginCheck(self,True)
		##get deal values from database for the logged in merchant
		businessID	= headerData['businessID']
		
		####### DEAL INFORMATION ######
		q = levr.Deal.gql("WHERE businessID=:1",businessID)
		##will have list of deal dictionaries
		deals = []
		##for each deal:
		for d in q:
			##grab the primary categories
			q2 = levr.Category.gql("WHERE dealID=:1",d.dealID)
			##list of primary categories for that deal
			prim_stack = []
			for p in q2:
				prim_stack.append(p.primary_cat)
			
			##create deal dict that has all the info needed to populate table
			deals.append({
				'dealID'		: d.dealID,
				'secondary_name': d.secondary_name,
				'description'	: d.description,
				'deal_type'		: d.deal_type,
				'deal_value'	: d.deal_value,
				'count_max'		: d.count_max,
				'count_redeemed': d.count_redeemed,
				'img_path'		: d.img_path,
				'primary_cats'	: prim_stack
				})
		######### BUSINESS INFORMATION ##########
		b = levr.Business.get_by_key_name(businessID)
		business_info = {
			
			}
		
		
		
		################Create template dictionary
		template_values = {
			'deals'	: deals,
			'headerData'	: headerData,
			'title'			: 'Manage'
			}
		##create view and send values to template
		template = jinja_environment.get_template('templates/manage.html')
		self.response.out.write(template.render(template_values))
app = webapp2.WSGIApplication([('/merchants', merchantsLanding), ('/merchants/manage',manage), ('/merchants/deal/new', new_deal), ('/merchants/deal/edit', edit_deal), ('/merchants/account',account)],debug=True)
