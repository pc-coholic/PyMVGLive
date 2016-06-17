#-*- coding: UTF-8 -*-
import requests
import json
import sys
import datetime
try:
  unicode
except NameError:
  unicode = str

class MVGLive(object):
  def getlivedata(self, station, entries = 10, ubahn = True, tram = True, bus = True, sbahn = True):
    productsymbolsurl = 'http://www.mvg-live.de/MvgLive/images/size30/produkt/'
    linesymbolsurl = 'http://www.mvg-live.de/MvgLive/images/size30/linie/'

    if unicode == str:
        # Workaround for Python 3
        station_str = station.encode('utf-8').decode('iso-8859-1')
    else:
        station_str = station

    s = requests.Session();

    # Depatures
    payload = ("7|0|8|http://www.mvg-live.de/MvgLive/mvglive/|"
              "20589F56B19C8B1615F7A32F69557CD5|"
              "de.swm.mvglive.gwt.client.departureView.GuiAnzeigeService|"
              "getDisplayAbfahrtinfos|java.lang.String/2004016611|I|Z|"
              + station_str  + "|1|2|3|4|7|5|6|6|7|7|7|7|8|0|" + str(entries) + "|"
              + str(int(ubahn)) + "|" + str(int(tram)) + "|" + str(int(bus)) + "|" + str(int(sbahn)) + "|")
    headers = {'Content-Type': 'text/x-gwt-rpc; charset=utf-8'}
    r = s.post("http://www.mvg-live.de/MvgLive/mvglive/rpc/guiAnzeigeService", data = payload, headers = headers)

    if (r.text[:4] == '//OK'):
      data = r.text[4:]
      data = data.replace("'", '"')
      data = json.loads(data)
      stringmap = data[-3]
      stringmap.insert(0, "unused")
      objectmap = data[3:-9]
      objectmap.reverse()
      firstdeparture = data[-9] # The first timestamp is actually the first departure-time, the last one the current time
    else:
      raise(ValueError('Returned Data is not //OK - Aborting.'))

    # Current Time
    payload = "7|0|4|http://www.mvg-live.de/MvgLive/mvglive/|5E1CA9FD268C6C532BCB96DB76FF670A|de.swm.mvglive.gwt.client.clock.ClockService|getCurrentDate|1|2|3|4|0|"
    r = s.post("http://www.mvg-live.de/MvgLive/mvglive/rpc/clockService", data = payload, headers = headers)

    if (r.text[:4] == '//OK'):
      data = r.text[4:]
      data = data.replace("'", '"')
      data = json.loads(data)
      currenttime = data[0]
    else:
      raise(ValueError('Returned Data is not //OK - Aborting.'))


    # Put all departures in separated arrays
    objects = []
    objects.append([])
    i = 0
    for field in objectmap:
      objects[i].append(field)
      if isinstance(field, unicode):
        i += 1
        if field != objectmap[-1]:
          objects.append([])

    # if first object is empty, there are no results in this set
    # there is also another way to check this using the headers, but I forgot how...
    if (len(objects[0]) == 0):
      return []

    # Move departuretime from offset (last departure is actually first, first = second, ...
    for i in range(len(objects)-1, 0, -1):
      objects[i][-1] = objects[i-1][-1]
    objects[0][-1] = firstdeparture

    #Get the actual data
    departures = []
    for objectgroup in objects:
      departure = {}

      if objectgroup[1] < 0:
        base = -1
      else:
        base = 0

      departure['linesymbol'] = stringmap[objectgroup[base + 3]]
      departure['linesymbolurl'] = linesymbolsurl + stringmap[objectgroup[base + 3]]
      departure['linename'] = stringmap[objectgroup[base + 4]]
      departure['productsymbol'] = stringmap[objectgroup[base + 5]]
      departure['productsymbolurl'] = productsymbolsurl + stringmap[objectgroup[base + 5]]
      departure['product'] = stringmap[objectgroup[base + 5]].replace(".gif", "")
      departure['direction'] = stringmap[objectgroup[base + 6]]
      departure['destination'] = stringmap[objectgroup[base + 9]]
      #departure['time'] = objectgroup[-1]
      departure['time'] = self.getDeparture(currenttime, objectgroup[-1])

      departures.append(departure)

    return departures

  def getDeparture(self, current, departure):
    departure = ( self.longFromBase64(departure) - self.longFromBase64(current) ) / 1000 // 60

    if departure < 0:
      return 0
    else:
      return departure

  # Adapted from https://github.com/dice-cyfronet/gwt-proxy/blob/master/src/com/gdevelop/gwt/syncrpc/Utils.java
  def longFromBase64(self, value):
    longval = self.base64Value(value[0])
    value = value[1:]
    for i in value:
      longval <<= 6
      longval |= self.base64Value(i)

    return longval

  def base64Value(self, digit):
    if ( (ord(digit) >= ord('A')) and (ord(digit) <= ord('Z')) ):
      return ord(digit) - ord('A')
    elif (  (ord(digit) >= ord('a')) and (ord(digit) <= ord('z')) ):
      return ord(digit) - ord('a') + 26
    elif ( (ord(digit) >= ord('0')) and (ord(digit) <= ord('9')) ):
      return ord(digit) - ord('0') + 52
    elif (digit == '$'):
      return 62
    elif (digit == '_'):
      return 63
    else:
      pass
