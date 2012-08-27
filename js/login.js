$(document).ready(function(){

	$('#btnHelp').click(function(){
		$('#loginForm').toggle(300,function(){
			$('#forgotPasswordForm').toggle(300);
			$('#email').val($('#emailInput').val());
		});
	})
	$('#btnBack').click(function(){
		$('#forgotPasswordForm').toggle(300,function(){
			$('#loginForm').toggle(300);
			$('#emailInput').val($('#email').val());
		});
	})
})