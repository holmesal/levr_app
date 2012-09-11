$(window).load(function(){
	var endTime = (new Date()).getTime();
    var millisecondsLoading = endTime - startTime;
	
	mixpanel.track("Merchant Beta Page Loaded",{"Load Time":millisecondsLoading})
	
	$('#btnSubmit').click(function(){
		mixpanel.track("Merchant Beta Signup",{"business_name":$('#business_name').text(),"contact_name":$('#contact_name').text(),"contact_email":$('#contact_email').text(),"contact_phone":$('#contact_phone').text()})
		alert('hi there')
	})
	
	
})