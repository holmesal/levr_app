
$(document).ready(function() {

$('#gmap').click(function(e) { e.preventDefault })

$('#business_select').focus()

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
	//console.log(place)
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
	
	$(document).keypress(function(e) {
	    if(e.which == 13) {
	        $('#btnConfirm').click()
	    }
	    if(e.which == 9){
		    $('#btnConfirm').focus()
	    }
	});
}

function showSignup(){
	$('#placeDetails,#whoAreYou').animate({opacity: 0}).hide()
	$('#container').animate({'height': '450px'})
	$('#signup').show()
	$('#email').focus()
	$(document).keypress(function(e) {
	    if(e.which == 13) {
	        $('#btnSignup').click()
	    }
	});
}

function showChoices(){
	$('#signup').animate({opacity: 0}).hide()
	$('#container').animate({'height': '430px'})
	$('#choices').show()
}

function isValidEmailAddress(emailAddress) {
	console.log(emailAddress)
    var pattern = new RegExp(/^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i);
    return pattern.test(emailAddress);
};

function attemptSignup(){

	checkEmail(false)

	//break if less than 5 characters
	if ($('#pw').val() < 5){
		$('#error_field').text('Please enter a password at least 5 characters long.')
		return false
	}
	
	//break if not equal
	if ($('#pw').val() != $('#pw2').val()) {
		$('#error_field').text('Passwords must match.')
		return false
	} 
	
	checkEmail(true)
	
	
	/*$.post(url,data,function(creds){
		console.log(creds)
	})*/
}

function checkEmail(submit){
	var creds = {
		email:	$('#email').val(),
		pw:		$('#pw').val()
	}
	
	
	url_string = 'emailCheck'
	
	$.ajax({
		type:	'POST',
		url:	url_string,
		data:	creds,
		success: function(result){
			console.log("response: " + result)
			if (result == 'True'){
				if (submit == true){
					showChoices()
				}
			} else{
				$('#error_field').text('Sorry, that email is already in use.')
			}
		}
	})
}

function submitData(destination,place){
	console.log(place)
	console.log(place.types)
	var data = {
		email:			$('#email').val(),
		password:		$('#pw').val(),
		destination:	destination,
		business_name:	place.name,
		vicinity:		place.vicinity,
		geo_point:		place.geometry.location.Xa + "," + place.geometry.location.Ya,
		types:			place.types
	}
	
	var URLstring = window.location.pathname + '?' + $.param(data)
	console.log(URLstring)
	//set form action
	$('#form1').attr('action',URLstring)
	$('#form1').submit()
}


//initialize places service
var input = document.getElementById('business_select');
var options = {types: ['establishment']};
autocomplete = new google.maps.places.Autocomplete(input, options);

//initialize place_changed listener
var place = {};
google.maps.event.addListener(autocomplete, 'place_changed', function() {
	place = autocomplete.getPlace();
	//if this is an actual place, show the details
	if (place.id != undefined){
	//show the details
	$('#container').animate({'height': '550px'},function(){showDetails()});
	}
})



//initialize confirm click listener
$('#btnConfirm').click(function(){showSignup()})

//initialize a email field blur listener
$('#email').blur(function(){
	if( isValidEmailAddress($('#email').val()) ) {
		checkEmail(false)
	}
})

//initialize signup click listener
$('#btnSignup').click(function(){
	if( isValidEmailAddress($('#email').val()) ) {
		attemptSignup()
	} else{
		$('#error_field').text('Please enter a valid email address.')
	}
	
})

//initialize button click listeners
$('#btnUpload').click(function(){submitData('upload',place)})
$('#btnCreate').click(function(){submitData('create',place)})

//disable enter key on autocomplete
var input = document.getElementById('business_select'); 
                        // dojo.connect(input, 'onkeydown', function(e) { 
                        google.maps.event.addDomListener(input, 'keydown', function(e) { 
                                if (e.keyCode == 13) 
                                { 
                                        if (e.preventDefault) 
                                        { 
                                                e.preventDefault(); 
                                        } 
                                        else 
                                        { 
                                                // Since the google event handler framework does not handle
                                                e.cancelBubble = true; 
                                                e.returnValue = false; 
                                        } 
                                } 
                        });    
})