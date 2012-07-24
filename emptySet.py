import os
import webapp2
import levr_classes as levr
from google.appengine.ext import db
from google.appengine.api import images
import logging


class edit(webapp2.RequestHandler):
	def get(self):
		#launch the jinja environment
		self.response.out.write("""
			<html>
			<body>
			<form action="/phone/uploadDealImage" enctype="multipart/form-data" method="post">
				<div><label>Index (1-10):</label></div>
				<div><input type="text" name="index"></input></div>

				<div><label>Primary Cat:</label></div>
				<div><input type="text" name="primary_cat"></input></div>

				<div><label>Image:</label></div>
				<div><input type="file" name="img"/></div>

				<div><input type="submit" value="Press for beer" /></div>
			</form>
			</body>
			</html>""")
	
	def post(self):
		logging.info(self.request.body)
		#grab form data
		idx			= int(self.request.get('index'))
		primary_cat	= self.request.get('primary_cat')
		image		= self.request.get('img')
		image		= images.resize(image,640,160)
		
		
#		obj				= levr.EmptySetResponse('index',idx)
		obj = levr.EmptySetResponse.all().filter('index',idx).get()
		if not obj:
			obj	= levr.EmptySetResponse()
		obj.primary_cat	= primary_cat
		obj.img			= db.Blob(image)
		obj.index		= idx
		obj.put()
		
		#url = images.get_serving_url(obj.img)
		self.response.headers['Content-Type'] = 'image/png'
		self.response.out.write(obj.img)
		logging.info(self.request.headers)
		logging.info(self.request.body)

app = webapp2.WSGIApplication([('/emptySet/edit', edit)],
								debug=True)
