$(function() {
    var TIME_BETWEEN = 30 * 1000; // ms
    var WARN_THRESHOLD = 95; // percent full
    var server = "";
    var t;
    var strip = /[^a-zA-Z0-9\-.:]/g;
    function handleData(data) {        
        pct = 0;
        pl = "";
        down = true;
        nearMax = false;
        if(data.error) {
            str = "there was an error!";
        } else {
            motd = ""
            if(data.status == "up") {
                pct = 100 * Math.min(data.players / data.max_players, 1);
                nearMax = (pct >= 95);
                pl = data.players + "/" + data.max_players + " players";
                motd = " [" + data.motd + "]"
                down = false;
            }
            
            str = "The server <tt>" + data.server + "</tt>" + motd + " is <span class='status-" + data.status + "'>" + data.status + "</span>.";
            str += "<br />It has been " + data.status + " since <abbr class='timeago' title='" + data.lastchange + "'>" + moment(data.lastchange).calendar() + "</abbr>.";
            str += "<br />Last checked <abbr class='timeago' title='" + data.timestamp + "'>" + moment(data.timestamp).calendar() + "</abbr>.";
        }
        $("#result").html(str);
        $("#num-players").text(pl);
        $("#player-meter").toggleClass("meter-down", down);
        $("#meter-bar").animate({"width": pct+"%"}, 500);
        $("#meter-bar").toggleClass("meter-warn", nearMax);
        jQuery("abbr.timeago").timeago();
        $("#spinner").hide();

        t = setTimeout(getData, TIME_BETWEEN);
    }
    function getData() {
        $("#spinner").show();
        $.getJSON($SCRIPT_ROOT + '/s/' + server, {}, handleData)
            .error(function(e, s, t) {
                handleData({error: s + ": " + t});
            });
    }

    $('form#frm').bind('submit', function(event) {
        event.preventDefault();
        clearTimeout(t);
        input = $('input[name="server"]').val();
        server = input.replace(strip, "-");
        $.address.path("u/" + server);
        getData();
        return false;
    });
    $.address.externalChange(function(event) {
        if (event.pathNames.length > 1 && event.pathNames[0] == "u") {
            clearTimeout(t);
            input = event.pathNames[1];
            server = input.replace(strip, "-");
            $('input[name="server"]').val(server);
            getData();
        }
    }); 
    jQuery("abbr.timeago").timeago();
    $("#spinner").hide();
});