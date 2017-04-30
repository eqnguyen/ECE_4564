function serverResponded( data ) {
    /*
    log the event data, so you can see what's going on.
    Shows up in the console on your browser. (Chrome: Tools > Developer Tools > Console)
    */
    console.log( data );

    /* check the server status, and report it on the screen */
    if ( data.servers ){
        for (var i = 0; i < data.servers.length; i++) {
            if ( data.servers.rasdserver1.online ) {
                $("#status ." + data.servers[i].hostname + "_status").html("<font color='green'>ONLINE<font>");
                $("##status ." + data.servers[i].hostname + "_ip").html(data.servers[i].ip);
                $("#status ." + data.servers[i].hostname + "_cpu").html(data.servers[i].cpu + " %");
                $("#status ." + data.servers[i].hostname + "_disk").html(data.servers[i].disk_usage + " %");
                $("#status ." + data.servers[i].hostname + "_sent").html(data.servers[i].net_stats.bytes_sent);
                $("#status ." + data.servers[i].hostname + "_received").html(data.servers[i].net_stats.bytes_recv);
                $("#status ." + data.servers[i].hostname + "_error_in").html(data.servers[i].net_stats.errin);
                $("#status ." + data.servers[i].hostname + "_error_out").html(data.servers[i].net_stats.errout);
                $("#status ." + data.servers[i].hostname + "_drop_in").html(data.servers[i].net_stats.dropin);
                $("#status ." + data.servers[i].hostname + "_drop_out").html(data.servers[i].net_stats.dropout);
            }
            else {
                $("#status ." + data.servers[i].hostname + "_status").html("<font color='green'>OFFLINE<font>");
                $("##status ." + data.servers[i].hostname + "_ip").html("N/A");
                $("#status ." + data.servers[i].hostname + "_cpu").html("N/A");
                $("#status ." + data.servers[i].hostname + "_disk").html("N/A");
                $("#status ." + data.servers[i].hostname + "_sent").html("N/A");
                $("#status ." + data.servers[i].hostname + "_received").html("N/A");
                $("#status ." + data.servers[i].hostname + "_error_in").html("N/A");
                $("#status ." + data.servers[i].hostname + "_error_out").html("N/A");
                $("#status ." + data.servers[i].hostname + "_drop_in").html("N/A");
                $("#status ." + data.servers[i].hostname + "_drop_out").html("N/A");
            }
        }
    }
}

var dropdown = false;

$(document).ready( function() {
    /* get server ip address */
    ip = location.host;

    params = { op: "status" };
    $.getJSON( 'http://'+ ip + '/com' , params, serverResponded );

    /* handle the click event on the clickme */
    $("#request").click( function() {
        params = { op: "status" };
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

/* request status of servers every 10 seconds */
window.setInterval( function() {
    params = { op: "status" };
    $.getJSON( 'http://' + ip + '/com' , params, serverResponded );
}, 5000);