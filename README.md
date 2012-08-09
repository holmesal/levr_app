levr_app to launchable state:
========

Things to do:

Turn off ability to redeem a deal more than once - this is only there for our testing ability
	This lives in two places - one in redeem, and one in checkRedeem
	
hook up barcode url (spoofed right now) to actually point at a barcode

flurry including logging search queries
Landing page - sketch out phone shots
aesthetics
terms of service
Privacyy policy!
barcode for redeem screen
log last login



email updates for pending deals
later...
start thinking about async methods
lower-casify each search

post-launchable state:
=======
restart merchants page
	very very very slim feature set
embeddable widget
auto remove deal from favorite post redeeem?



ISSUES
=======
DINC - upload URL is generated but not sent


APP AESTHETICS
=======
Browse button should search for an empty string or something - return isEmpty=true screen
make the height of the "related items" cell the same height as the header cell, and change the text to: "popular"
hide the header cell if isempty=True
business name should be bold face
change "Add" text to "Favorite"
Change homescreen add deal camera icon
change add deal textboxes
First page aesthetics


Analytics - App
===============

What we want to measure
-----------------------
number of redemptions per search query/deal
number of addfavs per query/deal
redemptions/addfavs per business/deal
redemptions/addfavs per user

frequency of sessions/favorite/redemption per user


funnels
-------
home > search/browse + query > deal > redeem/addfav
favorite > deal screen > delete/redeem
home > add deal > take picture > upload deal

