/*
Todo:
	load cities

*/

//Initialize namespace: levr
var levr = levr || {};
// deals is an array of deal objects
levr.deals = [];
// grab form object.
levr.credits = 100;

$(document).ready(function() {
	//prevent default for radio buttons
	$('.btn').click(function(e) {
		//console.log('default event prevented');
		e.preventDefault();
	});

	$('.radio-dealType').click(function() {
		// register this button as the active button
		levr.form.data.nameType(this.value);
		// remove error
		$('#group-dealType').removeClass('error');
		$('.radio-dealType').removeClass('btn-danger');
		//console.log(levr.form.data.getValues());
	})

	$('.radio-discountType').click(function() {
		// register this button as the active button
		levr.form.data.dealType(this.value);
		// remove error
		$('#group-discountType').removeClass('error');
		$('.radio-discountType').removeClass('btn-danger');
		//console.log(levr.form.data.getValues());
	})
	$('#radio-category').click(function() {
		levr.nameType = "category";
		//show/hide appropriate fields
		$('.dealCategory').removeClass('hidden');
		$('.dealSpecific').addClass('hidden');
		$('#review-categoryTag, #review-categoryDescription').parent().removeClass('hidden');
		$('#review-specificName, #review-specificTag, #review-specificDescription').parent().addClass('hidden');
	})
	$('#radio-itemName').click(function() {
		levr.nameType = "itemName";
		//show/hide appropriate fields
		$('.dealSpecific').removeClass('hidden');
		$('.dealCategory').addClass('hidden');
		$('#review-specificName, #review-specificTag, #review-specificDescription').parent().removeClass('hidden');
		$('#review-categoryTag, #review-categoryDescription').parent().addClass('hidden');
	})
	$('#radio-percent').click(function() {
		levr.dealType = "percent";
		//show/hide appropriate fields
		$('#valueText').text('Percent')
		$('#text-dealValue').removeAttr('disabled');
		$('#review-dealValue').parent().removeClass('hidden');
	});
	$('#radio-monetary').click(function() {
		levr.dealType = "monetary";
		//show/hide appropriate fields
		$('#valueText').text('Dollars')
		$('#text-dealValue').removeAttr('disabled');
		$('#review-dealValue').parent().removeClass('hidden');
	});
	$('#radio-free').click(function() {
		levr.dealType = "free";
		//show/hide appropriate fields
		$('#valueText').text('')
		$('#text-dealValue').attr('disabled', 'disabled');
		$('#review-dealValue').parent().addClass('hidden');
	});

	$('#goTo1').click(function() {
		/*$('#collapse1Head').removeClass('hidden');
		$('.collapse1').trigger('click');
		$('#accord0').addClass("hidden");*/
		goToNext(0,1)
	});

	$('#goTo2').click(function() {
		if(levr.form.validate('fieldset-items')) {
			/*$('#collapse2Head').removeClass('hidden');
			$('.collapse2').trigger('click');*/
			goToNext(1,2)
		}
	});
	$('#goTo3').click(function() {
		if(levr.form.validate('fieldset-details')) {
			/*$('#collapse3Head').removeClass('hidden');
			$('.collapse3').trigger('click');*/
			goToNext(2,3)
		}
	});
	$('#goTo4').click(function() {
		if(levr.form.validate('fieldset-offer')) {
			/*$('#collapse4Head').removeClass('hidden');
			$('.collapse4').trigger('click');*/
			goToNext(3,4)
		}
	});
	$('#goTo5').click(function() {
		if(levr.form.validate('fieldset-businessInfo')) {
			/*$('#collapse5Head').removeClass('hidden');
			$('.collapse5').trigger('click');*/
			goToNext(4,5)
		}
	});
	$('#goTo6').click(function() {
		if(levr.form.validate('fieldset-contactInfo')) {
			levr.populateReview();
			/*$('#collapse6Head').removeClass('hidden');
			$('.collapse6').trigger('click');*/
			goToNext(5,6)
		}

	});
	$('#skipTo6').click(function() {
		if(levr.form.validate('editDeal')) {
			levr.populateReview();
			$('#collapse6Head').removeClass('hidden');
			$('.collapse6').trigger('click');
			$('#collapse1Head, #collapse2Head, #collapse3Head').removeClass('hidden');

		}

	});

	$('.collapse6').click(function() {
		//find current fieldset
		//if(levr.form.validate('fieldset-offer')) {
		levr.populateReview();

		//}
	});
	$('#btnSubmit').click(function() {
		// validate whole form
		levr.form.submit();
	})

	$('#btnUpdateDeal').click(function() {
		levr.form.updateDeal();
	});

	$('#btnUpdateAccount').click(function() {
		levr.form.updateAccount();
	});
	// default the add button to off
	$('#btnAdd').attr("disabled", false);
	// check if field is empty on blur
	$("input:text,textarea,input:password").not("#refURL").blur(function() {
		//console.info('BLUR', $(this).attr('name'), ": ", $(this).val());
		var name = this.name;
		var value = this.value;
		levr.check[name](value);
	});

	//Keyup listener for text field
	$('#text-description').keypress(function() {
		$('#characterCounts').text(140 - $('#text-description').val().length + ' characters remaining.');
	});

	$('#btnRedemption').click(function() {
		var URL = "manageDeals.html?tab=redemption";
		document.location.href = URL;
	})
	$('#btnManage').click(function() {
		var URL = "manageDeals.html";
		document.location.href = URL;
	})

	$('#text-specificDescription').keypress(function() {
		$('#characterCounts-specificDescription').text(140 - $('#text-specificDescription').val().length + ' characters remaining.');
	});
	$('#text-categoryDescription').keypress(function() {
		$('#characterCounts-categoryDescription').text(140 - $('#text-categoryDescription').val().length + ' characters remaining.');
	});

	
	// clicking in the refURL box selects the text
	$("#refURL").focus(function() {
		$(this).select();
	});
	
	//
	$(document).bind("keydown", function(event) {
		if(event.which === 13 && !$(event.target).is('button')) {
			event.preventDefault();
			//stop event
		}
		return true;
	});

});

