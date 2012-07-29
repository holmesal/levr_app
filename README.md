levr_app to launchable state:
========

Things to do:

Turn off ability to redeem a deal more than once - this is only there for our testing ability
	This lives in two places - one in redeem, and one in checkRedeem

flurry including logging search queries
Landing page - sketch out phone shots
aesthetics
terms of service
barcode for redeem screen

<!--Empty set response to blobstore - phone response handler and upload-->
email updates for pending deals
apartment applications

lost password recovery - decrypt and email


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
Search or browse or add deal the first time
search vs browse vs add deal frequency
search queries
frequency of each search query
number of results per query
number of results per browse query
number of redemptions per search query/deal
number of addfavs per query/deal
number of deals viewed in between action (add fav/ redeem)
number of repeat users
number of downloads (know from app store)
number of first time users with favorite - i.e. got there through share
	- should log on web side
number of signups on phone
frequency of being search for each browse category
number of people viewing help screen from inside app
	- what screen they were on
number of favorites/redemptions through browse vs search
number of cashout requests
number of shares for each deal
	- frequency of sharing for newly created deals
location of users
location of redemptions/addfav in relation to location of deal
log uid for each action - native in flurry
uncaught exeptions

redemptions/addfavs per business/deal
redemptions/addfavs per user
frequency of sessions/favorite/redemption per user


funnels
-------
home > search/browse + query > deal > redeem/addfav
favorite > deal screen > delete/redeem
home > add deal > take picture > upload deal



Screen breakdown
----------------
login screen

home screen
- screen: search
	- search query
	- search results
	- selection of deal
	- return to search after viewing a deal and select another one

- browse
	- what do they select
	- 
- upload
	- user
	- 
- screen: deal view
	- redemption vs favorite vs back
	- search query
	- deal id
- screen: my favorites
	- 
- screen: my deals
	- histogram of number of times viewing this screen vs % of users
	- 

- screen: my stats
	- histogram of number of times viewing this screen vs % of users


