 Canary
========

 What
------
Canary is a simple service to monitor a few stats about Minecraft servers.  Specifically, it keeps track of whether the server is down or up and how long it has been in that state as well as the MOTD and number of players.

 How
-----
First you'll need to grab the required `flask` and `python-dateutil` libraries:

    pip install -r requirements.txt

Right now, the simplest way to get Canary it running is to run

    python canary.py
    
and set up cron jobs to update the data for each server every so often by using `curl` (this ensures that the "how long" data is mostly accurate):

    curl http://localhost:5000/s/<server>

Then you can just point your browser at <http://localhost:5000/> and punch in the server to see the latest results (this will also trigger an update if there hasn't been one recently).

See the `settings.py` file for more tweaks.

 Why
-----
Why not?  It's useful to not have to open the Minecraft client to check on a server, plus it's nice to see how long the server has been down/up.

The name "canary" comes from the original status monitor--the canary in the coal mine.

 Who
-----
Created by Nick Aldwin.

In the spirit of giving credit where credit is due: the crucial Minecraft protocol code is based on [this gist](https://gist.github.com/1209061) by [Barney Gale](https://github.com/barneygale).
