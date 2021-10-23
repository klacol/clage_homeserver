from unittest import (TestCase, mock)
from clage_homeserver import (ClageHomeServer,ClageHomeServerStatusMapper)

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
            "signal": -67,
            "rssi": 0,
            "lqi": 0,
            "status": {
                "setpoint": 600,
                "tLimit": 0,
                "tIn": 274,
                "tOut": 244,
                "tP1": 0,
                "tP2": 0,
                "tP3": 0,
                "tP4": 0,
                "flow": 0,
                "flowMax": 254,
                "valvePos": 71,
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
SAMPLE_REQUEST_STATUS_RESPONSE_UNAVAIL = {}

def helper_create_instance_without_host():
    return ClageHomeServer(None,None)

def helper_setButtonCurrentValue_ValueError():
    return ClageHomeServer('https://192.168.0.78','2049DB0CD7').setButtonCurrentValue(0,6)

def helper_setAccessType_ValueError():
    return ClageHomeServer('https://192.168.0.78','2049DB0CD7').setAccessType(1111)

def helper_setCableLockMode_ValueError():
    return ClageHomeServer('https://192.168.0.78','2049DB0CD7').setCableLockMode(1111)

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, status_code, response):
            self._response = response
            self.status_code = status_code

        def json(self):
            return self._response

    if args[0] == 'https://192.168.0.78/status':
        return MockResponse(200, SAMPLE_API_STATUS_RESPONSE)
    return MockResponse(404, None)

class TestClageWaterHeater(TestCase):

    def test_create_without_host(self):
        self.assertRaises(ValueError, helper_create_instance_without_host)

    def test_create_with_host(self):
        self.assertIsNotNone(ClageHomeServer('https://192.168.0.78','2049DB0CD7'))

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_requestStatus(self, mock_get):
        status = ClageHomeServer('https://192.168.0.78/status','2049DB0CD7').requestStatus()
        self.assertEqual(SAMPLE_API_STATUS_RESPONSE, status)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setTemperature(self, mock_get):
        response = ClageHomeServer('https://192.168.0.78','2049DB0CD7').setTemperature(450)
        mock_get.assert_called_once_with('https://192.168.0.78/x')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setMaxCurrentToHigh(self, mock_get):
        response = ClageHomeServer('https://192.168.0.78','2049DB0CD7').setMaxCurrent(33)
        mock_get.assert_called_once_with('https://192.168.0.78/mqtt?payload=amp=32')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setLedAutoTurnOffTrue(self, mock_get):
        response = ClageHomeServer('https://192.168.0.78','2049DB0CD7').setLedAutoTurnOff(True)
        mock_get.assert_called_once_with('https://192.168.0.78/mqtt?payload=r2x=1')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setAllowChargingTrue(self, mock_get):
        response = ClageHomeServer('https://192.168.0.78','2049DB0CD7').setAllowCharging(True)
        mock_get.assert_called_once_with('https://192.168.0.78/mqtt?payload=alw=1')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setAllowChargingFalse(self, mock_get):
        response = ClageHomeServer('https://192.168.0.78','2049DB0CD7').setAllowCharging(False)
        mock_get.assert_called_once_with('https://192.168.0.78/mqtt?payload=alw=0')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setAutoStopTrue(self, mock_get):
        response = ClageHomeServer('https://192.168.0.78','2049DB0CD7').setAutoStop(True)
        mock_get.assert_called_once_with('https://192.168.0.78/mqtt?payload=stp=2')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setAutoStopFalse(self, mock_get):
        response = ClageHomeServer('https://192.168.0.78','2049DB0CD7').setAutoStop(False)
        mock_get.assert_called_once_with('https://192.168.0.78/mqtt?payload=stp=0')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setStandbyColor(self, mock_get):
        response = ClageHomeServer('https://192.168.0.78','2049DB0CD7').setStandbyColor(0x808080)
        mock_get.assert_called_once_with('https://192.168.0.78/mqtt?payload=cid=8421504')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setChargingActiveColor(self, mock_get):
        response = ClageHomeServer('https://192.168.0.78','2049DB0CD7').setChargingActiveColor(0x808080)
        mock_get.assert_called_once_with('https://192.168.0.78/mqtt?payload=cch=8421504')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setChargingFinishedColor(self, mock_get):
        response = ClageHomeServer('https://192.168.0.78','2049DB0CD7').setChargingFinishedColor(0x808080)
        mock_get.assert_called_once_with('https://192.168.0.78/mqtt?payload=cfi=8421504')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setLedBrightness(self, mock_get):
        response = ClageHomeServer('https://192.168.0.78','2049DB0CD7').setLedBrightness(100)
        mock_get.assert_called_once_with('https://192.168.0.78/mqtt?payload=lbr=100')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setLedBrightnessToLow(self, mock_get):
        response = ClageHomeServer('https://192.168.0.78','2049DB0CD7').setLedBrightness(-1)
        mock_get.assert_called_once_with('https://192.168.0.78/mqtt?payload=lbr=0')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setLedBrightnessToHigh(self, mock_get):
        response = ClageHomeServer('https://192.168.0.78','2049DB0CD7').setLedBrightness(256)
        mock_get.assert_called_once_with('https://192.168.0.78/mqtt?payload=lbr=255')
        self.assertIsNotNone(response)

    def test_chargerNotAvailable(self):
        status = ClageHomeServer('http://127.0.0.2','2049DB0CD7').requestStatus()
        self.maxDiff = None
        self.assertEqual(SAMPLE_REQUEST_STATUS_RESPONSE_UNAVAIL, status)
