import webapp2
import jinja2
import os

jinja_environment = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class new_deal(webapp2.RequestHandler):
	def get(self):
		
		template_values = {
			'name' : 'Alonso'
		}
		
		template = jinja_environment.get_template('./templates/index.html')
		self.response.out.write(template.render(template_values))
		
class manage(webapp2.RequestHandler):
	def get(self):
		print "This is a request for manage"

app = webapp2.WSGIApplication([('/merchants/deal/new', new_deal), ('/merchants/deal/edit', edit_deal),('/merchants/manage',manage), ('/merchants/account',account)],debug=True)