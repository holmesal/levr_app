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
			template = jinja_environment.get_template('templates/form_new_deal_existing_account.html')
			self.response.out.write(template.render(template_values))
		else:
			template = jinja_environment.get_template('templates/form_new_deal_new_account.html')
			self.response.out.write(template.render(template_values))
		
		
	
	def post(self):
		#grab the form data
		formdata = self.request.body
		logging.info(formdata)
		
		######### GRAB CURRENT MERCHANT OR CREATE NEW ##########
		#get session, check loginstate
		session = get_current_session()
		
		#Check login state
		if session.has_key('loggedIn') == False or session['loggedIn'] == False:
			#not logged in, create new business
			business = levr.Business() #no parent, business is root entity
			#map request parameters to business object
			business.email 			= self.request.get('email')
			business.pw				= self.request.get('password')
			business.business_name	= self.request.get('businessName')
			business.address_line1	= self.request.get('address1')
			business.address_line2	= self.request.get('address2')
			business.city			= self.request.get('city')
			business.state			= self.request.get('state')
			business.zip_code		= self.request.get('zipCode')
			business.alias	= self.request.get('ownerName')
			business.contact_phone	= self.request.get('phone')
			
			
			#check that email is available
			q = business.gql("WHERE email = :1",business.email)
			#if email exists, write error page and exit
			for result in q:
				logging.info('duplicate email in use')
				template = jinja_environment.get_template('templates/error.html')
				template_values = {}
				self.response.out.write(template.render(template_values))
				sys.exit()
			
			#create business
			business.put()
			
			#log in the newly created business account
			session['businessID'] = business.key()
			session['alias'] = business.alias
			session['loggedIn'] = True
			logging.info(session)
			
		elif session.has_key('loggedIn') == True and session['loggedIn'] == True:
			#logged in, grab current business info
			business = session['businessID']
		#!! end of if. the rest of the code operates independent of login state
		
		####### BUSINESS HAS EITHER BEEN CREATED OR EXISTING BUSINESS KEY IS GRABBED
		#create new deal that is child of the business		
		deal = levr.Deal(parent=business)
		
		#Grab form data and apply to new deal object
		#deal.name_type		= self.request.get('nameType')
		### overwrite values until form has changed
		deal.name_type = 'itemName'
		deal.discount_type	= self.request.get('discountType')
		deal.deal_origin	= 'internal'
		deal.count_end		= int(self.request.get('endValue'))
		deal.city			= self.request.get('dealCity')
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
		
		#put deal in database and key is created
		deal.put()
		############ DEAL HAS BEEN CREATED, CREATE PRIMARY CATS AS CHILDREN OF DEAL
		#for now, put request tags into list
		#prim_stack will turn into a list of variable length
		prim_stack = [self.request.get('dealTag1'),self.request.get('dealTag2'),self.request.get('dealTag3')]
		#create each primary_cat as a child of the deal that was just created
		for tag in prim_stack:
			category = levr.Category(parent=deal)
			category.primary_cat = tag
			category.put()
		
		#redirect to manage
		self.redirect('/merchants/manage')
		
class edit_deal(webapp2.RequestHandler):
	def get(self):
		#Bounce if user is not logged in
		headerData = levr_utils.loginCheck(self,True)
		
		#grab deal key
		deal_key = self.request.get('id')
		self.response.out.write(deal_key)
		
		#get the deal information from the key
		deal = db.get(deal_key)
		
		#grab categories for deal
		primary_cats = levr.Category.gql("WHERE ANCESTOR IS :1",deal_key)
		
		logging.info(deal)
		#set form variables from deal
		template_values = levr.web_edit_deal_format(deal)
		#add form variables not handled by format function
		template_values.update({
			'headerData' : headerData,
			'title' : 'Edit Deal'
		})
		self.response.out.write(template_values)
		#create template, render, and push to browser
#		template = jinja_environment.get_template('templates/header.html')
#		self.response.out.write(template.render(template_values))
		
class account(webapp2.RequestHandler):
	def get(self):
		#Bounce if user is not logged in
		headerData = levr_utils.loginCheck(self,True)
		
		#get business info
		business = db.get(headerData['businessID'])
		#business = db.fetch(business)
		logging.info(business)
		#dictionary-ize business info
		template_values = levr.web_edit_account_format(business)
		#put business info into form template
		template_values['headerData']	= headerData
		template_values['title']		= 'Account'
		
		self.response.out.write(template_values)
		template = jinja_environment.get_template('templates/form_edit_account.html')
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
		b.alias			= form('ownerName')
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
		#grab all of the deals
		q = levr.Deal.gql("WHERE ANCESTOR IS :1",headerData['businessID'])
#		q = levr.Deal.gql("WHERE businessID=:1",headerData['businessID'])
		
		##will have list of deal dictionaries
		deals = []
		##for each deal:
		for d in q:
			##grab the primary categories
			q2 = levr.Category.gql("WHERE ANCESTOR IS :1",d.key())
#			q2 = levr.Category.gql("WHERE dealID=:1",d.dealID)
			##list of primary categories for that deal
			prim_stack = []
			for p in q2:
				prim_stack.append(p.primary_cat)
			
			##create deal dict that has all the info needed to populate table
			deals.append({
				'dealID'		: d.key(),
				'secondary_name': d.secondary_name,
				'description'	: d.description,
				'discount_type'	: d.discount_type,
				'discount_value': d.discount_value,
				'count_end'		: d.count_end,
				'count_redeemed': d.count_redeemed,
				'img_path'		: d.img_path,
				'primary_cats'	: prim_stack
				})
		######### BUSINESS INFORMATION ##########
		business = levr.Business.get(headerData['businessID'])
		business_info = levr.web_edit_account_format(business)
		
		################Create template dictionary
		template_values = {
			'deals'			: deals,
			'headerData'	: headerData,
			'title'			: 'Manage',
			'business'		: business_info
			}
		self.response.out.write(template_values)
		##create view and send values to template
		template = jinja_environment.get_template('templates/manage.html')
		self.response.out.write(template.render(template_values))
app = webapp2.WSGIApplication([('/merchants', merchantsLanding),
								('/merchants/manage',manage),
								('/merchants/deal/new', new_deal),
								('/merchants/deal/edit', edit_deal),
								('/merchants/account',account)],
								debug=True)
