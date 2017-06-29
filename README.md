# OctoPrint-PanTilt-Nano

This plugin extends the plugin controlls developed by [Salandora](https://github.com/Salandora/OctoPrint-PanTilt) and adds support
for a simple and low cost 2 axis gimbal bracket.  The plugin uses the web cam controls (added through the Octoprint-PanTilt plugin) located on the
control tab.

This implementation uses an Arduino Nano as the controller for the gimbal.  The Nano
is controlled and powered through the USB port. This plugin has had very limited testing!!

## Setup

First, the base Octoprint-PanTilt plugin needs to be installed from here:
https://github.com/c-devine/OctoPrint-PanTilt/archive/command-handler.zip

see [command-handler topic](https://github.com/c-devine/OctoPrint-PanTilt/tree/command-handler)

Then install via the bundled [Plugin Manager](https://github.com/foosel/OctoPrint/wiki/Plugin:-Plugin-Manager)
or manually using this URL:

    https://github.com/c-devine/OctoPrint-PanTilt-Nano/archive/master.zip


## Video

[![PanTilt Nano Video](https://raw.githubusercontent.com/c-devine/OctoPrint-PanTilt-Nano/snapshots/assets/img/youtube.png?raw=true)](http://www.youtube.com/watch?v=r1rvIeMVfCk "PanTilt-Nano")


## Hardware

The 2 axis servo gimbals can be found on ebay and other [online](https://www.google.com/search?q=ebay+Servo+Mount+bracket+pan+tilt+with+servos&oq=ebay+Servo+Mount+bracket+pan+tilt+with+servos)
 locations.  [Arduino Nanos](https://www.google.com/#q=Arduino+Nano+compatible+v3.0+5v+ATmega328p) are also pretty easy to find.

3D Printed Part: [C270 Camera Mount Block](https://www.thingiverse.com/thing:2409919)

<img src="https://raw.githubusercontent.com/c-devine/OctoPrint-PanTilt-Nano/snapshots/assets/img/pantilt.png?raw=true" width="320" height="240">
<img src="https://raw.githubusercontent.com/c-devine/OctoPrint-PanTilt-Nano/snapshots/assets/img/webcam.png?raw=true" width="320" height="240">



## Firmware

The [Firmware](https://github.com/c-devine/OctoPrint-PanTilt-Nano-Firmware) is located here: https://github.com/c-devine/OctoPrint-PanTilt-Nano-Firmware.


## Configuration

The plugin is configured though the Setting Dialog -> PanTilt-Nano screen.  Select the Serial Port, and min max Us values -> Save.


<a href="https://raw.githubusercontent.com/c-devine/OctoPrint-PanTilt-Nano/snapshots/assets/img/settings.png?raw=true"><img src="https://raw.githubusercontent.com/c-devine/OctoPrint-PanTilt-Nano/snapshots/assets/img/settings.png?raw=true" width="493" height="403"></a>

