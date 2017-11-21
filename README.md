# HA-Config
my home-assistant.io config
## Hardware
- Raspberry PI 3 with HASSIO
- Yeelight white bulb
- Yeelight Color bulb
- TP-Link HS110
- Raspberry Zero W with Pimoroni Radio Kit (mpd)
- RFXcom
- RFLink Arduino
- Somfy cover
- Zwave.me ZME_UZB1
- Fibaro FGWPE-102 ZW5 EU
- Sony BraviaTV
- RPi Zero W with camera
- QNAP TS-212p

## Software
- Zanzito
- Node-Red

## Automations

- At 7:30 have tts.google_say the weather details for today (Wunderground).
- At 7:45 have tts say in how many minutes the next Bus is arriving at the stop.
- At 20:00 tell the kids it's bedtime
- Switch on the dimmed yeelight when the tv is set to on.
- Switch on a yeelight 1h before sunset.
- Send a message to Zanzito when the TV has been switched on/off (kids screen time control).
- Switch TV off after 2h of screen time on weekends.
- Take a picture every 15min.
- Switch RPiCam off/on if _nothome_ after 10 min (if wifi goes down and back up, it seems not to reconnect).
- GCAL: add the description of a gcal entry to the 7:30 morning message ("Don't forget that: ...")
- Send a payload with Zanzito to the mqtt broker to tts.google_say the time and distance for getting home.
- Send notification to Zanzito if Qnap is not home for more than 30 min. 
- Restart Qnap with TP-Link switch if mqtt topic received.
- RFLink: open Somfy cover at sunrise. Close Somfy cover at sunset (offset : 01:00:00)
- RFLink: Kerui door sensor for a Velux roof window. Send notification if windows is open/closed (WIP)

## Custom_components

- Stib : script to get Brussel's public transport data
- Zanzito notify : script to integrate zanito mqtt into hass notify.

## Pi camera
There's a construction site in front of my house and to make a timelapse of the works I taped a RPiZero on a window. Then I installed Node-Red to be able to receive and send  mqtt payloads.
