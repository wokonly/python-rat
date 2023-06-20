# Python Remote Access Tool (RAT)

[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

Python Remote Access Tool (RAT) is a tool created by Wok forgor.xyz that allows remote access to a client system. This tool is designed to be used responsibly and ethically.

## Prerequisites

- Python 3.9 or later installed

## Usage

1. Open a port on your network. You can refer to this [video tutorial](https://youtu.be/DhxM9mglrag) for assistance.
2. Open the `server.py` and `client.py` files.
3. In `server.py`, go to line 108 and change `127.0.0.1` to your IP address. Also, change the port from `12345` to the port you opened.
4. In `client.py`, go to lines 356 and 357 and change `localhost` to your IP address. Again, update the port to the one you opened.
5. Build the executable:
   - Open a command prompt and navigate to the directory `C:\Users\Wok\example\Test`.
   - Run the following commands:
     ```
     pip install pyinstaller
     pyinstaller --onefile --noconsole client.py
     ```
   - The compiled `client.exe` will be available in the `dist` directory.

## Hosting the Server

If you cannot keep your PC on 24/7 or have an unstable Wi-Fi connection, it is recommended to use a VPS server to host the `server.py` file.

## Issues and Feedback

Please report any issues you encounter at [GitHub Issues](https://github.com/wokonly/python-rat/issues). You can also join the Discord server for feedback and assistance at [Discord](https://discord.gg/VAx9qUsfhw).

## Disclaimer

The Python Remote Access Tool (RAT) is provided as-is and without warranty. Use it responsibly and only with the appropriate consent. The creator and contributors of this tool are not responsible for any misuse or damage caused.
