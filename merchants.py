import webapp2
import jinja2
import os

jinja_environment = jinja2.Environment(loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))
    
class merchantsLanding(webapp2.RequestHandler):
	def get(self):
		template = jinja_environment.get_template('templates/merchantsLanding.html')
		self.response.out.write(template.render())

class manage(webapp2.RequestHandler):
	def get(self):
		
		template = jinja_environment.get_template('templates/manage.html')
		self.response.out.write(template.render(template_values))

class new_deal(webapp2.RequestHandler):
	def get(self):
		
		template_values = {
			'name' : 'Alonso'
		}
		
		template = jinja_environment.get_template('test.html')
		self.response.out.write(template.render(template_values))
		
class edit_deal(webapp2.RequestHandler):
	def get(self):
		print "This is a request for edit_deal"
		
class account(webapp2.RequestHandler):
	def get(self):
		print "This is a request for account"

app = webapp2.WSGIApplication([('/merchants/', merchantsLanding), ('/merchants/manage',manage), ('/merchants/deal/new', new_deal), ('/merchants/deal/edit', edit_deal), ('/merchants/account',account)],debug=True)