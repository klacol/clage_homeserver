import json
from unittest import (TestCase, mock)

from functools import partial, reduce
get_value_from_dict = partial(reduce, lambda d, k: d[k])

from clage_homeserver import ClageHomeServerMapper

SAMPLE_API_STATUS_RESPONSE = {
    "version": "1.4",
    "error": 0,
    "time": 1631263211,
    "success": True,
    "cached": True,
    "devices": [
        {
            "id": "2049DB0CD7",
            "busId": 1,
            "name": "",
            "connected": True,
            "signal": -72,
            "rssi": 0,
            "lqi": 0,
            "status": {
                "setpoint": 600,
                "tLimit": 0,
                "tIn": 229,
                "tOut": 188,
                "tP1": 0,
                "tP2": 0,
                "tP3": 0,
                "tP4": 0,
                "flow": 0,
                "flowMax": 250,
                "valvePos": 34,
                "valveFlags": 0,
                "power": 0,
                "powerMax": 140,
                "power100": 0,
                "fillingLeft": 0,
                "flags": 1,
                "sysFlags": 0,
                "error": 0
            }
        }
    ]
}

SAMPLE_REQUEST_STATUS_RESPONSE = {}

class TestClageHomeServerMapper(TestCase):

    def __nested_set(self, dic, keys, value):
        for key in keys[:-1]:
            if (type(key) == int):
              dic = dic[key]
            else:
              dic = dic.setdefault(key, {})
        dic[keys[-1]] = value

    def __helper_get_mapped_key(self, keys, value):
        apiResponse = dict(SAMPLE_API_STATUS_RESPONSE)
        self.__nested_set(apiResponse,keys,value)
        return ClageHomeServerMapper().mapApiStatusResponse(apiResponse)

    def test_map_homeserver_version(self):
        self.assertEqual(self.__helper_get_mapped_key(['version'], '1.4').get('homeserver_version'),'1.4')
        self.assertEqual(self.__helper_get_mapped_key(['version'], '1.xxx').get('homeserver_version'),'unknown')

    def test_map_homeserver_error(self):
        self.assertEqual(self.__helper_get_mapped_key(['error'], 0).get('homeserver_error'),'OK')
        self.assertEqual(self.__helper_get_mapped_key(['error'], 1).get('homeserver_error'),'Known, but not documented')
        self.assertEqual(self.__helper_get_mapped_key(['error'], 3).get('homeserver_error'),'Known, but not documented')
        self.assertEqual(self.__helper_get_mapped_key(['error'], 8).get('homeserver_error'),'Known, but not documented')
        self.assertEqual(self.__helper_get_mapped_key(['error'], 10).get('homeserver_error'),'Known, but not documented')
        self.assertEqual(self.__helper_get_mapped_key(['error'], 999).get('homeserver_error'),'unknown')

    def test_map_homeserver_success(self):
        self.assertEqual(self.__helper_get_mapped_key(['success'], True).get('homeserver_success'),True)

    def test_map_homeserver_time(self):
        self.assertEqual("2021-09-10 08:40:11", self.__helper_get_mapped_key('time', 1631263211).get('homeserver_time'))

    def test_map_heater_setpoint(self):
        self.assertEqual(self.__helper_get_mapped_key(['devices',0,'status','setpoint'],333).get('heater_status_setpoint'),33.3)

    def test_map_heater_connected(self):
        self.assertEqual(self.__helper_get_mapped_key(['connected'], True).get('heater_connected'),True)
        
    





    