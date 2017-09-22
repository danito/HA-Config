#########################################################################################
# Stib Sensor
# 
# To obtain stop id visit http://m.stib.be/api/getitinerary.php?line=54&iti=1
# replace line=xx with a line number passing by your stop
# replace iti=2 to obtain the return trip
#########################################################################################

import logging
import re
from datetime import datetime, timedelta
import requests
#import xmldict
from lxml import etree as ET
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
from homeassistant.helpers.entity import Entity
from homeassistant.util import Throttle
from homeassistant.const import CONF_NAME, ATTR_ATTRIBUTION, STATE_UNKNOWN
import homeassistant.helpers.config_validation as cv

_LOGGER = logging.getLogger(__name__)

_RESOURCE = 'http://m.stib.be/api/getwaitingtimes.php'

ATTR_NEXT = 'Next departure'
ATTR_UPCOMING = 'Upcoming departure'
ATTR_STOPNAME = 'Stop name'
ATTR_DESTINATION = 'Next Destination'
ATTR_UPCOMING_DESTINATION = 'Upcoming Destination'
ATTR_MODE = 'Mode'
ATTR_LINE_ID = 'line'
ATTR_ATTRIBUTION = 'Data provided by api.stib.be'


ICON = 'mdi:bus'
CONF_STOP_LIST = 'station_ids'
SCAN_INTERVAL = timedelta(seconds=30)
DEFAULT_NAME = 'STIB'

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({
    vol.Optional(CONF_NAME, default=DEFAULT_NAME): cv.string,
    vol.Optional(CONF_STOP_LIST, 'station_filter'):
            vol.All(
                cv.ensure_list,
                vol.Length(min=1),
                [cv.string])
})


def setup_platform(hass, config, add_devices, discovery_info=None):
    sensors = []
    stations_list = set(config.get(CONF_STOP_LIST, []))
    url = _RESOURCE
    interval = SCAN_INTERVAL
    for station in stations_list:
       d = StibData(station)
       d.update()
       data = d.stop_data
       lines = data['lines']
       stop_name = data["stop_name"][0].replace("-", "_").replace(" ","_")
       for l in lines:
           line = lines[l][0]['line']
           sensors.append(StibSensor(station, line, d, stop_name))
    
    add_devices(sensors, True)


class StibSensor(Entity):
    def __init__(self, stop, line, data, name):
        self._stop = stop
        self._line = line
        self._name = name
        self._data = data
        self._stop_name = None
        self._destination = None
        self._state = STATE_UNKNOWN
        self._next = None
        self._upcoming = None
        self._upcoming_destination = None
        self._lines = None
        self._mode = None
        self._line_id = None

    @property
    def name(self):
        return self._name

    @property
    def state(self):
        return self._state

    @property
    def device_state_attributes(self):
        if self._data is not None:
            return {
                    ATTR_STOPNAME: self._stop_name,
                    ATTR_NEXT: self._next,
                    ATTR_DESTINATION: self._destination,
                    ATTR_UPCOMING: self._upcoming,
                    ATTR_UPCOMING_DESTINATION: self._upcoming_destination,
                    ATTR_LINE_ID: self._line_id,
                    ATTR_MODE: self._mode,
                    }
    @property
    def icon(self):
        if self._mode is not None:
            if self._mode == 'B':
                return 'mdi:bus'
            if self._mode == 'T':
                return 'mdi:tram'
            if self.mode == 'M':
                return 'mdi:subway'
        return ICON


    def update(self):
        self._data.update()
        stop_data = self._data.stop_data
        line = 'line_' + str(self._line)
        minutes = -1
        t = []
        d = {}
        state = ""
        other_lines = []
        if stop_data is not None:
            lines = stop_data['lines']
            self._stop_name = stop_data['stop_name']
            for o_line in lines:
                all_line_id = lines[o_line][0]['mode'] + lines[o_line][0]['line']
                other_lines.append(all_line_id)
            self._lines = other_lines
            if line in lines:
                for l in lines[line]:
                    m = lines[line][l]['minutes']
                    t.append(m)
                    d[m] = lines[line][l]['destination']
                    line_id = lines[line][l]['line']
                    self._mode  = lines[line][l]['mode']
            else:
                _LOGGER.info("Line %s doesn't stop at stop %s. Check your line number",self._line, self._stop_name)
            if len(t) is not 0:
                minutes = max(t)         
                self._next = min(t)
                self._upcoming = max(t)
                self._line_id = line_id
                self._destination = d[minutes].title()
                self._upcoming_destination = d[self._upcoming].title()
                self._name = "stib " + self._stop + " " + self._stop_name + " " + self._mode + line_id
                state = self._next + " (" + self._destination + ")"
                if len(t) == 2:
                    state = state + " - " + self._upcoming + " (" + self._upcoming_destination + ")"
            
        if minutes == -1:
            self._state  = STATE_UNKNOWN
        else: 
            self._state = state



class StibData(object):
    def __init__(self, stop):
        self.stop = stop
        self.stop_data = {}

    def update(self):
        response = requests.get(_RESOURCE, params  = {'halt': self.stop})
        stop_waiting_times = {}
        stop_name = "n/a"
        if response.status_code == 200:
           r_xml = response.content
           r_tree = ET.XML(r_xml)
           stop_name = r_tree.xpath('/waitingtimes/stopname/text()')
           stop_name = stop_name[0]
           if stop_name == "":
               _LOGGER.error("STIB Wrong stopID, check %s", result.url)
            
           stop_waiting_times['stop_name'] = stop_name
           stop_waiting_times['lines'] = {}
           for wt in r_tree.xpath('/waitingtimes/waitingtime'):
               l = '0'
               wt_tmp = {}
               for c in wt.getchildren():
                   if c.tag == 'line':
                       l = c.text
                   wt_tmp[c.tag] = c.text
               l_key = 'line_' + l
               l_idx = 0
               if l_key in stop_waiting_times['lines']:
                   l_idx = len(stop_waiting_times['lines'][l_key])
               else:
                   stop_waiting_times['lines'][l_key] = {}
                   stop_waiting_times['lines'][l_key][l_idx] = {}
               stop_waiting_times['lines'][l_key][l_idx] = wt_tmp  #'lines': {'line_54':{0:{'line':54, 'minutes' : 11, ...}}}
        else:
            _LOGGER.error("Impossible to get data from STIB api. Response code: %s. Check %s", response.status_code, response.url)
            stop_waiting_times = None

        self.stop_data = stop_waiting_times 
