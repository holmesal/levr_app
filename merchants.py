import webapp2
import jinja2
import os
import levr_utils
import logging
import levr_classes as levr

from gaesessions import get_current_session
from google.appengine.ext import db

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
		
		logging.info(headerData)
		
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
		
		
		#create a new deal object (but don't store yet)
		#this will be the same for both new and existing users
		deal = levr.Deal()
		#map request parameters to deal object parameters
		
		deal.name_type			 	= self.request.get('nameType')
		deal.discount_type			= self.request.get('discountType')
		#(deal_rating)
		deal.deal_origin			= 'internal'
		deal.count_end				= int(self.request.get('endValue'))
		deal.city					= self.request.get('dealCity')
		
		logging.info(deal.discount_type)
		if deal.discount_type == "free":
			pass
		else:
			deal.discount_value		= float(self.request.get('dealValue'))
		
		if deal.name_type == "itemName":
			deal.secondary_name = self.request.get('specificName')
			deal.description = self.request.get('specificDescription')
		elif deal.name_type == "category":
			deal.secondary_name = self.request.get('categoryTag')
			deal.description = self.request.get('categoryDescription')
		
		
		#get session, check loginstate
		#hello ethan
		session = get_current_session()
		
		if session.has_key('loggedIn') == False or session['loggedIn'] == False:
			#not logged in, create new business
			business = levr.Business()
			#map request parameters to business object
			business.email 			= self.request.get('email')
			business.pw				= self.request.get('password')
			business.business_name	= self.request.get('businessName')
			business.address_line1	= self.request.get('address1')
			business.address_line2	= self.request.get('address2')
			business.city			= self.request.get('city')
			business.state			= self.request.get('state')
			business.zip_code		= self.request.get('zipCode')
			business.contact_owner	= self.request.get('ownerName')
			business.contact_phone	= self.request.get('phone')
			
			
			#check that email is available
			q = business.gql("WHERE email = :email",email=email)
			#if exists, write error page and exit
			for result in q:
				logging.info('duplicate email in use')
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
			
			#insert deal into DB
			deal.put()
			
			#login
			session['businessID'] = business.key()
			session['contact_owner'] = business.contact_owner
			session['loggedIn'] = True
			logging.info(session)
			
		elif session.has_key('loggedIn') == True and session['loggedIn'] == True:
			#logged in, grab current business info
			pass
		

		#get dealID
		dealID = deal.key().__str__()
		
		#put category mappings into db
		#for now, put request tags into list
		prim_stack = [self.request.get('dealTag1'),self.request.get('dealTag2'),self.request.get('dealTag3')]
		#build and store
		for tag in prim_stack:
			category = levr.Category()
			category.dealID = dealID
			category.primary_cat = tag
			category.put()
		
		#redirect to manage
		self.redirect('/merchants/manage')
		
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
		session = get_current_session()
		
		#get business info
		business = db.get(session['businessKey'])
		#business = db.fetch(business)
		logging.info(business)
		logging.info(session)
		#dictionary-ize business info
		template_values = levr.webBusinessFormat(business)
		#put business info into form template
		template_values['headerData']	= headerData
		template_values['title']		= 'Account'
		
		self.response.out.write(session)
		self.response.out.write(template_values)
		template = jinja_environment.get_template('templates/editAccount.html')
		self.response.out.write(template.render(template_values))

	def post(self):
		session = get_current_session()
		formdata = self.request.body
		logging.info(formdata)
		#create instance of the business entity
		b = levr.Business(key=session['businessKey'])
		#alias the request function
		form = self.request.get
		#grab data from form
		b.business_name = form('businessName')
		b.address_line1 = form('address1')
		b.address_line2 = form('address2')
		b.city			= form('city')
		b.state			= form('state')
		b.zip_code		= form('zipCode')
		b.contact_owner	= form('ownerName')
		b.contact_phone	= form('phone')
		b.pw			= form('password')
		b.email			= form('email')
		#insert into database
		b.put()
		#redirect
		self.redirect('/merchants/manage')
        
		
class manage(webapp2.RequestHandler):
	def get(self):
		##get logged in state
		headerData	= levr_utils.loginCheck(self,True)
		##get deal values from database for the logged in merchant
		
		####### DEAL INFORMATION ######
		logging.info(headerData['businessID'])
		q = levr.Deal.gql("WHERE businessID=:1",headerData['businessID'])
		
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
				'discount_type'		: d.discount_type,
				'discount_value'	: d.discount_value,
				'count_end'		: d.count_end,
				'count_redeemed': d.count_redeemed,
				'img_path'		: d.img_path,
				'primary_cats'	: prim_stack
				})
		######### BUSINESS INFORMATION ##########
		b = levr.Business.get(businessID)
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
