[![Python application](https://github.com/klacol/clage_homerserver/actions/workflows/pythonapp.yml/badge.svg)](https://github.com/klacol/clage_homerserver/actions/workflows/pythonapp.yml) [![PyPI](https://img.shields.io/pypi/v/clage-homeserver)](https://pypi.org/project/clage-homeserver/)

# clage_homeserver (WIP)
Python client for accessing the Clage Waterheater via the local https-Rest-API-Endpoint of the clage Homeserver

Tested with the "[Clage DSX Touch](https://www.clage.de/de/produkte/e-komfortdurchlauferhitzer/DSX-Touch)" with an integrated Homeserver.

Based on the [API documentation version 1.3.4](https://github.com/klacol/clage-homerserver-api/blob/master/api-docs/CLAGE%20HomeServer%20API%20v1.3.4.pdf).

# Warning: WIP - Breaking changes possible
This is the first version of the API so there are still breaking chnages possible eg. output parameter names or values.

# Links
[Project Homepage](https://github.com/klacol/clage_homeserver)

[PyPi Package](https://pypi.org/project/clage_homeserver)

[Openapi Document](https://app.swaggerhub.com/apis/klacol/ClageHomeServer/1.0.0) 

[Product Homepage](https://www.clage.de/de/produkte/e-komfortdurchlauferhitzer/DSX-Touch)

All rights of CLAGE GmbH remain unaffected.

# Features
- Query the status of the homeserver & water heater
- Query the setup values of the homeserver & water heater
- Query the consumption values for water (Liter) and energy (kWh)
- Set the setpoint temperature for the heater

# Install

```
pip install clage_homeserver
```

# Example

```python
from clage_homeserver import ClageHomeServer
clageHomeServer = ClageHomeServer('192.168.0.78','Your Homeserver ID','Your Heater ID') 
 
 # Request the status of the homeserver/heater
print (clageHomeServer.requestStatus())

 # Request the setup values of the homeserver/heater
print (clageHomeServer.requestSetup())

 # Request the consupmtion values of the homeserver/heater
print (clageHomeServer.GetConsumptionTotals())

# Set the temperature to 45.6 °C (setpoint)
clageHomeServer.setTemperature(45.6)
```
