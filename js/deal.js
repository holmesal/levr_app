$(document).ready(function() {
	
	//register typing listeners
	$('.textin').keyup(function() {
		$('#'+this.name).text($(this).val())
	})
	
	$('#business_select').keyup(function() {
		url = 'https://maps.googleapis.com/maps/api/place/autocomplete/json?input=' + $(this).val() + '&sensor=false&types=establishment&key=AIzaSyDA6oSrrTbFLHVqZSt2JGeJWFLVa9F0074';
		console.log(url)
		
		$.ajax({
			url: 'http://api.hostip.info/get_json.php',
			type: 'GET',
			crossdomain: true,
			success: function(result) {
				console.log(result)
				console.log('success')
				result['Content-Length'] = len(result)
			}
			
		});
		
		/*$.get('http://api.hostip.info/get_json.php', function(data) {
		  $('.result').html(data);
		  alert('Load was performed.');
		});*/
		
		
		$.ajax({
			url: url,
			type: 'GET',
			success: function(result) {
				console.log(result)
			}
			
		});
	});
});