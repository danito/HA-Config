# HA-Config
my home-assistant.io config
## Hardware
- Raspberry PI 3 with HASSIO
- Yeelight white bulb
- Yeelight Color bulb
- TP-Link HS110
- Raspberry Zero W with Pimoroni Radio Kit (mpd)
- RFXcom
- Somfy cover
- Zwave.me ZME_UZB1
- Fibaro FGWPE-102 ZW5 EU
- Sony BraviaTV
- RPi Zero W with camera

## Software
- Zanzito
- Node-Red

## Automations

- At 7:30 have tts.google_say the weather details for today (Wunderground)
- At 20:00 tell the kids it's bedtime
- Switch on the dimmed yeelight when the tv is set to on.
- Switch on a yeelight 1h before sunset.
- Send a message to Zanzito when the TV has been switched off (kids screen time control)
- Switch TV off after 2h of screen time
- Take a picture every 15min.
- Switch RPiCam off/on if _not_home after 10 min (if wifi goes down and back up, it seems not to reconnect).

## Custom_components

- Stib : script to get Brussel's public transport data
- Zanzito notify : script to integrate zanito mqtt into hass notify.

## Pi camera
There's a construction site in front of my house and to make a timelapse of the works I taped a RPiZero on a window. I installed Node-Red to be able to receive mqtt payloads from HA.
