var dropdown = false;

$(document).ready( function() {
    //Hamburger Menu show/hide
	$( '#hamMenuPic' ).click(function() {
		if(dropdown == false){
			$(".navigation").css("display", "block");
			dropdown = true;
		} else {
			$(".navigation").css("display", "none");
			dropdown = false;
        }
	});

	//Hide Hamburger Menu if click outside of menu
	$('html').click(function(evt){
		if(evt.target.id == "dropdown" || evt.target.id == "menuBar")
			return;
	    //For descendants of menu_content being clicked
        if($(evt.target).closest('#dropdown').length)
            return;
        if($(evt.target).closest('#menuBar').length)
            return;
        //Do processing of click event here for every element except with id menu_content
        $(".navigation").css("display", "none");
        dropdown = false;
    });
});
