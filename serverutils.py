import os
import socket
import settings
import dateutil.parser
from dateutil.tz import *
import json
from datetime import datetime, timedelta
import re

__all__ = ['filename', 'check']

safename = re.compile(r'[^a-zA-Z0-9\-.]')
safeport = re.compile(r'[^0-9]')
safemotd = re.compile(r'[^a-zA-Z0-9\-+&@#\/%\?=~_|!:,\.;\(\) ]')

MAX_DOMAIN_LEN = 255

def get_info(host, port):
    """ Get information about a Minecraft server """
    # inspired from
    # https://gist.github.com/1209061
    # http://www.wiki.vg/Protocol#Server_List_Ping_.280xFE.29

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.settimeout(settings.TIMEOUT)
    s.connect((host, port))
    
    s.send('\xfe')
    d = s.recv(256)
    s.close()
    assert d[0] == '\xff'
    
    d = d[3:].decode('utf-16be').split(u'\xa7')
    
    return {'motd':        safemotd.sub(".", d[0]),
            'players':     int(d[1]),
            'max_players': int(d[2])}

def filename(server):
    """ Get the filename corresponding to the server (may or may not exist)
    Note that the server name should include the port """

    # note this may still generate an error if running on windows
    # since windows has a 260-char path limit
    (host,sep,port) = server.partition(":")
    host = safename.sub('-', host)[:MAX_DOMAIN_LEN]
    port = safeport.sub('', port)
    return os.path.join(settings.STORE_DIR, "%s(%s)" % (host, port))

def check(server):
    """ Get the status of the server in a dict --
    runs a check if data is nonexistent or stale."""

    if not os.path.exists(settings.STORE_DIR):
        os.mkdir(settings.STORE_DIR)

    # add default port if necessary
    if server.find(":")<0:
        server = server + ":25565"

    needs = False # becomes True if data needs to be refreshed
    data = {}

    try:
        # load the old data if there is any
        f = open(filename(server), "r")
        data = json.load(f)
        f.close()

        # check staleness
        # (using default for timezone info, just in case, as old versions of canary weren't tz aware)
        last = dateutil.parser.parse(data["timestamp"], default=datetime.now(tzlocal()))
        if (last + timedelta(seconds=settings.TIME_BETWEEN)) <= datetime.now(tzutc()):
            needs = True

    except IOError:
        # file does not exist
        needs = True

    if needs:
        # needs a refresh

        s = {}
        try:
            (host,sep,port) = server.partition(":")
            s = get_info(host, int(port))
        except socket.timeout:
            # timeout -> empty dict
            pass
        except:
            # server problem -> empty dict
            pass

        ndata = {"timestamp": datetime.now(tzutc()).isoformat(),
                 "server":    server}

        if len(s)>0:
            ndata["status"]      = "up"
            ndata["motd"]        = s["motd"]
            ndata["players"]     = s["players"]
            ndata["max_players"] = s["max_players"]
        else:
            ndata["status"]      = "down"

        # set time of last change
        ndata["lastchange"]      = ndata["timestamp"]
        if "status" in data and data["status"] == ndata["status"] and "lastchange" in data:
            # status hasn't changed
            ndata["lastchange"]  = data["lastchange"]

        # dump new data
        data = ndata
        f = open(filename(server), "w")
        json.dump(data, f)
        f.close()

    return data
