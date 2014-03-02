Output
======

Canary guarantees best-effort output in the format below for most servers.  It is written in an attempt to be as backwards-compatible as possible.

*NOTE*: If `players.online`, `players.max`, or `version.protocol` are not reported by the server, canary will report the value as `-1`.  If `version.name` is not reported by the server, canary will report the value as `""`.

if up
-----
* motd (HTML-escaped)
* number of players
* max # of players
* last time down (for uptime)
* server version (as string)
* protocol version (as int)
* timestamp of data
* reference timestamp of request
* minimum refresh interval (as int, in seconds)

```json
{
    "lastchange": "2012-04-17T16:21:04.732000+00:00",
    "description": {
        "text": "Nerd.Nu"
    },
    "players": {
        "max": 100,
        "online": 38
    },
    "server": "p.nerd.nu",
    "status": "up",
    "version": {
        "name": "1.4.5",
        "protocol": 49
    },
    "timestamp": "2012-04-17T16:21:14.435000+00:00",
    "reference_timestamp": "2012-04-17T16:21:14.435000+00:00",
    "min_refresh_interval": 60
}
```

if down:
--------
* last time up
* timestamp of data
* reference timestamp of request
* minimum refresh interval (as int, in seconds)

```json
{
    "lastchange": "2012-04-17T16:28:04.185000+00:00", 
    "server": "p.nerd.nu", 
    "status": "down", 
    "timestamp": "2012-04-17T16:21:14.435000+00:00", 
    "reference_timestamp": "2012-04-17T16:21:14.435000+00:00",
    "min_refresh_interval": 60
}
```

if error:
---------
* error

```json
{
    "error": "error message"
}
```
