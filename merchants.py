import webapp2
import jinja2
import os
import levr_utils
import logging
import levr_classes as levr

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
		#Bounce if user is not logged in
		headerData = levr_utils.loginCheck(self,True)
		
		template_values = {
			'headerData' : headerData,
			'title' : 'New Deal'
		}
		
		template = jinja_environment.get_template('templates/header.html')
		self.response.out.write(template.render(template_values))
		
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
		q	 		= levr.Deal.gql("WHERE businessID=:1",businessID)
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
		
		##Create template dictionary
		template_values = {
			'deals'	: deals,
			'headerData'	: headerData,
			'title'			: 'Manage'
			}
		##create view and send values to template
		template = jinja_environment.get_template('templates/manage.html')
		self.response.out.write(template.render(template_values))
app = webapp2.WSGIApplication([('/merchants', merchantsLanding), ('/merchants/manage',manage), ('/merchants/deal/new', new_deal), ('/merchants/deal/edit', edit_deal), ('/merchants/account',account)],debug=True)
