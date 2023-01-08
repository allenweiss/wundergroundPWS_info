# wundergroundPWS_info
Uses the apis to get historical wunderground data and presents in a user-friendly way
All you need to input in the python code is your station ID and your API.
There are some modules you will also need to make thie work

    wu = WUndergroundAPI(
        api_key="",  # input your the api key here
        default_station_id="",  # your station id
        units=units.ENGLISH_UNITS,
    )
    
### Usage

Then you simply run python3 weather.py  

<img width="379" alt="choice_screen" src="https://user-images.githubusercontent.com/1487109/211218104-4d003369-68a3-4025-93ac-f9733cdeac70.png">

### Result

You will get a result something like this:

<img width="683" alt="results_screen" src="https://user-images.githubusercontent.com/1487109/211218144-5b61b728-6748-4e8f-9396-1f53fd3089ec.png">
