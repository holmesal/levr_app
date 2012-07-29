$(document).ready(function() {
	
	//register typing listeners
	$('.textIn').keyup(function() {
		console.log(this)
		//if it's deal line2, add inputted text to the middle of a parenthetical
		if (this.name=='deal_line2' && $(this).val().length > 0) {
			$('#deal_line2').text('(with purchase of '+$(this).val()+')')
		} else if ($(this).val().length == 0) {
			$('#'+this.name).html('&nbsp;')
		} else{
			$('#'+this.name).text($(this).val())
		}
	})
	
	//initialize places service
	var input = document.getElementById('business_select');
	var options = {types: ['establishment']};
	autocomplete = new google.maps.places.Autocomplete(input, options);
	
	//initialize place_changed listener
	var place = {};
	google.maps.event.addListener(autocomplete, 'place_changed', function() {
		var place = autocomplete.getPlace();
		$('#deal_business').text(place.name);
		$('#deal_address').text(place.vicinity);
	});
	
	//listen for a change in the file button, use that to upload images
	$('#img_upload').change(function(){
		$('#uploaded_img').css('background-image','url(../img/landing_background.jpeg)')
	})
	
});