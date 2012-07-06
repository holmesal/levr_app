import webapp2
import jinja2
import os
import levr_utils
import logging

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

app = webapp2.WSGIApplication([('/merchants', merchantsLanding), ('/merchants/manage',manage), ('/merchants/deal/new', new_deal), ('/merchants/deal/edit', edit_deal), ('/merchants/account',account)],debug=True)