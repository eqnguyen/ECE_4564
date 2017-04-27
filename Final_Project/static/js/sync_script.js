function serverResponded( data ) {
    /*
    log the event data, so you can see what's going on.
    Shows up in the console on your browser. (Chrome: Tools > Developer Tools > Console)
    */
    console.log( data );

    /* check the server status, and report it on the screen */
    if ( data.client_list ) {
        $("#clients .client_list").html('');

        for (var i = 0; i < data.client_list.length; i++) {
            var ip = data.client_list[i]
            $("#clients .client_list").append(ip
                + "<form id='sync' name='" + ip + "' onsubmit='myFunction( event, this.name )'>"
                + " <input type='submit' value='Sync'>"
                + " <input type='radio' name='" + ip + "' value='Now' checked>Now"
                + " <input type='radio' name='" + ip + "' value='Later'>"
                + " <input id='datetime' type='datetime-local' name='" + ip + "'>"
                + " </form><br><br>");
        }
    }
}

function scheduleSync( event, client ) {
    var isValid = 0;
    var time = $("input[name='" + client + "']:checked").val();

    if ( time == "Now" ) {
        isValid = 1;
        console.log("Sync " + client + " " + time);
    } else if ($("#datetime[name='" + client + "'").val()) {
        isValid = 1;
        time = $("#datetime[name='" + client + "'").val();
        console.log("Sync " + client + " at " + $("#datetime[name='" + client + "'").val());
    } else {
        console.log("Date time is empty");
    }

    if (isValid) {
        payload = { client: client, time: time};
        $.post('http://' + ip + '/com/sync' , payload);
    }

    event.preventDefault();
}

var dropdown = false;

$(document).ready( function() {
    /* get server ip address */
    ip = location.host;

    /* handle the click event on the clickme */
    $("button#request").click( function() {
        params = { op: "clients" };
        $.getJSON( 'http://'+ ip + '/com' , params, serverResponded );
    });

    //Hamburger Menu show/hide
	$("#hamMenuPic").click(function() {
		if(dropdown == false){
			$(".navigation").css("display", "block");
			dropdown = true;
		} else {
			$(".navigation").css("display", "none");
			dropdown = false;
        }
	});

	//Hide Hamburger Menu if click outside of menu
	$("html").click(function(evt){
		if(evt.target.id == "dropdown" || evt.target.id == "menuBar")
			return;
	    //For descendants of menu_content being clicked
        if($(evt.target).closest("#dropdown").length)
            return;
        if($(evt.target).closest("#menuBar").length)
            return;
        //Do processing of click event here for every element except with id menu_content
        $(".navigation").css("display", "none");
        dropdown = false;
    });
});
