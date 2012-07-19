import levr_classes as levr
from datetime import datetime
from google.appengine.ext import db

try:
	now = datetime.now()
	expired = levr.CustomerDeal.gql("WHERE deal_status=:'active' AND date_end <:1",now)
	for x in expired:
		x.deal_status = "expired"
		x.push()
except:
	levr.log_error()
