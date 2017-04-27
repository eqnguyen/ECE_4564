function serverResponded( data ) {
    /*
    log the event data, so you can see what's going on.
    Shows up in the console on your browser. (Chrome: Tools > Developer Tools > Console)
    */
    console.log( data );

    /* check the server status, and report it on the screen */
    if ( data.servers.rasdserver1.online ) {
        $("#status .server_status_1").html("<font color='green'>ONLINE<font>");
        $("#status .server_cpu_1").html(data.servers.rasdserver1.cpu + " %");
        $("#status .server_disk_1").html(data.servers.rasdserver1.disk_usage + " %");
        $("#status .server_net_1").html(data.servers.rasdserver1.net_stats.bytes_recv);
    }
    else {
        $("#status .server_status_1").html("<font color='red'>OFFLINE<font>");
        $("#status .server_cpu_1").html("N/A");
        $("#status .server_disk_1").html("N/A");
        $("#status .server_net_1").html("N/A");
    }

    if ( data.servers.rasdserver2.online ) {
        $("#status .server_status_2").html("<font color='green'>ONLINE<font>");
        $("#status .server_cpu_2").html(data.servers.rasdserver2.cpu + " %");
        $("#status .server_disk_2").html(data.servers.rasdserver2.disk_usage + " %");
        $("#status .server_net_2").html(data.servers.rasdserver2.net_stats.bytes_recv);
    }
    else {
        $("#status .server_status_2").html("<font color='red'>OFFLINE<font>");
        $("#status .server_cpu_2").html("N/A");
        $("#status .server_disk_2").html("N/A");
        $("#status .server_net_2").html("N/A");
    }

    if ( data.backups.rasdbackup1.online ) {
        $("#status .backup_status_1").html("<font color='green'>ONLINE<font>");
        $("#status .backup_cpu_1").html(data.backups.rasdbackup1.cpu + " %");
        $("#status .backup_disk_1").html(data.backups.rasdbackup1.disk_usage + " %");
        $("#status .backup_net_1").html(data.backups.rasdbackup1.net_stats.bytes_recv);
    }
    else {
        $("#status .backup_status_1").html("<font color='red'>OFFLINE<font>");
        $("#status .backup_cpu_1").html("N/A");
        $("#status .backup_disk_1").html("N/A");
        $("#status .backup_net_1").html("N/A");
    }

    if ( data.backups.rasdbackup2.online ) {
        $("#status .backup_status_2").html("<font color='green'>ONLINE<font>");
        $("#status .backup_cpu_2").html(data.backups.rasdbackup2.cpu + " %");
        $("#status .backup_disk_2").html(data.backups.rasdbackup2.disk_usage + " %");
        $("#status .backup_net_2").html(data.backups.rasdbackup2.net_stats.bytes_recv);
    }
    else {
        $("#status .backup_status_2").html("<font color='red'>OFFLINE<font>");
        $("#status .backup_cpu_2").html("N/A");
        $("#status .backup_disk_2").html("N/A");
        $("#status .backup_net_2").html("N/A");
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