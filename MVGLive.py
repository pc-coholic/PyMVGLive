#-*- coding: UTF-8 -*-
import requests
import json
import sys

def getlivedata(station, entries = 10, ubahn = True, tram = True, bus = True, sbahn = True):
  productsymbolsurl = 'http://www.mvg-live.de/MvgLive/images/size30/linie/'
  linesymbolsurl = 'http://www.mvg-live.de/MvgLive/images/size30/produkt/'

  s = requests.Session();
  payload = ("7|0|8|http://www.mvg-live.de/MvgLive/mvglive/|"
            "D6A616B1901EA7F258D3F1C9A20942A1|"
            "de.swm.mvglive.gwt.client.departureView.GuiAnzeigeService|"
            "getDisplayAbfahrtinfos|java.lang.String/2004016611|I|Z|" 
            + station  + "|1|2|3|4|7|5|6|6|7|7|7|7|8|0|" + str(entries) + "|"
            + str(int(ubahn)) + "|" + str(int(tram)) + "|" + str(int(bus)) + "|" + str(int(sbahn)) + "|")
  headers = {'Content-Type': 'text/x-gwt-rpc; charset=utf-8'}
  r = s.post("http://www.mvg-live.de/MvgLive/mvglive/rpc/guiAnzeigeService", data = payload, headers = headers)
  
  if (r.text[:4] == '//OK'):
    data = r.text[4:]
    data = data.replace("'", '"')
    data = json.loads(data)
    stringmap = data[-3]
    stringmap.insert(0, "unused")
    #objectmap = data[3:-3] # With timemap
    objectmap = data[3:-9]
    objectmap.reverse()
  else:
    sys.exit('Returned Data is not //OK - Aborting.')

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
    departure['time'] = objectgroup[-1]

    departures.append(departure)

  return departures
