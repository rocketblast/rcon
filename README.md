rcon
====
rcon is a Python library for interaction with game servers.

Supported games today are Battlefield: Bad Company 2, Battlefield 3, Medal of Honor, Battlefield 4, Battlefield: Hardline.

Examples
--------

```
from rocketblast.rcon import FrostbiteClient as Client

client = Client('192.0.0.1', 47200, 'secret')
serverinfo = client.send(['serverinfo'])
print serverinfo
```
This example will connect to a server, run the command `serverinfo` and print the result. You will get an array back with the result.

```
from rocketblast.rcon import FormatFrostbiteClient as Client

client = Client('192.0.0.1', 47200, 'secret')
serverinfo = client.send(['serverinfo'])
print client.serverinfo(serverinfo)
```
This example does the same as the first one, except that it attempts to parse the result into a `dict`.

Installation
------------
The easiest way to get started is to download the source and then run the following command:
```
python setup.py install
```

Contribute
----------
The purpose of this repository is to continue to evolve rcon core, making it easier to use and support more games. If you are interested in helping with that feel free to contribute and give feedback.

=== License 
rcon is GNU Affero GPL v3. 
