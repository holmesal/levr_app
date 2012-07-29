function autocomplete_click() {
	$('.result').click(function(){
		//populate box and phone
		$('#business_select').val($('.result_primary',this).text())
		$('#deal_business').text($('.result_primary',this).text())
		//hide autocomplete
		$('#results').css('visibility','hidden')
		//go get places detail request, reference is this.id
		url = 'https://maps.googleapis.com/maps/api/place/details/json?key=AIzaSyDA6oSrrTbFLHVqZSt2JGeJWFLVa9F0074&sensor=false&reference='+this.id
		$.ajax({
				url: url,
				type: 'GET',
				success: function(result) {
					$('#deal_address').text(result.result.vicinity);
				}
				
			});
	})
	
}

function populate_autocomplete(predictions) {
	//empty current autocomplete
	$('#results').empty();
	
	$.each(predictions, function(i,prediction){
		primary = prediction.terms[0].value
		//split string after comma
		idx = prediction.description.indexOf(',') + 2
		secondary = prediction.description.substring(idx)
		
		html_string = '<div class="result" id="'+prediction.reference+'"><p class="result_primary">'+primary+'</p><p class="result_secondary">'+secondary+'</p></div>';
		
		//append new result
		$('#results').append(html_string);
	})
	//register listeners
	autocomplete_click();	
}

$(document).ready(function() {
	
	//register typing listeners
	$('.textin').keyup(function() {
		//if it's deal line2, add inputted text to the middle of a parenthetical
		if (this.name=='deal_line2' && $(this).val().length > 0) {
			$('#deal_line2').text('(with purchase of '+$(this).val()+')')
		} else if ($(this).val().length == 0) {
			$('#'+this.name).html('&nbsp;')
		} else{
			$('#'+this.name).text($(this).val())
		}
	})
	
	//typing listeners for business selector
	$('#business_select').keyup(function() {
		if ($(this).val().length > 2){
			url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json?input=' + $(this).val() + '&sensor=false&types=establishment&key=AIzaSyDA6oSrrTbFLHVqZSt2JGeJWFLVa9F007';
			
			$.ajax({
				url: url,
				type: 'GET',
				success: function(result) {
					$('#results').css('visibility','visible')
					populate_autocomplete(result.predictions)
				}
				
			});
		} else{
			$('#results').css('visibility','hidden')
		}
	});
	
	/* This is broken - it triggers the click event, but after the file dialog closes the change event is not triggered
	//click listener for image upload pretty button
	$('#uploaded_img').click(function() {
		$('#img_upload').click();
	})*/
	
	//listen for a change in the file button, use that to upload images
	$('#img_upload').change(function(){
		$('#uploaded_img').css('background-image','url(../img/landing_background.jpeg)')
	})
	
});