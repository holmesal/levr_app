#import levr_classes as levr

#This is where the places wrapper can be found: https://github.com/slimkrazy/python-google-places
from googleplaces import GooglePlaces

# Determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs. This fuction
# returns True or False.  The algorithm is called
# "Ray Casting Method".

def point_in_poly(x, y, poly):

	n = len(poly)
	inside = False

	p1x, p1y = poly[0]
	for i in range(n + 1):
		p2x, p2y = poly[i % n]
		if y > min(p1y, p2y):
			if y <= max(p1y, p2y):
				if x <= max(p1x, p2x):
					if p1y != p2y:
						xinters = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
					if p1x == p2x or x <= xinters:
						inside = not inside
		p1x, p1y = p2x, p2y

	return inside

#data = [
#	- 71.13291567731757, 42.35554491199912, 0 - 71.13371142324495, 42.35317880718497, 0 - 71.13071182248666, 42.35289425055202, 0 - 71.13120518406669, 42.35121446445319, 0 - 71.12951035135833, 42.34920812692455, 0 - 71.12830549341774, 42.3468052971652, 0 - 71.12592906032192, 42.34488439481419, 0 - 71.12421419842904, 42.343752552996, 0 - 71.12227464653085, 42.34263570582295, 0 - 71.12299930022292, 42.34161471905097, 0 - 71.12065810066707, 42.34012858302157, 0 - 71.12008937946634, 42.34237078340382, 0 - 71.11717797680373, 42.34312576500385, 0 - 71.11297801076428, 42.34423285638898, 0 - 71.10925581162213, 42.34516971467844, 0 - 71.10611554302466, 42.34615224076367, 0 - 71.10442484360148, 42.34481638440683, 0 - 71.10258028422642, 42.34326677877443, 0 - 71.10059296644449, 42.34517741879495, 0 - 71.09861831469122, 42.3470223284111, 0 - 71.09722081635779, 42.34823347557149, 0 - 71.09475160912974, 42.34963713278553, 0 - 71.09749017370243, 42.3496346818714, 0 - 71.1011879442639, 42.34993818517612, 0 - 71.10576272712214, 42.35050758481145, 0 - 71.10976333416478, 42.35093388400737, 0 - 71.11328415581951, 42.35119022006207, 0 - 71.11774445071369, 42.35178222332647, 0 - 71.12167291908858, 42.3523710674681, 0 - 71.12553396759073, 42.35315711697848, 0 - 71.1291265033779, 42.35395797070547, 0 - 71.12786802070478, 42.35167827577001, 0 - 71.12427600791742, 42.35097974863034, 0 - 71.11995661357103, 42.35019482854115, 0 - 71.11526733504046, 42.34961707764953, 0 - 71.09983109334259, 42.34818877813406, 0 - 71.10261625382694, 42.34606580261889, 0 - 71.12065362440021, 42.34392584742306, 0 - 71.125125153395, 42.34674378297035, 0 - 71.1263241505234, 42.34958151468953, 0 - 71.13291567731757, 42.35554491199912, 0 
#	]

data = [- 71.13291567731757, 42.35554491199912, 0 - 71.13371142324495, 42.35317880718497, 0
	]

zipped = zip(data[0::2], data[1::2])

lat = []
lng = []

for point in zipped:
	lng.append(point[0])
	lat.append(point[1])

#these are the sample points
#lng = [-71.13231864637851]
#lat = [42.3528309839968]
print lat.__len__()
points = zip(lat, lng)

#print lon
#print lat
#import types
API_KEY = 'AIzaSyDM4iR9vK4uKUJjdpXIsOcEAKkM-xa9g7g'

#create geo boundary
poly_lat = [42.35604793867138, 42.3536306062291, 42.35301975662632, 42.35130590336475, 42.35025979303107, 42.34889896173047, 42.3474035881804, 42.34587017442897, 42.3454410032402, 42.34240376898205, 42.34200386027403, 42.34665152547006, 42.34437686280481, 42.34335156373593, 42.34544719585433, 42.34689842049458, 42.35112647889721, 42.35062769794382, 42.35071497934108, 42.35189268933054, 42.35225746246078, 42.35405913476999, 42.35424633071435, 42.35461863217454, 42.35493709975472, 42.35550741935002, 42.35597048179658]
poly_lng = [-71.13128751569184, -71.13747576487495, -71.13221920314751, -71.1315606660475, -71.1309193072284, -71.1297731686955, -71.12886527141396, -71.12773981063141, -71.12726203628873, -71.1216289071829, -71.12121164180434, -71.10497418088163, -71.1040140000405, -71.10267756839711, -71.0946922485677, -71.09243243954906, -71.09227823963506, -71.0950832349529, -71.097815779737, -71.11251814985596, -71.11356954283684, -71.11706884229781, -71.11779512636194, -71.11965434764042, -71.12212678446998, -71.12626327632834, -71.13026582412857]
#poly_lat = [42.35604793867138]
#poly_lng = [-71.13128751569184]
polygon = zip(poly_lat, poly_lng)
#print polygon

#x = 42.349712
#y = 71.119995
#print point_in_poly(x,y,polygon)

TYPES	 = ['establishment']
KEYWORD	 = None#'food'
RADIUS	 = 100




#(name, geo_point) for checking if it already exists in the set - to eliminate a lot of redundant queries
businesses_check = set()

#open business file for writing out 
businesses_food = open('businesses-food.txt', 'w')
businesses_other = open('businesses-other.txt', 'w')
print businesses_food
print businesses_other
queries = 0
places = 0
checked = 0
valid = 0
food = 0
other = 0
print points

print_glob = ''
for point in points:
	queries += 1
#	print point
#	print list(point)
	p = list(point)
	#grab lat, lng from the point in question
	lat = p[0]
	lng = p[1]
	LAT_LNG = {
				'lat':lat,
				'lng':lng
				}
	#query google places
	query_result = GooglePlaces(API_KEY).query(
			lat_lng=LAT_LNG,
			types=TYPES,
			rankby='distance',
			keyword=KEYWORD
			)


	for place in query_result.places:
		places +=1
		# Returned places from a query are place summaries, not the whole object
		x = place.geo_location['lat']
		y = place.geo_location['lng']
		geo_string	 = "" + str(x) + "," + str(y)
		name		 = place.name
		business	 = (name, geo_string)
		
#		print business
		if business not in businesses_check:
			checked += 1
			#business is not in the set of already checked businesses
			if point_in_poly(x, y, polygon):
				valid += 1
				#business exists in our range
				#get additional details from place
				place.get_details()
				vicinity	 = place.vicinity
				types		 = place.types
				types		 = ','.join(types)
				print_str = name + "\t" + vicinity + "\t" + geo_string + "\t" + types + "\n"
				
				if 'food' in types or 'restaurant' in types or 'bar' in types:
					food += 1
					#output business info to txt file
					print print_str
					businesses_food.write(print_str)
				else: 
					other += 1
					print '!!!'+ print_str
					businesses_other.write(print_str)
				
				
				#add business to set of businesses that have been checked
			businesses_check.add(business)
businesses_food.close()
businesses_other.close()

print queries
print places
print checked
print valid
print food
print other