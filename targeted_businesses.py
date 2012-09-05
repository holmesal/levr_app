
# Determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs. This fuction
# returns True or False.  The algorithm is called
# "Ray Casting Method".

def point_in_poly(x,y,poly):

	n = len(poly)
	inside = False

	p1x,p1y = poly[0]
	for i in range(n+1):
		p2x,p2y = poly[i % n]
		if y > min(p1y,p2y):
			if y <= max(p1y,p2y):
				if x <= max(p1x,p2x):
					if p1y != p2y:
						xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
					if p1x == p2x or x <= xinters:
						inside = not inside
		p1x,p1y = p2x,p2y

	return inside


#This is where the places wrapper can be found: https://github.com/slimkrazy/python-google-places
from googleplaces import GooglePlaces
#import types
API_KEY = 'AIzaSyDM4iR9vK4uKUJjdpXIsOcEAKkM-xa9g7g'




#create geo boundary
poly_lat = [42.35604793867138, 42.3536306062291, 42.35301975662632, 42.35130590336475, 42.35025979303107, 42.34889896173047, 42.3474035881804, 42.34587017442897, 42.3454410032402, 42.34240376898205, 42.34200386027403, 42.34665152547006, 42.34437686280481, 42.34335156373593, 42.34544719585433, 42.34689842049458, 42.35112647889721, 42.35062769794382, 42.35071497934108, 42.35189268933054, 42.35225746246078, 42.35405913476999, 42.35424633071435, 42.35461863217454, 42.35493709975472, 42.35550741935002, 42.35597048179658]
poly_lng = [-71.13128751569184, -71.13747576487495, -71.13221920314751, -71.1315606660475, -71.1309193072284, -71.1297731686955, -71.12886527141396, -71.12773981063141, -71.12726203628873, -71.1216289071829, -71.12121164180434, -71.10497418088163, -71.1040140000405, -71.10267756839711, -71.0946922485677, -71.09243243954906, -71.09227823963506, -71.0950832349529, -71.097815779737, -71.11251814985596, -71.11356954283684, -71.11706884229781, -71.11779512636194, -71.11965434764042, -71.12212678446998, -71.12626327632834, -71.13026582412857]
polygon = zip(poly_lat,poly_lng)
print polygon

x = 42.349712
y = 71.119995
print point_in_poly(x,y,polygon)




#LAT_LNG	= {
#			'lat': 42.35604793867138,#42.349712,
#			'lng': -71.13128751569184#-71.119995}
#			}
TYPES	= []#['establishment']
KEYWORD	= 'food'
RADIUS	= 100

#these are the sample points
t = [42.35130590336475, 42.35025979303107, 42.34889896173047, 42.3474035881804]
g = [-71.1315606660475, -71.1309193072284, -71.1297731686955, -71.12886527141396]
points=zip(t,g)

businesses = set() #is a set to eliminate duplicates

for point in points:
	print point
	print list(point)
	p = list(point)
	lat = p[0]
	lng = p[1]
	LAT_LNG = {
				'lat':lat,
				'lng':lng
				}
	query_result = GooglePlaces(API_KEY).query(
			lat_lng=LAT_LNG,
			keyword=KEYWORD,
#			radius=RADIUS,
			rankby='distance',
			types=TYPES)


	print query_result.places.__len__()
	
	for place in query_result.places:
		# Returned places from a query are place summaries.
		print place.geo_location
		print place.name
		x = place.geo_location['lat']
		y = place.geo_location['lng']
		if point_in_poly(x,y,polygon):
			place.get_details()
			vicinity = place.vicinity
			name			= place.name
			geo_location	= (x,y) #(lat,lng) tuple
			reference		= place.reference
			toople = (name,vicinity,geo_location)
			print toople
			businesses.add(toople)
	print businesses