//hide and show
goToNext = function(currentNum, nextNum) {
	$('#accord'+currentNum).addClass('hidden');
	//$('#accord'+nextNum).removeClass('hidden');
	$('.collapse'+nextNum).trigger('click');
}

//========populateReview==========//
levr.populateReview = function() {
	//col1
	$('#review-dealTags').text($('#text-dealTag1').val() + ', ' + $('#text-dealTag2').val() + ', ' + $('#text-dealTag3').val());
	if(levr.nameType == 'itemName') {
		$('#review-nameType').text('Specific item');
	} else if(levr.nameType == 'category') {
		$('#review-nameType').text('Category');
	}
	var dealType = levr.form.data.getDealType();
	$('#review-dealType').text(dealType.charAt(0).toUpperCase() + dealType.slice(1));
	$('#review-dealValue').text($('#text-dealValue').val());
	$('#review-endValue').text($('#text-endValue').val() + ' customers');
	$('#review-dealCity').text($('#text-dealCity').val());

	$('#review-ownerName').text($('#text-ownerName').val());
	$('#review-phone').text($('#text-phone').val());
	$('#review-email').text($('#text-email').val())
	//sendEmails checkbox
	if($('#checkbox-sendEmails').is(':checked') == true) {
		$('#review-sendEmails').text('Yes');
	} else {
		$('#review-sendEmails').text('No');
	}
	////console.log($('#sendEmails').val())
	//$('#review-sendEmails')
	//col2
	$('#review-specificName').text($('#text-specificName').val());
	$('#review-specificTag').text($('#text-specificTag').val());
	$('#review-specificDescription').text($('#text-specificDescription').val());
	$('#review-categoryTag').text($('#text-categoryTag').val());
	$('#review-categoryDescription').text($('#text-categoryDescription').val());
	$('#review-businessName').text($('#text-businessName').val());
	$('#review-address1').text($('#text-address1').val());
	$('#review-address2').text($('#text-address2').val());
	$('#review-city').text($('#text-city').val());
	$('#review-zipCode').text($('#text-zipCode').val());
	$('#review-state').text($('#text-state').val());

	$('#creditsUsed').text($('#text-endValue').val());
	//$('#review-dealValue')
}
//=================================GENERAL===========================//

