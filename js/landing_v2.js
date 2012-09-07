function slide(position){
	//do stuff based on position
	if (position < width/3){
		slot = 1
	} else if (position > width*2/3){
		slot = 3
	} else{
		slot = 2
	}
	
	//console.log('Slot: '+slot)
	//console.log('globalSlot: '+globalSlot)
	
	
	if (slot !=globalSlot){
		//console.log('NOT EQUAL')
		if (slot==1){
			$('#img1').animate({'margin-left':'0px'})
			$('#textImg').animate({'margin-left':'0px'})
			globalSlot = 1
		} else if (slot==3){
			$('#img1').animate({'margin-left':'-508px'})
			$('#textImg').animate({'margin-left':'-800px'})
			globalSlot=3
		} else{
			$('#img1').animate({'margin-left':'-254px'})
			$('#textImg').animate({'margin-left':'-400px'})
			globalSlot=2
		}
	} else{
		//console.log('EQUAL')
	}
	
	
	
	
}

function animDone(){
	width = $(window).width()
	globalSlot = 3
	//bind mousemove handler
	$('body').mousemove(function(event){
		
		//console.log(event.pageX)
		slide(event.pageX)
		
	})
}

$(window).load(function(){
	var endTime = (new Date()).getTime();
    var millisecondsLoading = endTime - startTime;
	
	mixpanel.track("Desktop Landing Page Loaded",{"Load Time":millisecondsLoading})


	var delay = 1000;
	$('#img1').delay(delay).animate({'margin-left':'-254px'}).delay(delay).animate({'margin-left':'-508px'}).delay(delay)
	$('#textImg').delay(delay).animate({'margin-left':'-400px'}).delay(delay).animate({'margin-left':'-800px'}).delay(delay,animDone())
	
	//click listeners for votes
	$('.featureImg').click(function(event){
		var item = event.target.id;
		if ($('#'+item).attr('upvoted')=='true'){
			$('#'+item).css({'background-color': 'transparent'}).attr('src','../img/'+item+'.png').attr('upvoted','false')
		} else{
			$('#'+item).css({'background-color': 'rgba(79,167,93,0.43)'}).attr('src','../img/'+item+'_upvoted.png').attr('upvoted','true')
			mixpanel.track("Feature Vote",{"feature":item})
		}
		
		
	})
	
	//click listeners for beta request
	$('#requestBeta').click(function(event){
		$.post('/',{'email':$('#email').val()},function(){
			$('#requestBeta,#email').hide()
			$('#inviteRequested').show()
			mixpanel.track("Beta Request",{"email":$('#email').val()})
		})
	})
		
	
	
})