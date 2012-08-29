import logging#, email
from google.appengine.ext import webapp
from google.appengine.ext.webapp.mail_handlers import InboundMailHandler
#from google.appengine.ext.webapp.util import run_wsgi_app

class LogSenderHandler(InboundMailHandler):
	def receive(self, mail_message):
		logging.debug('YES~!')
		logging.info("Received a message from: " + mail_message.sender)
		logging.debug(mail_message)
		
		# Send a response confirming that we have 
		
app = webapp.WSGIApplication([LogSenderHandler.mapping()], debug=True)