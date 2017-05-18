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
