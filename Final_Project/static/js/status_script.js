function serverResponded( data ) {
    /*
    log the event data, so you can see what's going on.
    Shows up in the console on your browser. (Chrome: Tools > Developer Tools > Console)
    */
    console.log( data );

    /* check the server status, and report it on the screen */
    if ( data.servers ){
        for (var server in data.servers) {
            if ( server.online ) {
                $("#status ." + server + "_status").html("<font color='green'>ONLINE<font>");
                $("#status ." + server + "_ip").html(data.servers[server].ip);
                $("#status ." + server + "_cpu").html(data.servers[server].cpu + " %");
                $("#status ." + server + "_disk").html(data.servers[server].disk_usage + " %");
                $("#status ." + server + "_sent").html(data.servers[server].net_stats.bytes_sent);
                $("#status ." + server + "_received").html(data.servers[server].net_stats.bytes_recv);
                $("#status ." + server + "_error_in").html(data.servers[server].net_stats.errin);
                $("#status ." + server + "_error_out").html(data.servers[server].net_stats.errout);
                $("#status ." + server + "_drop_in").html(data.servers[server].net_stats.dropin);
                $("#status ." + server + "_drop_out").html(data.servers[server].net_stats.dropout);
            }
            else {
                $("#status ." + server + "_status").html("<font color='red'>OFFLINE<font>");
                $("#status ." + server + "_ip").html("N/A");
                $("#status ." + server + "_cpu").html("N/A");
                $("#status ." + server + "_disk").html("N/A");
                $("#status ." + server + "_sent").html("N/A");
                $("#status ." + server + "_received").html("N/A");
                $("#status ." + server + "_error_in").html("N/A");
                $("#status ." + server + "_error_out").html("N/A");
                $("#status ." + server + "_drop_in").html("N/A");
                $("#status ." + server + "_drop_out").html("N/A");
            }
        }
    }
    if ( data.backups ){
        for (var backup in data.backups) {
            console.log(backup)
            if ( backup.online ) {
                $("#status ." + backup + "_status").html("<font color='green'>ONLINE<font>");
                $("#status ." + backup + "_ip").html(data.servers[backup].ip);
                $("#status ." + backup + "_cpu").html(data.servers[backup].cpu + " %");
                $("#status ." + backup + "_disk").html(data.servers[backup].disk_usage + " %");
                $("#status ." + backup + "_sent").html(data.servers[backup].net_stats.bytes_sent);
                $("#status ." + backup + "_received").html(data.servers[backup].net_stats.bytes_recv);
                $("#status ." + backup + "_error_in").html(data.servers[backup].net_stats.errin);
                $("#status ." + backup + "_error_out").html(data.servers[backup].net_stats.errout);
                $("#status ." + backup + "_drop_in").html(data.servers[backup].net_stats.dropin);
                $("#status ." + backup + "_drop_out").html(data.servers[backup].net_stats.dropout);
            }
            else {
                $("#status ." + backup + "_status").html("<font color='red'>OFFLINE<font>");
                $("#status ." + backup + "_ip").html("N/A");
                $("#status ." + backup + "_cpu").html("N/A");
                $("#status ." + backup + "_disk").html("N/A");
                $("#status ." + backup + "_sent").html("N/A");
                $("#status ." + backup + "_received").html("N/A");
                $("#status ." + backup + "_error_in").html("N/A");
                $("#status ." + backup + "_error_out").html("N/A");
                $("#status ." + backup + "_drop_in").html("N/A");
                $("#status ." + backup + "_drop_out").html("N/A");
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