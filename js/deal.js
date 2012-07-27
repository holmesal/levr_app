$(document).ready(function() {
	
	api_key = AIzaSyDA6oSrrTbFLHVqZSt2JGeJWFLVa9F0074;
	
	//register typing listeners
	$('.textin').keyup(function() {
		$('#'+this.name).text($(this).val())
	})
	
	$('#business_select').keyup(function){
		ajax
	}
});