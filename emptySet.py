#import os
import webapp2
import levr_classes as levr
import levr_encrypt as enc
#from google.appengine.ext import db
#from google.appengine.api import images
import logging
from google.appengine.ext import blobstore
from google.appengine.ext.webapp import blobstore_handlers

class EditEmptySetHandler(webapp2.RequestHandler):
	def get(self):
		upload_url = blobstore.create_upload_url('/emptySet/post')
		logging.debug(upload_url)
		#launch the jinja environment
		self.response.out.write("""
			<html>
			<body>
			<form action="%s" enctype="multipart/form-data" method="post">
				<div><label>Index (1-10):</label></div>
				<div><input type="text" name="index"></input></div>

				<div><label>Primary Cat:</label></div>
				<div><input type="text" name="primary_cat"></input></div>

				<div><label>Image:</label></div>
				<div><input type="file" name="img"/></div>

				<div><input type="submit" value="Press for beer" /></div>
			</form>
			</body>
			</html>""" % upload_url)

class EmptySetUploadHandler(blobstore_handlers.BlobstoreUploadHandler):
	def post(self):
		try:
			logging.debug(self.request.headers)
			logging.debug(self.request.body)
			upload = self.get_uploads()[0]
			logging.debug(upload)
			blob_key = upload.key()
			#grab form data
			idx			= int(self.request.get('index'))
			primary_cat	= self.request.get('primary_cat')
#			image		= self.request.get('img')
#			image		= images.resize(image,640,160)
			
			obj = levr.EmptySetResponse.all().filter('index',idx).get()
###########			need to delete existing blob
			logging.debug(obj)
			if not obj:
				logging.info("NO OBJECT!~")
				#create new emptySetResponse
				obj	= levr.EmptySetResponse()
			else:
				logging.info("FLAG there is object!!!!!")
				#delete old blob
				old_blob	= obj.img
#				logging.debug(old_blob_key)
#				old_blob	= blobstore.BlobInfo.get(old_blob_key)
#				logging.debug(old_blob)
				old_blob.delete()
#				logging.debug(old_blob)
			obj.primary_cat	= primary_cat
			obj.img			= blob_key
			obj.index		= idx
			obj.put()
			
			obj_key = enc.encrypt_key(obj.key())
			logging.debug(obj_key)
			self.redirect('/phone/img?size=fullSize&dealID=%s' % obj_key)
			#url = images.get_serving_url(obj.img)
#			self.response.headers['Content-Type'] = 'image/png'
#			self.response.out.write(obj.img)
#			logging.info(self.request.headers)
#			logging.info(self.request.body)
		except:
			levr.log_error(self.request.body)
app = webapp2.WSGIApplication([('/emptySet/edit', EditEmptySetHandler),
								('/emptySet/post', EmptySetUploadHandler),
								],debug=True)
