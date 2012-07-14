import os
import webapp2
import levr_classes as levr
from google.appengine.ext import db
from google.appengine.api import images


class image(webapp2.RequestHandler):
	def get(self):
		#grab all the deals with current status == pending
		q = levr.Deal.gql('WHERE status=:status','pending')
		
		#get the first matching entity and parse into template values
		result = q.get()
		template_values = {
			'image'				: result.image,
			'business_name'		: result.business_name
		}
		template = jinja_environment.get_template('templates/admin_pending.html')
		self.response.out.write(template.render(template_values))
		

app = webapp2.WSGIApplication([('/admin/pending', pending)],debug=True)
