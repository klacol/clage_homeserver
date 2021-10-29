from unittest import (TestCase, mock)
TestCase.maxDiff = None
from clage_homeserver import (ClageHomeServer)
from clage_homeserver.clage_homeserver import (ClageHomeServerMapper)
import requests


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
            "name": "NameOfMyHeater",
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

SAMPLE_REQUEST_STATUS_RESPONSE = {
    "homeserver_version": "1.4",
    "homeserver_error": "OK",
    "homeserver_time": "2021-09-10 08:40:11",
    "homeserver_success": True,
    "homeserver_cached": True,
    "heater_id": "2049DB0CD7",
    "heater_busId": 1,
    "heater_name": "NameOfMyHeater",
    "heater_connected": True,
    "heater_signal": -72,
    "heater_rssi": 0,
    "heater_lqi": 0,
    "heater_status_setpoint": 60,
    "heater_status_tIn": 22.9,
    "heater_status_tOut": 18.8,
    "heater_status_tP1": 0.0,
    "heater_status_tP2": 0.0,
    "heater_status_tP3": 0.0,
    "heater_status_tP4": 0.0,
    "heater_status_flow": 0.0,
    "heater_status_flowMax": 25.0,
    "heater_status_valvePos": 34,
    "heater_status_valveFlags": 0,
    "heater_status_power": 0.0,
    "heater_status_powerMax": 140.0,
    "heater_status_power100": 0.0,
    "heater_status_fillingLeft": 0,
    "heater_status_flags": 1,
    "heater_status_sysFlags": 0,
    "heater_status_error": "OK"
}

SAMPLE_REQUEST_STATUS_RESPONSE_UNAVAIL = {}

def helper_create_instance_without_host():
    return ClageHomeServer(None,None,None)

def helper_setButtonCurrentValue_ValueError():
    return ClageHomeServer('192.168.0.78','F8F005DB0CD7','2049DB0CD7').setButtonCurrentValue(0,6)

def helper_setAccessType_ValueError():
    return ClageHomeServer('192.168.0.78','F8F005DB0CD7','2049DB0CD7').setAccessType(1111)

def helper_setCableLockMode_ValueError():
    return ClageHomeServer('192.168.0.78','F8F005DB0CD7','2049DB0CD7').setCableLockMode(1111)

def mocked_request_status(*args, **kwargs):
    class MockResponse:
        def __init__(self, status_code, response):
            self._response = response
            self.status_code = status_code

        def json(self):
            return self._response

    if args[0] == 'https://192.168.0.78/devices/status/2049DB0CD7':
        return MockResponse(200, SAMPLE_API_STATUS_RESPONSE)
    return MockResponse(404, None)

def mocked_temperature_payload(*args, **kwargs):
    class MockResponse:
        def __init__(self, status_code, response):
            self._response = response
            self.status_code = status_code

        def json(self):
            return self._response

    if args[0] == 'https://192.168.0.78/devices/status/2049DB0CD7':
        return MockResponse(200, SAMPLE_API_STATUS_RESPONSE)
    return MockResponse(404, None)

class TestClageHomeserver(TestCase):

    def test_create_without_host(self):
        self.assertRaises(ValueError, helper_create_instance_without_host)

    def test_create_with_host(self):
        self.assertIsNotNone(ClageHomeServer('192.168.0.78','F8F005DB0CD7','2049DB0CD7'))

    @mock.patch('requests.get', side_effect=mocked_request_status)
    def test_requestStatus(self, mock_get):
        clageHomeServer = ClageHomeServer('192.168.0.78','F8F005DB0CD7','2049DB0CD7') 
        status = clageHomeServer.requestStatus()
        self.assertEqual(SAMPLE_REQUEST_STATUS_RESPONSE, status)

    # @mock.patch('requests.put')
    # def test_setTemperature(self, mock_put):
    #     response = ClageHomeServer('192.168.0.78','F8F005DB0CD7','2049DB0CD7').setTemperature(45)
    #     url = "https://192.168.0.78/devices/setpoint/2049DB0CD7"
    #     body = {'data': 450, 'cid': '1'}
    #     mock_put.assert_called_once_with(url=url, auth=("appuser","smart"), data=body, timeout=5, verify=False)
    #     self.assertIsNotNone(response)

    # @mock.patch('requests.get', side_effect=mocked_request_status)
    # def test_setAllowChargingFalse(self, mock_get):
    #     response = ClageHomeServer('192.168.0.78','F8F005DB0CD7','2049DB0CD7').setAllowCharging(False)
    #     mock_get.assert_called_once_with('192.168.0.78/mqtt?payload=alw=0')
    #     self.assertIsNotNone(response)

    # @mock.patch('requests.get', side_effect=mocked_request_status)
    # def test_setAutoStopTrue(self, mock_get):
    #     response = ClageHomeServer('192.168.0.78','F8F005DB0CD7','2049DB0CD7').setAutoStop(True)
    #     mock_get.assert_called_once_with('192.168.0.78/mqtt?payload=stp=2')
    #     self.assertIsNotNone(response)

    # def test_chargerNotAvailable(self):
    #     status = ClageHomeServer('127.0.0.2','F8F005DB0CD7','2049DB0CD7').requestStatus()
    #     self.maxDiff = None
    #     self.assertEqual(SAMPLE_REQUEST_STATUS_RESPONSE_UNAVAIL, status)
