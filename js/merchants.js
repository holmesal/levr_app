/**
 * @author Levr Inc.
 */

$('.navigation').click(function() {
	//This is the tab bar function that switches between tabs
	console.log(this.hash);
	//Hides the active div
	$('.active').hide().removeClass('active');
	//Shows the selected div
	$(this.hash).show().addClass('active');
	
})

$(document).ready(function() {
	
})