levr.formData = function() {
	// constructor for the function that hides the private form values
	var values = {
	};
	this.addValue = function(key, value) {
		// add a value to the form que
		values[key] = value;
	};
	this.deleteValue = function(key) {
		// delete a key:value pair from the form data que
		delete values[key];
	};
	this.getValues = function() {
		// return all form values
		return values;
	};
	this.getDealType = function() {
		return values['dealType'];
	};
	this.toJSON = function() {
		// return formData as json
		return JSON.stringify(values);
	};
	this.nameType = function(value) {
		// set nameType
		switch(value) {
			case 'itemName':
				values['nameType'] = 'itemName';
				break;
			case 'category':
				values['nameType'] = 'category';
				break;
			default:
				break;
		}
	};
	this.dealType = function(value) {
		// set dealType
		switch(value) {
			case 'percent':
				values['dealType'] = 'percent';
				break;
			case 'monetary':
				values['dealType'] = 'monetary';
				break;
			case 'free':
				values['dealType'] = 'free';
				break;
			default:
				delete values['dealType'];
				break;
		}

		/*/ set dealType as category
		 values['nameType'] = 'category';*/
	}
}
levr.form = {
	submit : function() {
		//console.info('submitting');
		// disable button so multiple submits cant happen
		$('#btnSubmit').attr('disabled', 'disabled');
		if(this.validate()) {
			//console.info("form validates")
			var requestObj = JSON.parse(levr.form.data.toJSON());
			requestObj.action = 'add';
			//console.log(requestObj);
			$.ajax({
				url : "./../php/newDeal.php",
				type : "POST",
				cache : false,
				async : false,
				// pull form data with function and json-ify it in one fell swoop
				data : JSON.stringify(requestObj),
				success : function(result) {
					//console.log(result);
					try {
						result = JSON.parse(result);
					} catch(error) {
						//console.log(error);
					}

					//console.log(result);
					switch(result.success) {
						case 0:
							//this.makeGroupError(result.errorFields);
							alert(result.errorFields)
							$('#submitButton').removeAttr('disabled');
							break;
						case 1:
							$('#accord1, #accord2, #accord3, #accord4, #accord5, #accord6').addClass('hidden');
							$('#collapseSevenHead').removeClass('hidden');
							$('.collapseSeven').trigger('click');
							$('#refURL').val('http://getlevr.com/merchants.html?ref=' + result.data.refID);
							$('#submitButton').removeAttr('disabled');
							$.ajax({
								url : "./../php/loginstate.php",
								type : "POST",
								cache : false,
								contentType : "application/JSON",
								data : JSON.stringify(requestObj),
								success : function(result) {
									// parse result
									result = JSON.parse(result);
									//hide or show "Manage" instead of "Login"
									if(result.success == 1) {
										$('#navLogin').attr('href', '#');
										$('#navLogin').text('Logout').click(function() {
											logout();
										});
										$('#navManage').removeClass('hidden');
										$('#navStart').text('New Offer')
									}

								},
								error : function() {
									//console.error('Get failed...Try again tomorrow.');
									return false;
								}
							});
							break;
						default:
							$('#submitButton').removeAttr('disabled');
							//php echoed something it shouldnt have
							break;
					}
				},
				error : function(request, error) {
					//console.error(request, error);
					$('#submitButton').removeAttr('disabled');
				}
			})
			// need return false to stop default submit function
			$('#submitButton').removeAttr('disabled');
		} else {
			//console.info("Form doesn't pass initial validation");
			// at least one field is empty and/or passwords don't match - DO NOTHING
			// need return false to stop default submit function

			//undisable submit button
			$('#submitButton').removeAttr('disabled');
		}

	},

	updateDeal : function() {
		//console.info('updating');
		// disable button so multiple submits cant happen
		$('#btnUpdateDeal').attr('disabled', 'disabled');
		if(this.validate()) {
			//console.info("form validates")
			var requestObj = JSON.parse(levr.form.data.toJSON());
			requestObj.action = 'updateDeal';
			requestObj.dealID = levr.dealID;
			//console.log(requestObj);
			$.ajax({
				url : "./../php/newDeal.php",
				type : "POST",
				cache : false,
				// pull form data with function and json-ify it in one fell swoop
				data : JSON.stringify(requestObj),
				success : function(result) {
					try {
						result = JSON.parse(result);
					} catch(error) {
						//console.log(error);
					}

					//console.log(result);
					switch(result.success) {
						case 0:
							// this is not the correct this.makeGroupError(result.errorFields);
							alert(result.errorFields);
							$('#btnUpdateDeal').removeAttr('disabled');
							break;
						case 1:
							window.location.replace('./manageDeals.html');

							$('#btnUpdateDeal').removeAttr('disabled');
							break;
						default:
							//php echoed something it shouldnt have
							break;
					}
				},
				error : function(request, error) {
					//console.error(request, error);
					$('#btnUpdateDeal').removeAttr('disabled');
				}
			})
			// need return false to stop default submit function
			$('#btnUpdateDeal').removeAttr('disabled');
		} else {
			//console.info("Form doesn't pass initial validation");
			// at least one field is empty and/or passwords don't match - DO NOTHING
			// need return false to stop default submit function

			//undisable submit button
			$('#btnUpdateDeal').removeAttr('disabled');
		}

	},

	updateAccount : function() {
		//console.info('updating');
		// disable button so multiple submits cant happen
		$('#btnUpdateAccount').attr('disabled', 'disabled');
		if(this.validate('updateAccount')) {
			//console.info("form validates")
			var requestObj = JSON.parse(levr.form.data.toJSON());
			requestObj.action = 'updateAccount';
			//console.log(requestObj);
			$.ajax({
				url : "./../php/newDeal.php",
				type : "POST",
				cache : false,
				// pull form data with function and json-ify it in one fell swoop
				data : JSON.stringify(requestObj),
				success : function(result) {
					try {
						result = JSON.parse(result);
					} catch(error) {
						//console.log(error);
					}

					//console.log(result);
					switch(result.success) {
						case 0:
							// this is not the correct this.makeGroupError(result.errorFields);
							alert(result.errorFields);
							$('#btnUpdateAccount').removeAttr('disabled');
							break;
						case 1:
							window.location.replace('./manageDeals.html?tab=account');
							$('#btnUpdateAccount').removeAttr('disabled');
							break;
						default:
							//php echoed something it shouldnt have
							break;
					}
				},
				error : function(request, error) {
					//console.error(request, error);
					$('#btnUpdateDeal').removeAttr('disabled');
				}
			})
			// need return false to stop default submit function
			$('#btnUpdateAccount').removeAttr('disabled');
		} else {
			//console.info("Form doesn't pass initial validation");
			// at least one field is empty and/or passwords don't match - DO NOTHING
			// need return false to stop default submit function

			//undisable submit button
			$('#btnUpdateAccount').removeAttr('disabled');
		}

	},

	validate : function(field) {
		// select all valid text-boxes for the given field
		//console.log(field);
		// flag is true until something is invalid
		var flag = true;
		switch(field) {
			case 'fieldset-items':
				///var elems = $('#fieldset-items input:text');
				var elems = $('#text-dealTag1');
				// trip flag if no radio is selected
				if(!($('#fieldset-items').find('.radio-dealType').is('.active'))) {
					// no selected button - add error class to group and trip flag
					$('#group-dealType').addClass('error');
					$('.radio-dealType').addClass('btn-danger');
					flag = false;
				}

				break;
			case 'fieldset-details':
				var elems = $('#fieldset-details input:text,#fieldset-details textarea').not(':hidden');
				// no radio buttons
				break;
			case 'fieldset-offer':
				var elems = $('#fieldset-offer input:text').not(':disabled');
				// trip flag if no radio is selected
				if(!($('#fieldset-offer').find('.radio-discountType').is('.active'))) {
					// no selected button - add error class to group and trip flag
					$('#group-discountType').addClass('error');
					$('.radio-discountType').addClass('btn-danger');
					flag = false;
				}
				//$('.radio-discountType').removeClass('btn-danger');
				break;
			case 'fieldset-businessInfo':
				var elems = $('#fieldset-businessInfo input:text');
				// no radios
				break;
			case 'fieldset-contactInfo':
				var elems = $('#fieldset-contactInfo input:text,#fieldset-contactInfo input:password');
				// no radios
				break;
			case 'fieldset-review':
				var elems = $('#fieldset-review input:text');
				break;

			case 'editDeal':
				var elems = $('#fieldset-items input:text, #fieldset-details input:text,#fieldset-details textarea, #fieldset-offer input:text').not(':disabled, :hidden');
				if(!($('#fieldset-items').find('.radio-dealType').is('.active'))) {
					// no selected button - add error class to group and trip flag
					$('#group-dealType').addClass('error');
					$('.radio-dealType').addClass('btn-danger');
					flag = false;
				}
				// trip flag if no radio is selected
				if(!($('#fieldset-offer').find('.radio-discountType').is('.active'))) {
					// no selected button - add error class to group and trip flag
					$('#group-discountType').addClass('error');
					$('.radio-discountType').addClass('btn-danger');
					flag = false;
				}
				break;
			case 'updateAccount':
				var elems = $('#fieldset-businessInfo input:text,#fieldset-contactInfo input:text').not(':disabled, :hidden');
				break;
			default:
				var elems = $('input:text,input:password,textarea').not(':hidden, :disabled,#refURL');
				field = 'all';
				if(!($('#fieldset-items').find('.radio-dealType').is('.active'))) {
					// no selected button - add error class to group and trip flag
					$('#group-dealType').addClass('error');
					$('.radio-dealType').addClass('btn-danger');
					flag = false;
				}
				// trip flag if no radio is selected
				if(!($('#fieldset-offer').find('.radio-discountType').is('.active'))) {
					// no selected button - add error class to group and trip flag
					$('#group-discountType').addClass('error');
					$('.radio-discountType').addClass('btn-danger');
					flag = false;
				}

				// validate whole form
				break;
		}

		// check each of the input boxes
		elems.each(function() {
			//console.log(this.name, this.value);
			//flag = levr.check[this.name](this.value) ? flag : false;

			if(levr.check[this.name](this.value) === false) {
				// field is not valid
				flag = false;
				//console.log(this.name, ": ", this.value, " is invalid");
			}
			//console.log(flag);
		})
		// ============ THIS SHOULD SHOW ALL THE DIVS BUT IT DOESN'T!!! GRRRR =============//
		if(flag === false && field === 'all') {
			// need to reveal form so that user can review
			alert('One or more fields is not valid. Please review your inputs.');

			//$('.accordion-body').removeClass('in');
			$('.accordion-body').not('#collapseSeven,#collapse0').addClass('in');
			$('#goTo2, #goTo3, #goTo4, #goTo5,#goTo6').addClass('hidden');

		}

		return flag;
	},
	makeGroupError : function(array) {
		// TODO MAKE THIS WORK
		// takes in an array of
		//console.log(array);
		for(var i = 0; i < array.length; i++) {
			//console.log(array[i]);
			var name = array[i];
			levr.check.makeError(name);
		}
	},
	data : new levr.formData()
};

