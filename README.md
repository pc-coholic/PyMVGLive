PyMVGLive
=========

Python-Library to get live-data from mvg-live.de - yet another workaround the official, non-released API....


## MVGLive.getlivedata()
Retrieve the next departures from mvg-live.de

Configuration variables:
 
- **station** (*Required*): Name of the stop or station. Visit [the MVG live web site](http://www.mvg-live.de) to find valid names.
    
- **timeoffset** (*Optional*): Do not display connections departing sooner than this number of minutes (defaults to 0). Useful if you are a couple of minutes away from the stop.
    
- **entries** (*Optional*): Number of entries to retrieve (defaults to 10).
    
- **ubahn** (*Optional*): If 'False', do not display U-Bahn (subway) departures
    
- **tram** (*Optional*): If 'False', do not display tram departures
    
- **bus** (*Optional*): If 'False', do not display bus departures
    
- **sbahn** (*Optional*): If 'False', do not display S-Bahn (suburban train) departures

## MVGLive.getdisruptiondata()
Retrieve current disruptions/status messages from mvg-live.de. Returns headline and description of disruption.

Please note, that this call will execute another API-request and might cause problems with rate-limits imposed by the webservice.

For a saver way, please use [RSS-feed](http://www.mvg-mobil.de/Tickerrss/CreateRssClass) that is also provided by the MVG. You can find a sample implementation [here](https://github.com/muccc/anzeigr/blob/master/current_nodes/mvgdefas/ticker/getmvgticker.py)