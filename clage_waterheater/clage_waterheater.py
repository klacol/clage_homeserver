# -*- coding: utf-8 -*-

# API-documentation: https://app.swaggerhub.com/apis/klacol/ClageHomeServer/1.0.0
# Reverse engineered!! Unfortunaltely, there is no official documentation from the manufacturer available

import requests
import datetime
from json import JSONDecodeError


class ClageWaterHeaterStatusMapper:

    def __phaseDetection(self, phase, bit):
        if phase & bit:
            return 'on'
        else:
            return 'off'

    def mapApiStatusResponse(self, status):

        numberOfConnectedHeaters = 1  # I have only one hetaer, so i start with this scenario

        homeserver_version = ClageWaterHeater.VERSION.get(status.get('version')) or 'unknown'       # 1.4
        homeserver_error = ClageWaterHeater.ERROR.get(status.get('error')) or 'unknown'             # OK
        posixTimestamp = int(status.get('time', 0))                               # see https://www.epochconverter.com/
        homeserver_time = datetime.datetime.fromtimestamp(posixTimestamp)         # 1631263211 => Your time zone: Freitag, 10. September 2021 10:40:11 GMT+02:00 DST
        homeserver_success = bool(status.get('success'))                          # True
        homeserver_cached = bool(status.get('cached'))                            # True

        heater = status.get('devices')[numberOfConnectedHeaters-1]
        heater_id = heater.get('id')                                              # 2049DB0CD7
        heater_busId = heater.get('busId')                                        #  1
        heater_name = heater.get('name')                                          #  ""
        heater_connected = bool(heater.get('connected'))                          #  true
        heater_signal = heater.get('signal')                                      #  -67
        heater_rssi = heater.get('rssi')                                          #  0
        heater_lqi = heater.get('lqi')                                            #  0

        heater_status = heater.get('status')    
        heater_status_setpoint = float(heater_status.get('setpoint'))/10          # 600 => 60 °C
        heater_status_tInint = float(heater_status.get('tIn'))/10                 # 274 => 27.4 °C
        heater_status_tOutint = float(heater_status.get('tOut'))/10               # 244 => 24.4 °C
        heater_status_tP1 = float(heater_status.get('tP1'))/10                    # 0
        heater_status_tP2 = float(heater_status.get('tP2'))/10                    # 0
        heater_status_tP3 = float(heater_status.get('tP3'))/10                    # 0
        heater_status_tP4 = float(heater_status.get('tP4'))/10                    # 0
        heater_status_flow = float(heater_status.get('flow'))                     # 0
        heater_status_flowMax = float(heater_status.get('flowMax'))/100/1000      # 254 => 2.54 Liter => 0.00254 m³
        heater_status_valvePos = int(heater_status.get('valvePos'))               # 71 = 71 %
        heater_status_valveFlags = int(heater_status.get('valveFlags'))           # 0
        heater_status_power = float(heater_status.get('power'))                   # 0
        heater_status_powerMax = float(heater_status.get('powerMax'))/10          # 140 => 14 kW
        heater_status_power100 = float(heater_status.get('power100'))             # 0
        heater_status_fillingLeft = int(heater_status.get('fillingLeft'))         # 0
        heater_status_flags = int(heater_status.get('flags'))                     # 1
        heater_status_sysFlags = int(heater_status.get('sysFlags'))               # 0
        heater_status_error = ClageWaterHeater.ERROR.get(status.get('error')) or 'unknown' # OK

        return ({
            'homeserver_version': homeserver_version,
            'homeserver_error': homeserver_error,
            'homeserver_time': homeserver_time,
            'homeserver_success': homeserver_success,
            'homeserver_cached': homeserver_cached,
            'heater_id': heater_id,
            'heater_busId' : heater_busId,
            'heater_name' : heater_name,
            'heater_connected' : heater_connected,
            'heater_signal' : heater_signal,
            'heater_rssi' : heater_rssi,
            'heater_lqi' : heater_lqi,
            'heater_status_setpoint' : heater_status_setpoint,
            'heater_status_tInint' : heater_status_tInint,
            'heater_status_tOutint' : heater_status_tOutint,
            'heater_status_tP1' : heater_status_tP1,
            'heater_status_tP2' : heater_status_tP2,
            'heater_status_tP3' : heater_status_tP3,
            'heater_status_tP4' : heater_status_tP4,
            'heater_status_flow' : heater_status_flow,
            'heater_status_flowMax' : heater_status_flowMax,
            'heater_status_valvePos' : heater_status_valvePos,
            'heater_status_valveFlags' : heater_status_valveFlags,
            'heater_status_power' : heater_status_power,
            'heater_status_powerMax' : heater_status_powerMax,
            'heater_status_power100' : heater_status_power100,
            'heater_status_fillingLeft' : heater_status_fillingLeft,
            'heater_status_flags' : heater_status_flags,
            'heater_status_sysFlags' : heater_status_sysFlags,
            'heater_status_error' : heater_status_error,
        })


class ClageWaterHeater:

    ipAddress = ""
    homeserverId = ""
    username = "appuser"
    password = "smart"


    def __init__(self, ipAddress,homeserverId):
        if (ipAddress is None or ipAddress == ''):
            raise ValueError("ipAddress must be specified")
        self.ipAddress = ipAddress
        if (homeserverId is None or homeserverId == ''):
            raise ValueError("homeserverId must be specified")
        self.homeserverId = homeserverId
    
    VERSION = {
        '1.4': '1.4'
    }

    ERROR = {
        0: 'OK',
        1: '?',
        3: '?',
        8: '?',
        10: '?'
    }

    def __queryStatusApi(self):
        try:
            url = "https://"+self.ipAddress+"/devices/status/"+self.homeserverId
            statusRequest = requests.get(url, auth=(self.username, self.password), timeout=5, verify=False)
            status = statusRequest.json()
            return status
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            return {}


    def requestStatus(self):
        response = {}
        try:
            status = self.__queryStatusApi()
            response = ClageWaterHeaterStatusMapper().mapApiStatusResponse(status)
        except JSONDecodeError:
            response = ClageWaterHeaterStatusMapper().mapApiStatusResponse({})
        return response




######################################################################################
from ClageWaterHeater import ClageWaterHeater 
clageWaterHeater = ClageWaterHeater(ipAddress='192.168.0.78',homeserverId='2049DB0CD7') 
response = clageWaterHeater.requestStatus()

print(response)

######################################################################################