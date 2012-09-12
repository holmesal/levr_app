$(window).load(function(){
	var endTime = (new Date()).getTime();
    var millisecondsLoading = endTime - startTime;
	
	mixpanel.track("Merchant Beta Page Loaded",{"Load Time":millisecondsLoading});
	
	$('#signupForm').submit(function(e){
		e.preventDefault()
		mixpanel.track("Merchant Beta Signup",{"business_name":$('#business_name').val(),"contact_name":$('#contact_name').val(),"contact_email":$('#contact_email').val(),"contact_phone":$('#contact_phone').val()},function(){
			mixpanel.people.identify($('#business_name').val(),function(){
				mixpanel.people.set({"business_name":$('#business_name').val(),
							"$name":$('#contact_name').val(),
							"$email":$('#contact_email').val(),
							"contact_phone":$('#contact_phone').val()},function(){
								//$('#signupForm').submit()
							});
			});
		
		});
	})
	
	
})