$(function() {
    var TIME_BETWEEN = 30 * 1000; // ms
    var WARN_THRESHOLD = 95; // percent full
    var server = "";
    var t;
    var strip = /[^a-zA-Z0-9\-.:]/g;
    var seconds_between = Math.round(TIME_BETWEEN) / 1000;
    var seconds_between_plural = seconds_between === 1 ? "" : "s";
    function handleData(data) {        
        pct = 0;
        pl = "";
        down = true;
        nearMax = false;
        unknownData = false;
        docTitle = "MineCanary - " + server + " - ";
        if(data.error) {
            str = "There was an error!";
            docTitle += "error";
        } else {
            timeOffset = moment(data.reference_timestamp) - moment();

            motd = ""
            if(data.status == "up") {
                if(data.max_players <= 0) {
                    unknownData = true;
                    pct = 100;
                    pl = "???";
                } else {
                    pct = 100 * Math.min(data.players / data.max_players, 1);
                    nearMax = (pct >= 95);
                    pl = data.players + "/" + data.max_players;
                }
                pl = pl + " players";
                motd = " [" + data.motd + "]"
                down = false;
                docTitle += pl;
            } else {
                docTitle += "down";
            }

            lastChangeTime = moment(data.lastchange).add(timeOffset);
            lastCheckTime = moment(data.timestamp).add(timeOffset);
            
            str = "The server <tt>" + punycode.toUnicode(data.server) + "</tt>" + motd + " is <span class='status-" + data.status + "'>" + data.status + "</span>.";
            str += "<br />It has been " + data.status + " since <abbr class='timeago' title='" + lastChangeTime.format() + "'>" + lastChangeTime.calendar() + "</abbr>.";
            str += "<br />Last checked <abbr class='timeago' title='" + lastCheckTime.format() + "'>" + lastCheckTime.calendar() + "</abbr>.";
        }
        str += "<br />Status refreshes every " + seconds_between + " second" + seconds_between_plural + ".";
        $("#result").html(str);
        $("#num-players").text(pl);
        $("#player-meter").toggleClass("meter-down", down);
        $("#meter-bar").animate({"width": pct+"%"}, 500);
        $("#meter-bar").toggleClass("meter-warn", nearMax);
        $("#meter-bar").toggleClass("meter-unknown", unknownData);
        document.title = docTitle;
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
        input = punycode.toASCII($('input[name="server"]').val());
        server = input.replace(strip, "-");
        if(server.length > 0) {
            $.address.path("u/" + server);
            getData();
        }
        return false;
    });
    $.address.externalChange(function(event) {
        if (event.pathNames.length > 1 && event.pathNames[0] == "u") {
            clearTimeout(t);
            input = punycode.toASCII(event.pathNames[1]);
            server = input.replace(strip, "-");
            $('input[name="server"]').val(server);
            getData();
        }
    }); 
    jQuery("abbr.timeago").timeago();
    $("#spinner").hide();
    $('input[name="server"]').focus();
});