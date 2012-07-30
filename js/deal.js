function validateAllFields(){
	var pass = true;
	
	$('.textIn').each(function(){
		if ($(this).val().length < 1){
			$(this).prev().addClass('input_error');
			pass=false;
		}
	});
	if (!$('#img_upload').val()){
		$('#img_upload').prev().addClass('input_error');
		pass=false;
	}
	
	return pass;
	
}

function previewImage(input){
	if (input.files && input.files[0]) {
		$('#img_upload').prev().removeClass('input_error');
        var reader = new FileReader();
        reader.onload = function (e) {
        	
        	$('#uploaded_img').css('background-image','url('+e.target.result+')');
        };

        reader.readAsDataURL(input.files[0]);
    }
}

$(document).ready(function() {
	
	//register typing listeners
	$('.textIn').keyup(function() {
		//if it's deal line2, add inputted text to the middle of a parenthetical
		if (this.name=='deal_line2' && $(this).val().length > 0) {
			$('#deal_line2').text('(with purchase of '+$(this).val()+')')
		} else if ($(this).val().length == 0) {
			$('#'+this.name).html('&nbsp;')
		} else{
			$('#'+this.name).text($(this).val())
		}
	})
	
	//register lostfocus listeners
	$('.textIn,#deal_submit').blur(function(){
		if ($(this).val().length < 1){
			$(this).prev().addClass('input_error');
		} else{
			$(this).prev().removeClass('input_error');
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
		console.log(place)
		//add types as a hidden field
		var types = document.createElement("input");
        types.setAttribute("type", "hidden");
        types.setAttribute("name", types);
        types.setAttribute("value", place.types);
        $('#deal_form').appendChild(types);
        //add vicinity as a hidden field
        var vicinity = document.createElement("input");
        types.setAttribute("type", "hidden");
        types.setAttribute("name", vicinity);
        types.setAttribute("value", place.vicinity);
        $('#deal_form').appendChild(vicinity);
        
	});
	
	//register submit button listener
	/*
	$('#deal_submit').click(function(e) { 
		if (!validateAllFields()) {
			e.preventDefault()
		}	
	 })
	*/
	//listen for a change in the file button, use that to upload images
	/*$('#img_upload').change(function(){
		$('#uploaded_img').css('background-image','url(../img/landing_background.jpeg)')
	})*/
	
});