
$(document).ready(function() {

var map;

function initialize() {
	var mapOptions = {
		center: new google.maps.LatLng(42.349918,-71.10476),
		mapTypeId: google.maps.MapTypeId.ROADMAP,
		disableDefaultUI: true,
		draggable: false,
		disableDoubleClickZoom: true,
		zoom: 15,
		scrollwheel: false
	};
	map = new google.maps.Map(document.getElementById('gmap'),mapOptions);
}

google.maps.event.addDomListener(window, 'load', initialize);
  
function showDetails(){
	//refocus map on place
	place = autocomplete.getPlace();
	console.log(place)
	var position = new google.maps.LatLng(place.geometry.location.Xa,place.geometry.location.Ya)
	console.log(position.toString())
	map.panTo(position)
	//reset previous values from places
	$('#icon').attr("src",'#')
	$('#name,#textName,#address,#number,#website').text('')
	//set values from places
	$('#icon').attr("src",place.icon)
	$('#name,#textName').text(place.name)
	$('#address').text(place.formatted_address)
	$('#number').text(place.formatted_phone_number)
	$('#website').text(place.website)
	
	$('#placeDetails').show()
}

function showSignup(){
	$('#placeDetails,#whoAreYou').animate({opacity: 0}).hide()
	$('#container').animate({'height': '430px'})
	$('#signup').show()
}

function showChoices(){
	$('#signup').animate({opacity: 0}).hide()
	$('#container').animate({'height': '430px'})
	$('#choices').show()
}

function attemptSignup(){
	//break if not equal
	if ($('#pw').val() != $('#pw2').val()) {
		return false
	} 
	
	var data = {
		email:	$('#email').val(),
		pw:		$('#pw').val()
	}
	
	showChoices()
	
	/*$.ajax({
		type:	'GET',
		data:	data
	})*/
}

function submitData(destination,place){
	console.log(place)
	var data = {
		destination:	destination,
		business_name:	place.name,
		vicinity:		place.vicinity,
		geo_point:		place.geometry.location.Xa + "," + place.geometry.location.Ya,
		types:			place.types
	}
	
	var URLstring = window.location.pathname + '?' + $.param(data)
	//set form action
	$('.emptyForm').attr('action',URLstring)
	$('.emptyForm').submit()
}


//initialize places service
var input = document.getElementById('business_select');
var options = {types: ['establishment']};
autocomplete = new google.maps.places.Autocomplete(input, options);

//initialize place_changed listener
var place = {};
google.maps.event.addListener(autocomplete, 'place_changed', function() {
	//show the details
	$('#container').animate({'height': '550px'},function(){showDetails()});
})

//initialize confirm click listener
$('#btnConfirm').click(function(){showSignup()})

//initialize signup click listener
$('#btnSignup').click(function(){attemptSignup()})

//initialize button click listeners
$('#btnUpload').click(function(){submitData('upload',place)})
$('#btnCreate').click(function(){submitData('create',place)})

})