# wundergroundPWS_info
Uses the apis to get historical wunderground data and presents in a user-friendly way
All you need to input in the python code is your station ID and your API.
There are some modules you will also need to make thie work

    wu = WUndergroundAPI(
        api_key="",  # input your the api key here
        default_station_id="",  # your station id
        units=units.ENGLISH_UNITS,
    )
    
    ![screenshot_basic](https://raw.githubusercontent.com/allenweiss/wundergroundPWS_info/images/basic_screen.png)
