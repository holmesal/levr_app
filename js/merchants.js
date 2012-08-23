function attemptLogin(){
	var creds = {
		email:	$('#emailInput').val(),
		pw:		$('#pwInput').val(),
		type:	'ajax'
	}
	
	console.log(creds)
	
	url_string = 'merchants/login'
	
	$.ajax({
		type:	'POST',
		url:	url_string,
		data:	creds,
		success: function(result){
			console.log(result)
			if (result == 'True'){
				//submit the form
				$('#loginForm').submit()
			} else{
				$('#loginWelcome').text('Incorrect email/password.')
				$('#loginWelcome').css({'color':'red'})
			}
		}
	})
}

$(document).ready(function(){
	//expanded global var
	var expanded = false;
	//register login click listener
	$('#loginStub').click(function(){
		if (expanded == false){
			$('#loginBox').animate({'margin-top':'0px'})
			expanded = true
		} else{
			$('#loginBox').animate({'margin-top':'-160px'})
			expanded = false
		}
		
	})
	
	//register listener for login button
	$('#btnLogin').click(function(){attemptLogin()})
	
})