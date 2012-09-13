$(document).ready(function(){
	$('#editEmail').click(function(){
		// wants to show edit email form
		//if other form is open, close
		if($('#editPasswordForm').hasClass('hidden')===false){
			//edit password is open, so close before opening email edit
			$('#editPasswordForm').addClass('hidden')
			$('#editEmailForm').removeClass('hidden')
		}else if($('#editEmailForm').hasClass('hidden')===false){
			// edit email is ALREADY OPEN, so close it
			$('#editEmailForm').addClass('hidden')
			$('#error_field').text('')
			
		}else{
			//open edit email form
			$('#editEmailForm').removeClass('hidden')
		}
	})
	
	$('#editPassword').click(function(){
		//if other form is open, close
		if($('#editEmailForm').hasClass('hidden')===false){
			// other form is open, so close
			$('#editEmailForm').addClass('hidden')
			$('#editPasswordForm').removeClass('hidden')
		}else if($('#editPasswordForm').hasClass('hidden')===false){
			// this form is open, so close
			$('#editPasswordForm').addClass('hidden')
			$('#error_field').text('')
		}else{
			// this form is not open, so open
			$('#editPasswordForm').removeClass('hidden')
		}
		// if($('#editEmailForm').hasClass('hidden')===false){
			// console.log('trip true')
			// $('#editEmailForm').toggle(300,function(){
				// $('#editPasswordForm').toggle(300)
			// })
		// }else{
			// console.log('trip false')
			// $('#editPasswordForm').toggle(300)
		// }
	})
	$('#old_password1').blur(function(){
		console.log('blur')
		checkPassword($('#old_password1'))
	})
	$('#old_password2').blur(function(){
		checkPassword($('#old_password2'))
		
	})
})
function checkPassword(passwordObj,formObj){
		console.log('check')
		password = passwordObj.val()
		creds = {
			'password': password
		}
		//check password
		url_string = '/merchants/myAccount/checkPassword'
		$.ajax({
			type:	'POST',
			url:	url_string,
			data:	creds,
			success: function(result){
				console.log("response: " + result)
				if (result == 'True'){
					if(formObj){
						formObj.submit()
					}
					passwordObj.parent().removeClass('error')
					$('#error_field').text('')
					
					
				} else{
					passwordObj.parent().addClass('error')
					$('#error_field').text('The password you submitted is incorrect.')
				}
			}
		})
	}
function isValidEmailAddress(emailAddress) {
	console.log(emailAddress)
	var pattern = new RegExp(/^((([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+(\.([a-z]|\d|[!#\$%&'\*\+\-\/=\?\^_`{\|}~]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])+)*)|((\x22)((((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(([\x01-\x08\x0b\x0c\x0e-\x1f\x7f]|\x21|[\x23-\x5b]|[\x5d-\x7e]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(\\([\x01-\x09\x0b\x0c\x0d-\x7f]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF]))))*(((\x20|\x09)*(\x0d\x0a))?(\x20|\x09)+)?(\x22)))@((([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|\d|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.)+(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])|(([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])([a-z]|\d|-|\.|_|~|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])*([a-z]|[\u00A0-\uD7FF\uF900-\uFDCF\uFDF0-\uFFEF])))\.?$/i);
	return pattern.test(emailAddress);
};

function validate(form,submit){
	console.log(form)
	if(form === 'email'){
		email = $('#new_email').val()
		confirm_email = $('#confirm_new_email').val()
		
		if(isValidEmailAddress(email)){
			$('#new_email').parent().removeClass('error')
			$('#error_field').text('')
			if(email===confirm_email){
				//emails match
				$('#confirm_new_email').parent().removeClass('error')
				$('#error_field').text('')
				
				//check password
				checkPassword($('#old_password1'),$('#editEmailForm'))
			}else{
				//emails do not match
				$('#confirm_new_email').parent().addClass('error')
				$('#error_field').text('Emails do not match')
			}
		}else{
			$('#new_email').parent().addClass('error')
			$('#error_field').text('Please enter a valid email address')
		}
		
	}else if(form === 'password'){
		password = $('#new_password').val()
		confirm_password = $('#confirm_new_password').val()
		
		if(password === confirm_password){
			//passwords match
			$('#confirm_new_password').parent().removeClass('error')
			$('#error_field').text('')
			
			//check password
			checkPassword($('#old_password2'),$('#editPasswordForm'))
		}else{
			$('#confirm_new_password').parent().addClass('error')
			$('#error_field').text('Passwords do not match')
		}
	}
	
}
