# -*- coding: utf-8 -*-

# API-documentation: https://app.swaggerhub.com/apis/klacol/ClageHomeServer/1.0.0

import requests
import datetime
from json import JSONDecodeError
from datetime import datetime
import urllib3

NUMBER_OF_CONNECTED_HEATERS = 1       # I have only one heater, so i start with this scenario

class ClageHomeServerMapper:

    def __phaseDetection(self, phase, bit):
        if phase & bit:
            return 'on'
        else:
            return 'off'
    def mapApiStatusResponse(self, status):

        homeserver_version = ClageHomeServer.VERSION.get(status.get('version')) or 'unknown'       # 1.4
        homeserver_error = ClageHomeServer.ERROR.get(status.get('error')) or 'unknown'             # OK
        posixTimestamp = int(status.get('time', 0))                               # see https://www.epochconverter.com/
        homeserver_time = str(datetime.utcfromtimestamp(posixTimestamp))             # 1631263211 => Freitag, 10. September 2021 10:40:11 GMT+02:00 DST
        homeserver_success = bool(status.get('success'))                          # True
        homeserver_cached = bool(status.get('cached'))                            # True

        heater = status.get('devices')[NUMBER_OF_CONNECTED_HEATERS-1]
        heater_id = heater.get('id')                                              # 2049DB0CD7
        heater_busId = heater.get('busId')                                        # 1
        heater_name = heater.get('name')                                          # ""
        heater_connected = bool(heater.get('connected'))                          # true
        heater_signal = heater.get('signal')                                      # -67
        heater_rssi = heater.get('rssi')                                          # 0
        heater_lqi = heater.get('lqi')                                            # 0

        heater_status = heater.get('status')
        heater_status_setpoint = float(heater_status.get('setpoint'))/10          # 600 => 60 °C
        heater_status_tIn = float(heater_status.get('tIn'))/10                    # 274 => 27.4 °C
        heater_status_tOut = float(heater_status.get('tOut'))/10                  # 244 => 24.4 °C
        heater_status_tP1 = float(heater_status.get('tP1'))/10                    # 0 Temperaturspeicher 1
        heater_status_tP2 = float(heater_status.get('tP2'))/10                    # 0 Temperaturspeicher 2
        heater_status_tP3 = float(heater_status.get('tP3'))/10                    # 0 Temperaturspeicher 3
        heater_status_tP4 = float(heater_status.get('tP4'))/10                    # 0 Temperaturspeicher 4
        heater_status_flow = float(heater_status.get('flow'))/10                  # 0 Wasserfluss in Liter/Minute

        heater_status_flowMax_float = float(heater_status.get('flowMax'))    
        if (heater_status_flowMax_float == 0 or heater_status_flowMax_float == 253 or heater_status_flowMax_float == 254):
            heater_status_flowMax = ClageHomeServer.FLOWMAX.get(heater_status.get('flowMax')) or 'unknown'  # Durchflussmengenbegrenzung (0=AUS, 253=ECO, 254=AUTO)
        else: 
            heater_status_flowMax = heater_status_flowMax_float/10                                          # 250 Maximaler Wasserfluss in Liter/Minute
              
        heater_status_valvePos = int(heater_status.get('valvePos'))               # Stellung des Motorventils: 71 = 71 % offen
        heater_status_valveFlags = int(heater_status.get('valveFlags'))           # 0
        heater_status_power = float(heater_status.get('power'))/1000              # 1972 Watt = 1,972 kW  Leistungsaufnahme
        heater_status_powerMax = float(heater_status.get('powerMax'))             # Höchstwert der Leistungsaufnahme: 140 => 21 kW, siehe Kapitel 4.9 in der API-Dokumentation
        heater_status_power100 = float(heater_status.get('power100'))             # 0
        heater_status_fillingLeft = int(heater_status.get('fillingLeft'))         # 0
        heater_status_flags = int(heater_status.get('flags'))                     # 1
        heater_status_sysFlags = int(heater_status.get('sysFlags'))               # 0
        heater_status_error = ClageHomeServer.ERROR.get(heater_status.get('error')) or 'unknown'  # OK

        return ({
            'homeserver_version': homeserver_version,
            'homeserver_error': homeserver_error,
            'homeserver_time': homeserver_time,
            'homeserver_success': homeserver_success,
            'homeserver_cached': homeserver_cached,
            'heater_id': heater_id,
            'heater_busId': heater_busId,
            'heater_name': heater_name,
            'heater_connected': heater_connected,
            'heater_signal': heater_signal,
            'heater_rssi': heater_rssi,
            'heater_lqi': heater_lqi,
            'heater_status_setpoint': heater_status_setpoint,
            'heater_status_tIn': heater_status_tIn,
            'heater_status_tOut': heater_status_tOut,
            'heater_status_tP1': heater_status_tP1,
            'heater_status_tP2': heater_status_tP2,
            'heater_status_tP3': heater_status_tP3,
            'heater_status_tP4': heater_status_tP4,
            'heater_status_flow': heater_status_flow,
            'heater_status_flowMax': heater_status_flowMax,
            'heater_status_valvePos': heater_status_valvePos,
            'heater_status_valveFlags': heater_status_valveFlags,
            'heater_status_power': heater_status_power,
            'heater_status_powerMax': heater_status_powerMax,
            'heater_status_power100': heater_status_power100,
            'heater_status_fillingLeft': heater_status_fillingLeft,
            'heater_status_flags': heater_status_flags,
            'heater_status_sysFlags': heater_status_sysFlags,
            'heater_status_error': heater_status_error,
        })


    def mapApiSetupResponse(self, setup):

        heater = setup.get('devices')[NUMBER_OF_CONNECTED_HEATERS-1]
        heater_setup = heater.get('setup')

        heater_setup_swVersion = heater_setup.get('swVersion')                                    # String, z.B. 1.4.1,	Version der Gerätesoftware
        heater_setup_serialDevice = heater_setup.get('serialDevice')                              # String, Seriennummer des Gerätes
        heater_setup_serialPowerUnit = heater_setup.get('serialPowerUnit')                        # String, Seriennummer des Leistungsteils
        heater_setup_flowMax = float(heater_setup.get('flowMax'))/10                              # uint8_t, 1/10, l/min => m³/h", 254, "Durchflussmengenbegrenzung 0/255=aus, 253=ECO,254=AUTO"
        heater_setup_loadShedding = float(heater_setup.get('loadShedding')),                      # uint8_t, 0, Lastabwurf; 0=aus
        heater_setup_scaldProtection = float(heater_setup.get('scaldProtection'))                 # uint16_t, 1/10, °C, 420, Verbrühschutztemperatur; 0=aus; entspr. tLimit
        heater_setup_sound = heater_setup.get('sound')                                            # uint8_t, 0, Signalton; 0=aus
        heater_setup_fcpAddr = heater_setup.get('fcpAddr')                                        # uint8_t, dez.	80,	Adresse
        heater_setup_powerCosts = float(heater_setup.get('powerCosts'))                           # uint8_t, 25, Kosten pro kWh (Cent)
        heater_setup_powerMax = float(heater_setup.get('powerMax'))                               # uint8_t, 140, Höchstwert der Leistungsaufnahme
        heater_setup_calValue = float(heater_setup.get('calValue'))                               # Integer, 2800, interner Kontrollwert
        heater_setup_timerPowerOn = float(heater_setup.get('timerPowerOn'))                       # uint32_t, s, 300,	Heizdauer
        heater_setup_timerLifetime = float(heater_setup.get('timerLifetime'))/60/60               # uint32_t,	s=>h,	172800,	Gesamtbetriebsdauer
        heater_setup_timerStandby = float(heater_setup.get('timerStandby'))                       # uint32_t,	s, 2400, Betriebsdauer seit dem letzten Stromausfall
        #heater_setup_totalPowerConsumption = round(float(heater_setup.get('totalPowerConsumption')),1)     # uint16_t,	kWh, 0, Gesamtenergie
        #heater_setup_totalWaterConsumption = round(float(heater_setup.get('totalWaterConsumption')),0)     # uint16_t,	Liter, 0, Gesamtwassermenge

        return ({
            'heater_setup_swVersion': heater_setup_swVersion, 
            'heater_setup_serialDevice': heater_setup_serialDevice,
            'heater_setup_serialPowerUnit': heater_setup_serialPowerUnit,
            'heater_setup_flowMax': heater_setup_flowMax,
            'heater_setup_loadShedding': heater_setup_loadShedding,
            'heater_setup_scaldProtection': heater_setup_scaldProtection,
            'heater_setup_sound': heater_setup_sound,
            'heater_setup_fcpAddr': heater_setup_fcpAddr,
            'heater_setup_powerCosts': heater_setup_powerCosts,
            'heater_setup_powerMax': heater_setup_powerMax,
            'heater_setup_calValue': heater_setup_calValue,
            'heater_setup_timerPowerOn': heater_setup_timerPowerOn,
            'heater_setup_timerLifetime': heater_setup_timerLifetime,
            'heater_setup_timerStandby': heater_setup_timerStandby,
        })

    def mapApiLogsResponse(self, logs):

        heater = logs.get('devices')[NUMBER_OF_CONNECTED_HEATERS-1]
        heater_logs = heater.get('logs')
        
        heater_setup_id = float(heater_logs.get('id)'))                        # id	uint32_t		1	eindeutiger Datensatzindex
        posixTimestamp = int(heater_logs.get('time', 0))                       # see https://www.epochconverter.com/
        heater_setup_time = str(datetime.utcfromtimestamp(posixTimestamp))      # time	uint64_t	Unixtime	1355266800	Endzeit der Zapfung in UTC
        heater_setup_length = float(heater_logs.get('length'))                 # length	uint32_t	s	10 s	Dauer des Zapfvorgangs in s
        heater_setup_power = float(heater_logs.get('power'))/1000              # power	uint32_t	1/1 Wh	6 Wh	Energiebedarf in kWh
        heater_setup_water = float(heater_logs.get('water'))                   # water	uint32_t	1/100 l	0,42 l	genutzte Wassermenge in Liter
        heater_setup_cid = float(heater_logs.get('cid'))                       # cid	int32_t		2	"kundenspez. ID, die beim Zapfvorgang gesetzt war (über „PUT /devices/setpoint/{id}“)"

        return ({
            'heater_setup_id': heater_setup_id, 
            'heater_setup_time': heater_setup_time,
            'heater_setup_length': heater_setup_length,
            'heater_setup_power': heater_setup_power,
            'heater_setup_water': heater_setup_water,
            'heater_setup_cid': heater_setup_cid,
        })

