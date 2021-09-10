from unittest import (TestCase, mock)
from clage_waterheater import (ClageWaterHeater,ClageWaterHeaterStatusMapper)

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
    return ClageWaterHeater(None)

def helper_setButtonCurrentValue_ValueError():
    return ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setButtonCurrentValue(0,6)

def helper_setAccessType_ValueError():
    return ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setAccessType(1111)

def helper_setCableLockMode_ValueError():
    return ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setCableLockMode(1111)

def mocked_requests_get(*args, **kwargs):
    class MockResponse:
        def __init__(self, status_code, response):
            self._response = response
            self.status_code = status_code

        def json(self):
            return self._response

    if args[0] == 'http://127.0.0.1/status' or args[0].startswith('http://127.0.0.1/mqtt?payload='):
        return MockResponse(200, SAMPLE_API_STATUS_RESPONSE)
    return MockResponse(404, None)

class TestClageWaterHeater(TestCase):

    def test_create_without_host(self):
        self.assertRaises(ValueError, helper_create_instance_without_host)

    def test_create_with_host(self):
        self.assertIsNotNone(ClageWaterHeater('http://127.0.0.1','MyHomeServerID'))

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_requestStatus(self, mock_get):
        status = ClageWaterHeater('http://127.0.0.1','MyHomeServerID').requestStatus()
        self.assertEqual(SAMPLE_REQUEST_STATUS_RESPONSE, status)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setAccessType(self, mock_get):
        response = ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setAccessType(ClageWaterHeater.AccessType.FREE)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=ast=0')
        self.assertIsNotNone(response)

    def test_setAccessTypeInvalidValue(self):
        self.assertRaises(ValueError, helper_setAccessType_ValueError)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setCableLockMode(self, mock_get):
        response = ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setCableLockMode(ClageWaterHeater.CableLockMode.AUTOMATIC)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=ust=1')
        self.assertIsNotNone(response)

    def test_setCableLockModeInvalidValue(self):
        self.assertRaises(ValueError, helper_setCableLockMode_ValueError)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setButtonCurrentValue(self, mock_get):
        response = ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setButtonCurrentValue(1,6)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=al1=6')
        self.assertIsNotNone(response)

    def test_setButtonCurrentValueInvalidButton(self):
        self.assertRaises(ValueError, helper_setButtonCurrentValue_ValueError)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setButtonCurrentValueToLow(self, mock_get):
        response = ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setButtonCurrentValue(1,5)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=al1=0')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setButtonCurrentValueToHigh(self, mock_get):
        response = ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setButtonCurrentValue(1,33)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=al1=32')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setChargeLimit(self, mock_get):
        response = ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setChargeLimit(2.4)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=dwo=24')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setTmpMaxCurrent(self, mock_get):
        response = ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setTmpMaxCurrent(10)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=amx=10')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setTmpMaxCurrentToLow(self, mock_get):
        response = ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setTmpMaxCurrent(5)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=amx=6')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setTmpMaxCurrentToHigh(self, mock_get):
        response = ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setTmpMaxCurrent(33)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=amx=32')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setMaxCurrent(self, mock_get):
        response = ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setMaxCurrent(10)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=amp=10')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setMaxCurrentToLow(self, mock_get):
        response = ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setMaxCurrent(5)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=amp=6')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setMaxCurrentToHigh(self, mock_get):
        response = ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setMaxCurrent(33)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=amp=32')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setAbsoluteMaxCurrentToLow(self, mock_get):
        response = ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setAbsoluteMaxCurrent(5)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=ama=6')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setAbsoluteMaxCurrentToHigh(self, mock_get):
        response = ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setAbsoluteMaxCurrent(33)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=ama=32')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setLedAutoTurnOffTrue(self, mock_get):
        response = ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setLedAutoTurnOff(True)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=r2x=1')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setLedAutoTurnOffFalse(self, mock_get):
        response = ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setLedAutoTurnOff(False)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=r2x=0')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setAllowChargingTrue(self, mock_get):
        response = ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setAllowCharging(True)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=alw=1')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setAllowChargingFalse(self, mock_get):
        response = ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setAllowCharging(False)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=alw=0')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setAutoStopTrue(self, mock_get):
        response = ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setAutoStop(True)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=stp=2')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setAutoStopFalse(self, mock_get):
        response = ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setAutoStop(False)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=stp=0')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setStandbyColor(self, mock_get):
        response = ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setStandbyColor(0x808080)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=cid=8421504')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setChargingActiveColor(self, mock_get):
        response = ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setChargingActiveColor(0x808080)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=cch=8421504')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setChargingFinishedColor(self, mock_get):
        response = ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setChargingFinishedColor(0x808080)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=cfi=8421504')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setLedBrightness(self, mock_get):
        response = ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setLedBrightness(100)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=lbr=100')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setLedBrightnessToLow(self, mock_get):
        response = ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setLedBrightness(-1)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=lbr=0')
        self.assertIsNotNone(response)

    @mock.patch('requests.get', side_effect=mocked_requests_get)
    def test_setLedBrightnessToHigh(self, mock_get):
        response = ClageWaterHeater('http://127.0.0.1','MyHomeServerID').setLedBrightness(256)
        mock_get.assert_called_once_with('http://127.0.0.1/mqtt?payload=lbr=255')
        self.assertIsNotNone(response)

    def test_chargerNotAvailable(self):
        status = ClageWaterHeater('http://127.0.0.2','MyHomeServerID').requestStatus()
        self.maxDiff = None
        self.assertEqual(SAMPLE_REQUEST_STATUS_RESPONSE_UNAVAIL, status)
