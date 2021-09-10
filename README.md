# clage_waterheater API (WIP)
Python API for accessing the Clage Waterheater via the local http-Endpoint

Tested with the "[Clage DSX Touch](https://www.clage.de/de/produkte/e-komfortdurchlauferhitzer/DSX-Touch)" with an integrated Homeserver

# Warning: WIP - Breaking changes possible
This is the first version of the API so there are still breaking chnages possible eg. output parameter names or values.

# Links
[Product Homepage](https://www.clage.de/de/produkte/e-komfortdurchlauferhitzer/DSX-Touch)

[API-Documentation](ttps://app.swaggerhub.com/apis/klacol/ClageHomeServer/1.0.0) 

[Project Homepage](https://github.com/klacol/clage_waterheater)

[PyPi Package](https://pypi.org/project/clage_waterheater/)

# Features
- Query Heater Status
- Set Heater Temperature

# Install

```
pip install clage_waterheater
```

# Example

```python
from clage_waterheater import clage_waterheater

heater = clage_waterheater('192.168.1.1','xxxxxxx') # <- change to your charger IP and your homeserver id
 
print (heater.requestStatus())
```