class ClageHomeServer:

    ipAddress = ""
    homeserverId = ""
    heaterId = ""
    username = "appuser"
    password = "smart"

    def __init__(self, ipAddress, homeserverId, heaterId):
        if (ipAddress is None or ipAddress == ''):
            raise ValueError("ipAddress must be specified")
        self.ipAddress = ipAddress
        if (homeserverId is None or homeserverId == ''):
            raise ValueError("homeserverId must be specified")
        self.homeserverId = homeserverId
        if (heaterId is None or heaterId == ''):
            raise ValueError("heaterId must be specified")
        self.heaterId = heaterId

    VERSION = {
        '1.4': '1.4'
    }

    ERROR = {
        0: 'OK',
        1: 'Known, but not documented',
        3: 'Known, but not documented',
        8: 'Known, but not documented',
        10: 'Known, but not documented'
    }

    FLOWMAX = {
        0: 'Aus',
        253: 'ECO',
        254: 'AUTO'
    }

    ERRORTYPE = {
        0: 'No error',
        1: 'Warning',
        2: 'Defect'
    }

    ERRORCODE_HOMESERVER = {                # ToDo: Translate to english or find concept for translation of sensor names and sensor values
        0: 'kein Fehler',
        -1: 'Gerät nicht angemeldet oder nicht (mehr) vorhanden',
        -2: 'Reserviert',
        -3: 'Timeout, Gerät angemeldet aber antwortet nicht',
        -4: 'Reserviert',
        -5: 'Reserviert'
    }
    
    ERRORCODE_HEATER = {                   # ToDo: Translate to english or find concept for translation of sensor names and sensor values
        0: 'kein Fehler',
        10: 'Fehler Bussystem, Bedienfeld defekt?',
        11: 'Überspannung',
        12: 'Unterspannung',
        11: 'Überspannung',
        13: 'Phasenfehler',
        51: 'Auslauftemperatur falsch',
        53: 'Einlauftemperatur falsch',
        56: 'Temperaturfühler am Auslauf defekt',
        58: 'Temperaturfühler am Einlauf defekt?',
        59: 'Temperaturfühler vertauscht',
        61: 'Kalibrierwert zu hoch',
        62: 'Kalibrierwert zu niedrig',
        63: 'Fehler Heizelement',
        75: 'Durchfluss zu groß (Luft im System)',
        76: 'Auslauftemperatur zu groß (Luft im System)',
        77: 'Luftblasen erkannt',
        80: 'Initialisierungsfehler Funkmodul',
        99: 'Unbekannter Fehler'
    }

    ACCESSCODE_API = {
        0: 'fSetpointRead: GET deviceSetpoint (Sollwert lesen)',
        1: 'fSetpointWrite: PUT\:deviceSetpoint (Sollwert ändern)',
        2: 'fStatusRead: GET deviceStatus (Gerätestatus lesen)',
        3: 'fStatusWrite: PUT deviceStatus (Gerätestatus ändern)',
        4: 'fSetupRead: GET deviceSetup (Gerätekonfiguration lesen)',
        5: 'fSetupWrite: PUT deviceSetup (Gerätekonfiguration ändern)',
        6: 'fErrorsRead: GET deviceErrors (Fehlerspeicher lesen)',
        7: 'fErrorsWrite: PUT deviceErrors (Fehlerspeicher ändern)',
        8: 'fLogsRead: GET deviceLogs (Verbrauchsdaten lesen)',
        9: 'fLogsWrite: PUT deviceLogs (Verbrauchsdaten ändern)',
        10: 'fListRead: POST, GET deviceList (Geräte suchen, anzeigen)',
        11: 'fListWrite: PUT, DELETE deviceList (Geräte an-/abmelden)',
        12: 'fTimerRead: GET timerList (Timer lesen)',
        13: 'fTimerWrite: POST, PUT, DELETE timerList (Timer erstellen, ändern, löschen)',
        14: 'fFileRead: GET fileList (Dateien lesen)',
        15: 'fFileWrite: POST, PUT fileList (Dateien erstellen, ändern)',
    }


    def __queryStatusApi(self):
        try:
            urllib3.disable_warnings()
            
            # use http long polling (lp); see api docs
            # How to user this ansync in a Home Assistant integration/component??
            # rev=1; 
            # while (1): 
            #     url = "https://"+self.ipAddress+"/devices?lp="+str(rev)+"&showbusid=1&showerrors=1&showlogs=1&showtotal=1"   
            #     long_polling_timeout = 35 # greater than 30 seconds; after 30 seconds the server terminated the long polling request automatically
            #     statusrequest = requests.get(url, auth=(self.username, self.password), timeout=long_polling_timeout, verify=False)
            #     status_resonse_json = statusrequest.json() 
            #     rev_old=rev
            #     rev=status_resonse_json['rev']
            #     temperature = status_resonse_json['devices'][0]['info']['setpoint']
            #     if (rev != rev_old):
            #       print(str(datetime.today()) + ' - changed: setpoint = '+str(int(temperature)/10) + ' °c')
            #     else:
            #       print(str(datetime.today()) + ' - unchanged: setpoint = '+str(int(temperature)/10) + ' °c')   
            

            url = "https://"+self.ipAddress+"/devices/status/"+self.heaterId
            statusRequest = requests.get(url, auth=(self.username, self.password), timeout=5, verify=False)
            status = statusRequest.json()
            return status
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            return {}

    def __querySetupApi(self):
        try:
            urllib3.disable_warnings()
            
            # use http long polling (lp); see api docs
            # How to user this ansync in a Home Assistant integration/component??
            # rev=1; 
            # while (1): 
            #     url = "https://"+self.ipAddress+"/devices?lp="+str(rev)+"&showbusid=1&showerrors=1&showlogs=1&showtotal=1"   
            #     long_polling_timeout = 35 # greater than 30 seconds; after 30 seconds the server terminated the long polling request automatically
            #     statusrequest = requests.get(url, auth=(self.username, self.password), timeout=long_polling_timeout, verify=False)
            #     status_resonse_json = statusrequest.json() 
            #     rev_old=rev
            #     rev=status_resonse_json['rev']
            #     temperature = status_resonse_json['devices'][0]['info']['setpoint']
            #     if (rev != rev_old):
            #       print(str(datetime.today()) + ' - changed: setpoint = '+str(int(temperature)/10) + ' °c')
            #     else:
            #       print(str(datetime.today()) + ' - unchanged: setpoint = '+str(int(temperature)/10) + ' °c')   
            

            url = "https://"+self.ipAddress+"/devices/setup/"+self.heaterId
            setupRequest = requests.get(url, auth=(self.username, self.password), timeout=5, verify=False)
            setup = setupRequest.json()
            return setup
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            return {}

    def GetConsumption(self):
        urllib3.disable_warnings()
        response = {}
        try:
            url = "https://"+self.ipAddress+"/devices/logs/"+self.heaterId
            logsRequest = requests.get(url, auth=(self.username, self.password), timeout=5, verify=False)
            logs = logsRequest.json()

            heater = logs.get('devices')[NUMBER_OF_CONNECTED_HEATERS-1]
            heater_logs = heater.get('logs')
            
            number_of_watertaps = 0
            usage_time = 0
            consumption_energy = 0
            consumption_water = 0

            for log in heater_logs:
                heater_setup_id = int(log.get('id'))                         # id	uint32_t		1	eindeutiger Datensatzindex
                posixTimestamp = int(log['time'])                            # see https://www.epochconverter.com/
                heater_setup_time = str(datetime.utcfromtimestamp(posixTimestamp))      # time	uint64_t	Unixtime	1355266800	Endzeit der Zapfung in UTC
                heater_setup_length = int(log.get('length'))                 # length	uint32_t	s	10 s	Dauer des Zapfvorgangs in s
                heater_setup_energy = round(int(log.get('power'))/1000,1)    # power	uint32_t	1/1 Wh	6 Wh	Energiebedarf in kWh, it is energy(kWh) not power (kW)
                heater_setup_water = round(int(log.get('water'))/100,0)      # water	uint32_t	1/100 l	0,42 l	Genutzte Wassermenge in Liter
                heater_setup_cid = int(log.get('cid'))                       # cid	int32_t		2	"kundenspez. ID, die beim Zapfvorgang gesetzt war (über „PUT /devices/setpoint/{id}“)"
                number_of_watertaps += 1   
                usage_time += heater_setup_length                 
                consumption_energy += heater_setup_energy
                consumption_water += heater_setup_water

            return ({
            'number_of_watertaps': number_of_watertaps, 
            'usage_time': usage_time,
            'consumption_energy': consumption_energy,
            'consumption_water': consumption_water,
            })
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            return {}

    def setTemperature(self, temperature):
        try:
            tempApiValue = str(int(temperature*10))
            url = "https://"+self.ipAddress+"/devices/setpoint/"+self.heaterId
            body = {'data': tempApiValue, 'cid': '1'}
            setRequest = requests.put(url=url, auth=(self.username, self.password), data=body, timeout=5, verify=False)
            return ClageHomeServerMapper().mapApiStatusResponse(setRequest.json())
        except (requests.exceptions.ConnectTimeout, requests.exceptions.ConnectionError):
            return {}

    def requestStatus(self):
        response = {}
        try:
            status = self.__queryStatusApi()
            response = ClageHomeServerMapper().mapApiStatusResponse(status)
        except JSONDecodeError:
            response = ClageHomeServerMapper().mapApiStatusResponse({})
        return response

    def requestSetup(self):
        response = {}
        try:
            setup = self.__querySetupApi()
            response = ClageHomeServerMapper().mapApiSetupResponse(setup)
        except JSONDecodeError:
            response = ClageHomeServerMapper().mapApiSetupResponse({})
        return response

