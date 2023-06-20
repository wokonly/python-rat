##################################
#    Made by Wok / forgor.xyz    #
##################################

# Before using

You must have python installed 3.9 - latest

# How to use

First open a port on your network - https://youtu.be/DhxM9mglrag

Go into the code of server.py and client.py 

server.py - goto line 108 then change 127.0.0.1 to your IP address then change the port from 12345 to the port you opened
client.py - goto line 356 and 357 and change localhost to your IP address then change the port from 12345 to the port you opened

# How to build

Open command promt and enter in these commands

cmd> cd C:\Users\Wok\example\Test

pip install pyinstaller
or
py -m pip install pyinstaller

pyinstaller --onefile --noconsole client.py

Goto dist in the file location and client.exe will be there

# What to do

Run server.py and then get the user to run the client.exe / client.py

If you cant keep your pc on 24/7 and dont have stable wifi I would get a vps server to host the server.py

# Issues / Feedback

Please report issues at https://github.com/wokonly/python-rat/issues
Join the discord to report feedback or help! https://discord.gg/VAx9qUsfhw
