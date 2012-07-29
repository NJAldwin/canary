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

def clean_server(server):
    """ Get the sanitized host and port """

    # add default port if necessary
    if server.find(":")<0:
        server = server + ":25565"

    (host,sep,port) = server.partition(":")
    host = safename.sub('-', host)[:MAX_DOMAIN_LEN].lower()
    port = safeport.sub('', port)

    return (host, port)

def filename(host, port):
    """ Get the filename corresponding to the server (may or may not exist) """

    # note this may still generate an error if running on windows
    # since windows has a 260-char path limit
    return os.path.join(settings.STORE_DIR, "%s(%s)" % (host, port))

def check(server):
    """ Get the status of the server in a dict --
    runs a check if data is nonexistent or stale."""

    needs = False # becomes True if data needs to be refreshed
    data = {'error':'no data'} # default data

    (host, port) = clean_server(server)
    server = host + ":" + port
    fname = filename(host, port)

    nowutc = datetime.now(tzutc())
    nowlocal = datetime.now(tzlocal())

    try:
        # load the old data if there is any
        f = open(fname, "r")
        data = json.load(f)
        f.close()

        # check staleness
        # (using default for timezone info, just in case, as old versions of canary weren't tz aware)
        last = dateutil.parser.parse(data["timestamp"], default=nowlocal)
        if (last + timedelta(seconds=settings.TIME_BETWEEN)) <= nowutc:
            needs = True

    except IOError:
        # file does not exist
        needs = True

    with filelock(fname + ".lock") as fl:
        # only acquire the lock if needs is True
        # if it's already locked, needs will become False
        needs = needs and fl.acquire()

        if needs:
            # needs a refresh

            s = {}
            try:
                s = get_info(host, int(port))
            except socket.timeout:
                # timeout -> empty dict
                pass
            except:
                # server problem -> empty dict
                pass

            ndata = {"timestamp": nowutc.isoformat(),
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
            data["reference_timestamp"] = nowutc.isoformat()
            f = open(fname, "w")
            json.dump(data, f)
            f.close()

            fl.release()

        # if the file is already locked
        # this will return the old data
        # or if it's a new server, the default data
        return data

class filelock:
    """ A primitive exclusive lock on a file. """

    def __init__(self, filename):
        self.filename = filename;
        self.fd = None
    
    def acquire(self):
        """ Non-blocking.  Returns True if lock successfully obtained, else False. """
        try:
            # may not work if using NFS<v3 on kernel<2.6
            self.fd = os.open(self.filename, os.O_CREAT|os.O_EXCL|os.O_RDWR)
            return True
        except OSError as e:
            self.fd = None
            return False

    def release(self):
        """ Releases the lock.  Returns True if lock released, False if no lock. """
        if not self.fd:
            return False
        try:
            os.close(self.fd)
            os.remove(self.filename)
            self.fd = None
            return True
        except OSError:
            self.fd = None
            return False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        self.release()
        self.fd = None
