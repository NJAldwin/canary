$(function() {
    var TIME_BETWEEN = 30 * 1000; // ms
    var server = "";
    var t;
    function handleData(data) {        
        pct = 0;
        pl = "";
        down = true;
        if(data.error) {
            str = "there was an error!";
        } else {
            motd = ""
            if(data.status == "up") {
                pct = 100 * Math.min(data.players / data.max_players, 1);
                pl = data.players + "/" + data.max_players + " players";
                motd = " [" + data.motd + "]"
                down = false;
            }
            
            str = data.server + motd + " is <span class='status-" + data.status + "'>" + data.status + "</span>";
            str += "<br />since <abbr class='timeago' title='" + data.lastchange + "'>" + data.lastchange + "</abbr>";
            str += "<br />last checked <abbr class='timeago' title='" + data.timestamp + "'>" + data.timestamp + "</abbr>";
        }
        $("#result").html(str);
        $("#num-players").text(pl);
        $("#player-meter").toggleClass("meter-down", down);
        $("#meter-bar").animate({"width": pct+"%"}, 500);
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
        server = $('input[name="server"]').val();
        getData();
        return false;
    });
    jQuery("abbr.timeago").timeago();
    $("#spinner").hide();
});