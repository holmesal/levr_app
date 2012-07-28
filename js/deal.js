$(document).ready(function() {
	
	//register autocomplete
	var availableTags = [
			"ActionScript",
			"AppleScript",
			"Asp",
			"BASIC",
			"C",
			"C++",
			"Clojure",
			"COBOL",
			"ColdFusion",
			"Erlang",
			"Fortran",
			"Groovy",
			"Haskell",
			"Java",
			"JavaScript",
			"Lisp",
			"Perl",
			"PHP",
			"Python",
			"Ruby",
			"Scala",
			"Scheme"
		];
		
	$('#business_select').autocomplete({
		source: availableTags
	});
	
	//register typing listeners
	$('.textin').keyup(function() {
		$('#'+this.name).text($(this).val())
	})
	
	
	$('#business_select').keyup(function() {
		url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json?input=' + $(this).val() + '&sensor=false&types=establishment&key=AIzaSyDA6oSrrTbFLHVqZSt2JGeJWFLVa9F0074';
		console.log(url)
		
		$.ajax({
			url: url,
			type: 'GET',
			success: function(result) {
				console.log(result)
			}
			
		});
		
	});
});