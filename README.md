# clage-homeserver-api (WIP)
Python API for accessing the Clage Waterheater via the local https-Endpoint of the clage Homeserver

Tested with the "[Clage DSX Touch](https://www.clage.de/de/produkte/e-komfortdurchlauferhitzer/DSX-Touch)" with an integrated Homeserver.

Based on the [API documentation version 1.3.4](https://github.com/klacol/clage-homerserver-api/blob/master/api-docs/CLAGE%20HomeServer%20API%20v1.3.4.pdf).

# Warning: WIP - Breaking changes possible
This is the first version of the API so there are still breaking chnages possible eg. output parameter names or values.

# Links
[Product Homepage](https://www.clage.de/de/produkte/e-komfortdurchlauferhitzer/DSX-Touch)

[Openapi Document](ttps://app.swaggerhub.com/apis/klacol/ClageHomeServer/1.0.0) 

[Project Homepage](https://github.com/klacol/clage_homeserver-api)

[PyPi Package](https://pypi.org/project/clage_homeserver-api)

# Features
- Query Heater Status
- Set Heater Temperature

# Install

```
pip install clage_homeserver
```

# Example

```python
from clage_homeserver import clage_homeserver

heater = clage_homeserver('192.168.1.1', 'xxxxxxx') # <- change to your charger IP and your homeserver id
 
print (heater.requestStatus())
```
