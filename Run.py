from clage_homeserver import ClageHomeServer

clageHomeServer = ClageHomeServer('192.168.0.78','F8F005DB0CD7','2016FFEE22', '') # <- change to your charger IP
target_temperature = 50.0

print("=== Devices ===")
print(clageHomeServer.requestDevicesRaw())
print("=== Status (raw) ===")
print(clageHomeServer.requestStatusRaw())
print("=== Setup (raw) ===")
print(clageHomeServer.requestSetupRaw())
print("=== Status ===")
print(clageHomeServer.requestStatus())
print("=== Setup ===")
print(clageHomeServer.requestSetup())
print("=== Consumption ===")
print(clageHomeServer.GetConsumptionTotals())

print(f"=== Set Temperature to {target_temperature} °C ===")
result = clageHomeServer.setTemperature(target_temperature)
actual = result.get('heater_status_setpoint')
print(f"Response setpoint: {actual} °C")

print("=== Verify Status ===")
status = clageHomeServer.requestStatus()
verified = status.get('heater_status_setpoint')
print(f"Verified setpoint: {verified} °C")

if actual == target_temperature == verified:
    print(f"OK — Temperatur korrekt auf {target_temperature} °C gesetzt.")
else:
    print(f"FEHLER — Erwartet: {target_temperature}, Response: {actual}, Verify: {verified}")
