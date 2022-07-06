Happy Lighting
==============

Provides a basic BLE interface to LED light strips which use a Bluetooth interface controlled by the "LED LAMP" app (<a href="https://play.google.com/store/apps/details?id=com.ledble&gl=US">Android</a>; <a href="https://apps.apple.com/us/app/led-ble/id1072007734">iOS</a>)

Requires bleak (python3 -m venv; source venv/bin/activate; pip install -r requirements.txt)

Usage
-----

    python3 funtime.py --scan

From this identify the BLE device which looks like your LED lights, called something like `LEDBLE-000D5C`. These things
don't require pairing, entertainingly. Note the MAC address and use it in subsequent commands, like:

    python3 funtime.py --device C0:00:00:00:0D:5C --rgb 55ee55

Commands
--------

`--rgb RRGGBB`: Set the RGB value

`--brightness B`: Set brightness to a value between 0 and 100

`--off`: Turn the lights off

`--on`: Turn the lights on

`--rgbinteractive`: Enter a mode where you can repeatedly enter colour values for rapid testing or scripting.


