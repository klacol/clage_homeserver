from unittest import (TestCase, mock)
from clage_homeserver import ClageHomeServerStatusMapper

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

class TestClageHomeServerStatusMapper(TestCase):

    def __helper_get_mapped_key(self, key, value):
        apiResponse = dict(SAMPLE_API_STATUS_RESPONSE)
        apiResponse[key] = value
        return ClageHomeServerStatusMapper().mapApiStatusResponse(apiResponse)

    def test_map_version(self):
        self.assertEqual('unknown', self.__helper_get_mapped_key('version', 'unknown').get('homeserver_version'))

    def test_map_setpoint(self):
        self.assertEqual(600, self.__helper_get_mapped_key('setpoint', 600).get('heater_setpoint'))

    def test_map_charger_err(self):
        self.assertEqual("RCCB", self.__helper_get_mapped_key('err','1').get('charger_err'))
        self.assertEqual("PHASE", self.__helper_get_mapped_key('err','3').get('charger_err'))
        self.assertEqual("NO_GROUND", self.__helper_get_mapped_key('err','8').get('charger_err'))
        self.assertEqual("INTERNAL", self.__helper_get_mapped_key('err','10').get('charger_err'))
        self.assertEqual("OK", self.__helper_get_mapped_key('err','0').get('charger_err'))
        self.assertEqual("UNKNOWN", self.__helper_get_mapped_key('err','12').get('charger_err'))

    def test_map_access(self):
        self.assertEqual("free", self.__helper_get_mapped_key('ast','0').get('charger_access'))
        self.assertEqual("rfid/app", self.__helper_get_mapped_key('ast','1').get('charger_access'))
        self.assertEqual("cost based / automatic", self.__helper_get_mapped_key('ast','2').get('charger_access'))

    def test_map_allow_charging(self):
        self.assertEqual("off", self.__helper_get_mapped_key('alw','0').get('allow_charging'))
        self.assertEqual("on", self.__helper_get_mapped_key('alw','1').get('allow_charging'))

    def test_map_stop_mode(self):
        self.assertEqual("manual", self.__helper_get_mapped_key('stp','0').get('stop_mode'))
        self.assertEqual("kWh based", self.__helper_get_mapped_key('stp','2').get('stop_mode'))
 
    def test_map_cable_max_current(self):
        self.assertEqual(9, self.__helper_get_mapped_key('cbl', 9).get('cable_max_current'))

    def test_map_pre_contactor_l1(self):
        self.assertEqual('on', self.__helper_get_mapped_key('pha', 0x08).get('pre_contactor_l1'))
        self.assertEqual('off', self.__helper_get_mapped_key('pha', 0x00).get('pre_contactor_l1'))

    def test_map_pre_contactor_l2(self):
        self.assertEqual('on', self.__helper_get_mapped_key('pha', 0x10).get('pre_contactor_l2'))
        self.assertEqual('off', self.__helper_get_mapped_key('pha', 0x00).get('pre_contactor_l2'))

    def test_map_pre_contactor_l3(self):
        self.assertEqual('on', self.__helper_get_mapped_key('pha', 0x20).get('pre_contactor_l3'))
        self.assertEqual('off', self.__helper_get_mapped_key('pha', 0x00).get('pre_contactor_l3'))

    def test_map_post_contactor_l1(self):
        self.assertEqual('on', self.__helper_get_mapped_key('pha', 0x01).get('post_contactor_l1'))
        self.assertEqual('off', self.__helper_get_mapped_key('pha', 0x00).get('post_contactor_l1'))

    def test_map_post_contactor_l2(self):
        self.assertEqual('on', self.__helper_get_mapped_key('pha', 0x02).get('post_contactor_l2'))
        self.assertEqual('off', self.__helper_get_mapped_key('pha', 0x00).get('post_contactor_l2'))

    def test_map_post_contactor_l3(self):
        self.assertEqual('on', self.__helper_get_mapped_key('pha', 0x04).get('post_contactor_l3'))
        self.assertEqual('off', self.__helper_get_mapped_key('pha', 0x00).get('post_contactor_l3'))

    def test_map_charger_temp(self):
        self.assertEqual(32, self.__helper_get_mapped_key('tmp', 3).get('charger_temp'))

    def test_map_charger_temp0(self):
        self.assertEqual(30.55, ClageHomeServerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('charger_temp0'))

    def test_map_charger_temp1(self):
        self.assertEqual(31.55, ClageHomeServerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('charger_temp1'))

    def test_map_charger_temp2(self):
        self.assertEqual(32.55, ClageHomeServerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('charger_temp2'))

    def test_map_charger_temp3(self):
        self.assertEqual(33.55, ClageHomeServerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('charger_temp3'))

    def test_map_current_session_charged_energy(self):
        self.assertEqual(1, self.__helper_get_mapped_key('dws', 360000).get('current_session_charged_energy'))

    def test_map_charge_limit(self):
        self.assertEqual(1, self.__helper_get_mapped_key('dwo', 10).get('charge_limit'))

    def test_map_adapter(self):
        self.assertEqual('No Adapter', self.__helper_get_mapped_key('adi', '0').get('adapter'))
        self.assertEqual('16A-Adapter', self.__helper_get_mapped_key('adi', '1').get('adapter'))

    def test_map_unlocked_by_card(self):
        self.assertEqual(2, self.__helper_get_mapped_key('uby', '2').get('unlocked_by_card'))

    def test_map_energy_total(self):
        self.assertEqual(42, self.__helper_get_mapped_key('eto', 420).get('energy_total'))

    def test_map_wifi(self):
        self.assertEqual('connected', self.__helper_get_mapped_key('wst', '3').get('wifi'))
        self.assertEqual('not connected', self.__helper_get_mapped_key('wst', '0').get('wifi'))

    def test_map_firmware(self):
        self.assertEqual('33', self.__helper_get_mapped_key('fwv', '33').get('firmware'))

    def test_map_serial(self):
        self.assertEqual('123456', self.__helper_get_mapped_key('sse', '123456').get('serial_number'))

    def test_map_wifi_ssid(self):
        self.assertEqual('ssid', self.__helper_get_mapped_key('wss', 'ssid').get('wifi_ssid'))

    def test_map_wifi_enabled(self):
        self.assertEqual('off', self.__helper_get_mapped_key('wen', '0').get('wifi_enabled'))
        self.assertEqual('on', self.__helper_get_mapped_key('wen', '1').get('wifi_enabled'))

    def test_map_timezone_offset(self):
        self.assertEqual(100, self.__helper_get_mapped_key('tof', '200').get('timezone_offset'))

    def test_map_timezone_dst_offset(self):
        self.assertEqual(200, self.__helper_get_mapped_key('tds', '200').get('timezone_dst_offset'))

    def test_map_meter_values(self):
        self.assertEqual(1, ClageHomeServerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('u_l1'))
        self.assertEqual(2, ClageHomeServerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('u_l2'))
        self.assertEqual(3, ClageHomeServerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('u_l3'))
        self.assertEqual(4, ClageHomeServerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('u_n'))
        self.assertEqual(0.5, ClageHomeServerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('i_l1'))
        self.assertEqual(0.6, ClageHomeServerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('i_l2'))
        self.assertEqual(0.7, ClageHomeServerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('i_l3'))
        self.assertEqual(0.8, ClageHomeServerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('p_l1'))
        self.assertEqual(0.9, ClageHomeServerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('p_l2'))
        self.assertEqual(1.0, ClageHomeServerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('p_l3'))
        self.assertEqual(1.1, ClageHomeServerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('p_n'))
        self.assertEqual(0.12, ClageHomeServerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('p_all'))
        self.assertEqual(13, ClageHomeServerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('lf_l1'))
        self.assertEqual(14, ClageHomeServerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('lf_l2'))
        self.assertEqual(15, ClageHomeServerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('lf_l3'))
        self.assertEqual(16, ClageHomeServerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('lf_n'))
        self.assertEqual(0, ClageHomeServerStatusMapper().mapApiStatusResponse(SAMPLE_API_STATUS_RESPONSE).get('cable_lock_mode'))

    