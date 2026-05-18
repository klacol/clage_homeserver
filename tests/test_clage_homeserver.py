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
    "homeserver_time": "2021-09-10 08:40:11+00:00",
    "homeserver_success": True,
    "homeserver_cached": True,
    "heater_id": "2049DB0CD7",
    "heater_busId": 1,
    "heater_name": "NameOfMyHeater",
    "heater_connected": True,
    "heater_signal": -72,
    "heater_rssi": 0,
    "heater_lqi": 0,
    "heater_status_setpoint": 60.0,
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
    return ClageHomeServer(None,None,None,'')

SAMPLE_API_LOGS_RESPONSE = {
    "version": "1.4",
    "error": 0,
    "time": 1631263211,
    "success": True,
    "devices": [
        {
            "id": "2049DB0CD7",
            "logs": [
                {"id": 1, "time": 1631263000, "length": 120, "power": 3000, "water": 500, "cid": 1},
                {"id": 2, "time": 1631263200, "length": 60, "power": 1500, "water": 250, "cid": 1}
            ]
        }
    ]
}

SAMPLE_API_TOTALS_RESPONSE = {
    "version": "1.4",
    "error": 0,
    "time": 1631263211,
    "success": True,
    "devices": [
        {
            "id": "2049DB0CD7",
            "logs": [
                {"length": 180, "power": 4500, "water": 750}
            ]
        }
    ]
}

def mocked_request_status(*args, **kwargs):
    class MockResponse:
        def __init__(self, status_code, response):
            self._response = response
            self.status_code = status_code

        def json(self):
            return self._response

    url = args[0] if args else kwargs.get('url', '')
    if url == 'https://192.168.0.78/devices/status/2049DB0CD7':
        return MockResponse(200, SAMPLE_API_STATUS_RESPONSE)
    if url == 'https://192.168.0.78/devices/setpoint/2049DB0CD7':
        return MockResponse(200, SAMPLE_API_STATUS_RESPONSE)
    return MockResponse(404, None)

def mocked_request_consumption(*args, **kwargs):
    class MockResponse:
        def __init__(self, status_code, response):
            self._response = response
            self.status_code = status_code

        def json(self):
            return self._response

    if 'showTotal=true' in args[0]:
        return MockResponse(200, SAMPLE_API_TOTALS_RESPONSE)
    if args[0] == 'https://192.168.0.78/devices/logs/2049DB0CD7':
        return MockResponse(200, SAMPLE_API_LOGS_RESPONSE)
    return MockResponse(404, None)

class TestClageHomeserver(TestCase):

    def test_create_without_host(self):
        self.assertRaises(ValueError, helper_create_instance_without_host)

    def test_create_with_host(self):
        self.assertIsNotNone(ClageHomeServer('192.168.0.78','F8F005DB0CD7','2049DB0CD7',''))

    @mock.patch('requests.get', side_effect=mocked_request_status)
    def test_requestStatus(self, mock_get):
        clageHomeServer = ClageHomeServer('192.168.0.78','F8F005DB0CD7','2049DB0CD7','') 
        status = clageHomeServer.requestStatus()
        self.assertEqual(SAMPLE_REQUEST_STATUS_RESPONSE, status)

    @mock.patch('requests.get', side_effect=mocked_request_status)
    def test_requestStatus_unavailable(self, mock_get):
        clageHomeServer = ClageHomeServer('192.168.0.78','F8F005DB0CD7','UNKNOWN_ID','') 
        status = clageHomeServer.requestStatus()
        self.assertEqual({}, status)

    @mock.patch('requests.get', side_effect=mocked_request_consumption)
    def test_GetConsumptionTotals(self, mock_get):
        clageHomeServer = ClageHomeServer('192.168.0.78','F8F005DB0CD7','2049DB0CD7','') 
        totals = clageHomeServer.GetConsumptionTotals()
        self.assertEqual(totals['number_of_watertaps'], 2)
        self.assertEqual(totals['usage_time'], 3.0)
        self.assertEqual(totals['consumption_energy'], 4.5)
        self.assertEqual(totals['consumption_water'], 7.5)

    @mock.patch('requests.put', side_effect=mocked_request_status)
    @mock.patch('requests.get', side_effect=mocked_request_status)
    def test_setTemperature(self, mock_get, mock_put):
        clageHomeServer = ClageHomeServer('192.168.0.78','F8F005DB0CD7','2049DB0CD7','')
        response = clageHomeServer.setTemperature(45.0)
        mock_put.assert_called_once_with(
            url='https://192.168.0.78/devices/setpoint/2049DB0CD7',
            auth=('appuser', 'smart'),
            data={'data': '450', 'cid': '1'},
            timeout=5,
            verify=False
        )
        self.assertIsNotNone(response)
