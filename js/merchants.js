function attemptLogin() {
	var creds = {
		email : $('#emailInput').val(),
		pw : $('#pwInput').val(),
		type : 'ajax'
	}

	console.log(creds)

	url_string = '/merchants/login'

	$.ajax({
		type : 'POST',
		url : url_string,
		data : creds,
		success : function(result) {
			console.log(result)
			if (result == 'True') {
				mixpanel.people.identify(creds.email)
				mixpanel.people.set({
					"$last_login": new Date(),
				})
				mixpanel.identify(creds.email)
				console.log('register')
				mixpanel.track("User logging in", {
					"success" : true
				}, function() {
					console.log('login')
					// submit the form
					$('#loginForm').submit()
				})

			} else {
				mixpanel.track("User logging in", {
					"success" : false
				}, function() {
					$('#loginWelcome').text('Incorrect email/password.')
					$('#loginWelcome').css({
						'color' : 'red'
					})

				})
			}
		}
	})
}

$(document).ready(function() {
	var endTime = (new Date()).getTime();
	var millisecondsLoading = endTime - startTime;
	mixpanel.track("Merchants Landing Page Loaded", {
		"Load Time" : millisecondsLoading
	})
	// expanded global var
	var expanded = false;
	// register login click listener
	$('#loginStub').click(function() {
		if (expanded == false) {
			$('#loginBox').animate({
				'margin-top' : '0px'
			})
			expanded = true
			mixpanel.track("Login Stub Clicked")
		} else {
			$('#loginBox').animate({
				'margin-top' : '-160px'
			})
			expanded = false
		}

	})

	// register listener for login button
	$('#btnLogin').click(function() {
		attemptLogin();

	})

})