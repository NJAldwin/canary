Output
======

*NOTE*: If `players`, `max_players`, or `protocol_version` are not reported by the server, canary will report the value as `-1`.  If `server_version` is not reported by the server, canary will report the value as `""`.

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

```json
{
    "lastchange": "2012-04-17T16:21:04.732000+00:00", 
    "max_players": 100, 
    "motd": "Nerd.Nu", 
    "players": 38, 
    "server": "p.nerd.nu", 
    "status": "up", 
    "protocol_version": 49,
    "server_version": "1.4.5",
    "timestamp": "2012-04-17T16:21:14.435000+00:00", 
    "reference_timestamp": "2012-04-17T16:21:14.435000+00:00"
}
```

if down:
--------
* last time up
* timestamp of data
* reference timestamp of request

```json
{
    "lastchange": "2012-04-17T16:28:04.185000+00:00", 
    "server": "p.nerd.nu", 
    "status": "down", 
    "timestamp": "2012-04-17T16:21:14.435000+00:00", 
    "reference_timestamp": "2012-04-17T16:21:14.435000+00:00"
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
