$(function() {
    var TIME_BETWEEN = 30 * 1000; // ms
    var server = "";
    var t;
    function getData() {
        $('a#golink').html("[...]");
        $.getJSON($SCRIPT_ROOT + '/s/' + server, {},
                  function(data) {
                      if(data.error) {
                          str = "there was an error!";
                      } else {
                          motd = ""
                          pl = ""
                          if(data.status == "up") {
                              pl = " (" + data.players + "/" + data.max_players + " players)";
                              motd = " [" + data.motd + "]"
                          }
                          
                          str = data.server + motd + " is <span class='status-" + data.status + "'>" + data.status + "</span>" + pl;
                          str += "<br />since <abbr class='timeago' title='" + data.lastchange + "'>" + data.lastchange + "</abbr>";
                          str += "<br />last checked <abbr class='timeago' title='" + data.timestamp + "'>" + data.timestamp + "</abbr>";
                      }
                      $("#result").html(str);
                      jQuery("abbr.timeago").timeago();
                      $('a#golink').html("[get info]");

                      t = setTimeout(getData, TIME_BETWEEN);
                  });
        return false;
    }

    $('a#golink').bind('click', function() {
        clearTimeout(t);
        server = $('input[name="server"]').val();
        getData();
    });
    jQuery("abbr.timeago").timeago();
});