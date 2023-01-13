# wundergroundPWS_info

If you connect a weather station to Wunderground, this is a very simple way to see your data over time in a user-friendly way, plus get a forecast.

This script uses the wunderground apis to get historical and current wunderground data for your station and presents the results.  It also gives you forecasts for your specific area.
All you need to input in the python code is your station ID, your API and an estimate of how many weeks of data you have at Wunderground (see below in Set Up.  You also need to provide longitude and latitude information.  This can be found on a google map.  Simply find your location on the map, right click and you'll see the longitude and latitude.  Simple insert that as below (comma separated). There are also a few modules you will also need to make this work.

### Set Up

See below for the data you need:

    weeks_past = n  # how many weeks in the past do you have data
    wu = WUndergroundAPI(
        api_key="",  # input your the api key here
        default_station_id="",  # your station id
        units=units.ENGLISH_UNITS,
    )
	
	const={
	 'coord':'',    # you longitude and latitude for the forecast
	}
	

Import the following modules: datetime, simple_term_menu, colorama, urllib3, json

### Usage

You simply run python3 weather.py and, using the tab selector, choose how many days or weeks of data you want to analyze (this example uses 5 weeks of past data). 

<img width="204" alt="choice_screen" src="https://user-images.githubusercontent.com/1487109/211220200-84bf69f5-339d-41f2-a5de-e79ca691b8fa.png">


### Result

If you select the past 21 days, for example, you will get a result something like this:

<img width="683" alt="results_screen" src="https://user-images.githubusercontent.com/1487109/211218144-5b61b728-6748-4e8f-9396-1f53fd3089ec.png">
