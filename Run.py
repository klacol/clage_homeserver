from clage_homeserver import ClageHomeServer
clageHomeServer = ClageHomeServer('192.168.0.78','F8F005DB0CD7','2049DB0CD7') # <- change to your charger IP
 
print (clageHomeServer.requestStatus())

#clageHomeServer.setTemperature(456)

 