levr.check = {
	emptyField : function() {
	},
	dealTag1 : function(value) {
		return isNaN(value) ? this.removeError('dealTag1') : this.makeError('dealTag1');
	},
	dealTag2 : function(value) {
		//return isNaN(value) ? this.removeError('dealTag2') : this.makeError('dealTag2');
		return true ? this.removeError('dealTag2') : this.makeError('dealTag2');
	},
	dealTag3 : function(value) {
		//return isNaN(value) ? this.removeError('dealTag3') : this.makeError('dealTag3');
		return true ? this.removeError('dealTag3') : this.makeError('dealTag3');
	},
	categoryTag : function(value) {
		return isNaN(value) ? this.removeError('categoryTag') : this.makeError('categoryTag');
	},
	categoryDescription : function(value) {
		return this.removeError('categoryDescription');
		//return isNaN(value) ? this.removeError('categoryDescription') : this.makeError('categoryDescription');
	},
	specificName : function(value) {
		return isNaN(value) ? this.removeError('specificName') : this.makeError('specificName');
	},
	specificTag : function(value) {
		return isNaN(value) ? this.removeError('specificTag') : this.makeError('specificTag');
	},
	specificDescription : function(value) {
		return this.removeError('specificDescription');
		//return isNaN(value) ? this.removeError('specificDescription') : this.makeError('specificDescription');
	},
	dealValue : function(value) {
		// should be number
		return (!isNaN(value) && value !== '' && value > 0) ? this.removeError('dealValue') : this.makeError('dealValue');
	},
	endValue : function(value) {
		// should be number
		return (!isNaN(value) && value !== '' && parseInt(value) === +value && +value <= +levr.credits && +value > 0) ? this.removeError('endValue') : this.makeError('endValue');
	},
	dealCity : function(value) {
		// should be string
		return isNaN(value) ? this.removeError('dealCity') : this.makeError('dealCity');
	},
	businessName : function(value) {
		// should be string
		return isNaN(value) ? this.removeError('businessName') : this.makeError('businessName');
	},
	address1 : function(value) {
		// should be string
		return isNaN(value) ? this.removeError('address1') : this.makeError('address1');
	},
	address2 : function(value) {
		// not sure what this should be
		return this.removeError('address2');
	},
	city : function(value) {
		// should be string
		return isNaN(value) ? this.removeError('city') : this.makeError('city');
	},
	zipCode : function(value) {
		return (!isNaN(value) && value.length === 5) ? this.removeError('zipCode') : this.makeError('zipCode');
	},
	state : function(value) {
		// should index into the array of states e.g. NH, MA
		value = value.toUpperCase();
		document.getElementById("text-state").value = value;
		if(value.length != 2) {
			// state code is not two letters
			this.makeError('state');
			return false;
		} else if(this.stateArray.indexOf(value) === -1) {
			// state abbreviation is not in state list
			this.makeError('state');
			return false;
		} else {
			// state passes validation
			this.removeError('state');
			return true;
		}
	},
	ownerName : function(value) {
		// should be string
		return isNaN(value) ? this.removeError('ownerName') : this.makeError('ownerName');
	},
	phone : function(value) {
		value = value.replace(/[^0-9]/g, '');
		$('#text-phone').val(value);
		return (value.length === 10 && value.substr(0, 3) !== '555' && value.substr(3, 3) !== '555') ? this.removeError('phone') : this.makeError('phone');
	},
	email : function(value) {
		if(/(.+)@(.+){2,}\.(.+){2,}/.test(value)) {
			//console.log(this)
			//ajax call to validate email
			var requestObj = {
				action : 'validateEmail',
				email : value
			}
			//console.log(requestObj);
			//////////JURY RIGGED
			//levr.check.removeError('email');
			//return true;
			///////////
			$.ajax({
				url : "./../php/newDeal.php",
				type : "POST",
				cache : false,
				data : JSON.stringify(requestObj),
				async : false,
				success : function(result) {
					try {
						result = JSON.parse(result);
					} catch(error) {
						//console.log(error);
					}

					//console.log(result);
					switch(result.success) {
						case 0:
							// email is NOT valid
							$('#error-email').html('<span class="help-inline" id="error-email">Email already in use. <a href="./login.html">Login</a></span>');
							levr.check.makeError('email');
							return false;
							break;
						case 1:
							//email is valid
							$('#error-email').html('<span class="help-inline" id="error-email">Please enter a valid email address</span>')
							levr.check.removeError('email');
							return true;
							break;
						default:
							//php echoed something it shouldnt have
							break;
					}
				},
				error : function(request, error) {
					//console.error(request, error);
				}
			})
			////console.log(phpEmail)
		} else {
			$('#error-email').html('<span class="help-inline" id="error-email">Please enter a valid email address</span>')
			////console.log('email format NOT OK')
			this.makeError('email');
			return false
		}
	},
	password : function(value) {
		var pw2 = document.getElementById("text-confirmPassword").value;
		if(value.length > 5) {
			// password is long enough - remove error
			var a = this.removeError('password');
			// check if passwords match
			if(!!pw2) {// keep the !! - it typecasts the value
				var b = this.confirmPassword(pw2);
			}
			return true;
		} else {
			// password doesnt match
			this.makeError('password');
			return false;
		}
	},
	confirmPassword : function(value) {
		var pw1 = document.getElementById("text-password").value;
		var pw2 = document.getElementById("text-confirmPassword").value;
		return (pw1 === pw2) ? this.removeError('confirmPassword') : this.makeError('confirmPassword');

	},
	makeError : function(name) {
		// grab id of inline error helptext
		var errorTextID = "#error-" + name;
		// grab id of the control group
		var controlGroupID = "#group-" + name;
		// add error class to control group
		$(controlGroupID).addClass("error");
		// show the error inline help text
		$(errorTextID).removeClass("hidden");
		// return false because the value doesn't pass
		// delete value from que
		levr.form.data.deleteValue(name);
		return false;
	},
	removeError : function(name) {
		// grab id of inline error helptext
		var errorTextID = "#error-" + name;
		// grab id of the control group
		var controlGroupID = "#group-" + name;
		// remove error class from control group
		$(controlGroupID).removeClass("error");
		// show the error inline help text
		$(errorTextID).addClass("hidden");
		// grab value
		var elemID = '#text-' + name;
		var value = $(elemID).val();

		// add key:value to the value que
		levr.form.data.addValue(name, value);
		// return true because the value passes

		// ==== dynamically populate review form ==== //
		// necessary for if send form fails
		if(name === 'sendEmails') {
			if($('#checkbox-sendEmails').is(':checked') == true) {
				$('#review-sendEmails').text('Yes');
			} else {
				$('#review-sendEmails').text('No');
			}
		} else if(name === 'endValue') {
			$('#creditsUsed').text(value);
		} else {
			// other things
			$('#review-dealTags').text($('#text-dealTag1').val() + ', ' + $('#text-dealTag2').val() + ', ' + $('#text-dealTag3').val());
			if(levr.nameType == 'itemName') {
				$('#review-nameType').text('Specific item');
			} else if(levr.nameType == 'category') {
				$('#review-nameType').text('Category');
			}
			$('#review-' + name).text(value);
		}
		return true;
	},
	stateArray : ['AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA', 'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'],
	catArray : ["Jeans","Shirts","Stockings","Socks","Shoes","Dresses","Skirts","Swimwear","Bathing suits","Shorts","Hoodies","Sweaters", "Watches","Jewelry","Earrings",
"Sandals","Flip-Flops","Leggings","Accessories","Men's Accessories","Women's Accessories","Pajamas","Jackets","Coats","T-Shirts","Blazers","Slippers","Denim","Underwear","Dinner","Pizza","Drinks","Doughnuts","Crepes","Sandwiches","Subs","Coffee","Bagels","Tea"]
}

//================================FORM STUFF======================//
//Posting functions

levr.loadCats = function() {
	var requestBody = {
		action : "getCategories"
	}
	// Pull from server
	$.ajax({
		url : "./../php/newDeal.php",
		type : "POST",
		cache : false,
		data : JSON.stringify(requestBody),
		success : function(result) {
			//console.info('Loading Categories: mySQL request success.');
			try {
				var data = JSON.parse(result);
				var cats = data.data.concat(levr.check.catArray);
				//console.log(cats);
				if(data.success === 1) {
					// set autocomplete
					$('.tagSelect').typeahead({
						source : cats
					});
				} else {
					//console.error('categories not loaded', data);
				}
			} catch(e) {
				//console.error(e);
			}

		},
		error : function() {
			//console.error('Get failed...Try again tomorrow.');
		}
	})
};

