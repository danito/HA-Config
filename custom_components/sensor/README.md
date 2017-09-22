# Stib 
Brussels public transport 

## Install
copy stib.py to custom_components/sensor/

cunfiguration.yaml:

```yaml
sensor:
  - platform: stib
    station_ids:
      - 1234
      - 4567

```

##How to get the station_id of a stop?

open http://m.stib.be/api/getitinerary.php?line=xx&iti=y
xx = line number of one of the lines passing by your stop
y = 1 or 2  to get the one way or return trip

So http://m.stib.be/api/getitinerary.php?line=81&iti=1 will provide all the stops for the tram line 81 from Marius Renard to Montgomery and http://m.stib.be/api/getitinerary.php?line=81&iti=2 the return trip.

The result is a xml file with data for each stop:
```xml
<stop>
  <id>6113</id>
  <name>GERMOIR</name>
  <present>TRUE</present>
  <latitude>50.82995</latitude>
  <longitude>4.37983</longitude>
</stop>
```
Get the id for each stop you need and add them to your configuration.

For each line that passes you get a new sensor.stib\_[stopid]\_[stopname]\_[mode][line].

The state returns the waiting time for the next vehicles : 

```text
sensor.stib_6113_germoir_T81      1 (Montgomery) - 8 (Montgomery)
```

Other attributes are :
```json
{
  "Stop name": "Germoir",
  "Next departure": "1",
  "Next Destination": "Montgomery",
  "Upcoming departure": "8",
  "Upcoming Destination": "Montgomery",
  "line": "81",
  "Mode": "T",
  "friendly_name": "T81",
  "icon": "mdi:tram"
}
```


