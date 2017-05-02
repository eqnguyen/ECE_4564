function serverResponded( data ) {
    /*
    log the event data, so you can see what's going on.
    Shows up in the console on your browser. (Chrome: Tools > Developer Tools > Console)
    */
    console.log( data );

    /* check the server status, and report it on the screen */
    if ( data ) {
        $("#status").html('');
        for ( var server in data.servers ) {
            var node = data.servers[server];

            if ( node.online ) {
                $("#status").append(
                    "<b><u>" + server + ":</u></b> <font color='green'>ONLINE</font> - " + node.ip + "<br><br>"
                    + "CPU: " + node.cpu + "<br>"
                    + "Disk Usage: " + node.disk_usage + "<br>"
                    + "Bytes Sent: " + node.net_stats.bytes_sent + "<br>"
                    + "Bytes Received: " + node.net_stats.bytes_recv + "<br>"
                    + "Error In: " + node.net_stats.errin
                    + "Error Out: " + node.net_stats.errout + "<br>"
                    + "Drop In: " + node.net_stats.dropin
                    + "Drop Out: " + node.net_stats.dropout + "<br><br>"
                )
            } else {
                $("#status").append(
                    "<b><u>" + server + ":</u></b> <font color='red'>OFFLINE</font><br><br>"
                    + "CPU: N/A<br>"
                    + "Disk Usage: N/A<br>"
                    + "Bytes Sent: N/A<br>"
                    + "Bytes Received: N/A<br>"
                    + "Error In: N/A"
                    + "Error Out: N/A<br>"
                    + "Drop In: N/A"
                    + "Drop Out: N/A<br><br>"
                )
            }
        }
        for ( var backup in data.backups ) {
            var node = data.servers[server];

            if ( node.online ) {
                $("#status").append(
                    "<b><u>" + backup + ":</u></b> <font color='green'>ONLINE</font> - " + node.ip + "<br><br>"
                    + "CPU: " + node.cpu + "<br>"
                    + "Disk Usage: " + node.disk_usage + "<br>"
                    + "Bytes Sent: " + node.net_stats.bytes_sent + "<br>"
                    + "Bytes Received: " + node.net_stats.bytes_recv + "<br>"
                    + "Error In: " + node.net_stats.errin
                    + "Error Out: " + node.net_stats.errout + "<br>"
                    + "Drop In: " + node.net_stats.dropin
                    + "Drop Out: " + node.net_stats.dropout + "<br><br>"
                )
            } else {
                $("#status").append(
                    "<b><u>" + backup + ":</u></b> <font color='red'>OFFLINE</font><br><br>"
                    + "CPU: N/A<br>"
                    + "Disk Usage: N/A<br>"
                    + "Bytes Sent: N/A<br>"
                    + "Bytes Received: N/A<br>"
                    + "Error In: N/A"
                    + "Error Out: N/A<br>"
                    + "Drop In: N/A"
                    + "Drop Out: N/A<br><br>"
                )
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
