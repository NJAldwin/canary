$(function() {
    $('a#golink').bind('click', function() {
        $.getJSON($SCRIPT_ROOT + '/s/' + $('input[name="server"]').val(), {},
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
                  });
        return false;
    });
    jQuery("abbr.timeago").timeago();
});