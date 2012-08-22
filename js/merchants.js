function attemptLogin(){
	data = {
		email:	$('#emailInput').val(),
		pw:		$('#pwInput').val()
	}
	
	$.ajax({
		type:	'POST',
		data:	data,
		url:	window.location.pathname
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