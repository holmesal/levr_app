function slideOver(id_out,id_in,pause){
	$('#'+id_out).delay(pause).animate({marginLeft: '-=282'})
	$('#'+id_in).delay(pause).animate({marginLeft: '-=282'})
	return true;
}

function mapMouse(){
	$(document).mousemove(function(e){
		switch (true){
			case ((e.pageX>=0) && (e.pageX<=200)):
				//put element one on the right
				$('img2').css('margin-left','-141px')
				//show out the first image
				$('#img2').animate({marginLeft: '-282px'})
				
			case ((e.pageX>=220) && (e.pageX<=400)):
				//put element one on the right
				$('img3').css('margin-left','-141px')
				//show out the first image
				$('#img3').animate({marginLeft: '-282px'})
			default:
				console.log((e.pageX>=0) && (e.pageX<=100))
		}
	});
}

function mapHover(){
	$('#left1').mouseenter(function(){
		$('#img1,#img3,#img4,#background2').animate({opacity: 0},200)
		$('#img2').css('margin-left','-141px').animate({opacity: 1},200)
		$('#background1').animate({opacity: 0.2})
	})
	
	$('#left2').mouseenter(function(){
		$('#img1,#img2,#img4,#background1').animate({opacity: 0},200)
		$('#img3').css('margin-left','-141px').animate({opacity: 1},200)
		$('#background2').animate({opacity: 0.2})
	})
	
	$('#right').mouseenter(function(){
		$('#img1,#img2,#img3').animate({opacity: 0},200)
		$('#img4').css('margin-left','-141px').animate({opacity: 1},200)
		$('#background1,#background2').animate({opacity: 0})
	})
}

$(document).ready(function() {
	$('#containerbg1,#img1').animate({opacity: 1},function(){
		$('#loading').animate({opacity: 0.75})
		//show images hidden during loading
		$('#containerbg2').css('visibility','visible')
		$('#img2,#img3,#img4').show()
	})
	
});

$(window).load(function() {
	
	//set element opacities and remove hidden divs
	$('.left1,.left2').css('opacity',0)
	$('#left').css('opacity',1)
	
	

	var init_pause = 500
	var pause = 2000
	
	//fade in the first image
	$('#loading').delay(500).animate({opacity: 0},function(){
		//show out the first image
		$('#img1').delay(init_pause).animate({marginLeft: '-=282'})
		//show in the second text
		$('.left1').delay(init_pause).animate({opacity: 1})
		//show in the second image
		$('#img2').delay(init_pause).animate({marginLeft: '-=282'},function(){
			//hide everything
			$('#img1,#img3,#img4').css('opacity',0)
			$('#containerbg1').css({'visibility':'hidden'})
			//fade in background
			$('#background1').animate({opacity: 0.2},1000)
			//fade out the background
			$('#background1').delay(pause).animate({opacity: 0},function(){
				//show white block again
				$('#containerbg1').css({'visibility':'visible'})
				//show out the second image
				$('#img2').animate({marginLeft: '-=282'})
				//show in the third text
				$('.left2').animate({opacity: 1})
				//show in the third image
				$('#img3').css({opacity: 1}).animate({marginLeft: '-=282'},function(){
					//hide everything
					$('#img1,#img2,#img4').css('opacity',0)
					$('#containerbg1').css({'visibility':'hidden'})
					//fade in background
					$('#background2').animate({opacity: 0.2},1000)
					//fade out the background
					$('#background2').delay(pause).animate({opacity: 0},function(){
						//show white block again
						$('#containerbg1').css({'visibility':'visible'})
						//show out the third image
						$('#img3').animate({marginLeft: '-=282'})
						//show in the fourth text
						$('#right').animate({opacity: 1})
						//show in the fourth image
						$('#img4').css({opacity: 1}).animate({marginLeft: '-=282'},function(){
							//hide everything left over
							$('#img3').css({opacity: 0})
							$('#containerbg1').css({'visibility':'hidden'})
							mapHover();
						})
					})
					
				})
			})
			
			
		})
	})
	
	/*$('#img1').delay(pause).animate({opacity: 1},function(){
		slideOver('img1','img2',function(){console.log('callback')})
		})*/
	
	
});