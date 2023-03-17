from datetime import date
from pprint import pprint
from simple_term_menu import TerminalMenu
from wunderground_pws import WUndergroundAPI, units
from datetime import datetime, timedelta
from itertools import cycle
import json
import urllib3
import colorama
from colorama import Fore, Back, Style
import csv, os, sys, time
import os.path
import time

colorama.init(autoreset=True)
http = urllib3.PoolManager()

# *********SET UP *******************

weeks_past = 11  # how many weeks in the past do you want to examine

wu = WUndergroundAPI(
    api_key="9c0e747f7a9b4fdd8e747f7a9b5fdd89",  # the api key
    default_station_id="KCASANTA4208",  # your station id
    units=units.ENGLISH_UNITS,
)

const={
 'coord':'34.45,-119.70',    # your longitude and latitude for the forecast
}

# *********END SET UP *******************


dow = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

dt = datetime.now()

dayNumber = dt.weekday()


today = datetime.today()

tmp = datetime.now() - timedelta(days=weeks_past * 7)

date_asked = tmp.strftime("%m-%d")


def getWeekEnds():
    arr = []
    for i in range(2, weeks_past + 1):
        arr.append(i * 7)
    return arr


def getDropDown():
    a = []
    l = getWeekEnds()
    for i in [*range(1, 8), *l]:
        if i == 1:
            wrds = "Today"
        else:
            wrds = str(i) + " Days Ago to Now"
        idx = "[" + str(i) + "] " + wrds
        a.append(idx)
    return a


def last_n_days(day, n):
    days_past = weeks_past * 7
    result = []
    x = min(n, days_past)
    for i in range(x, 0, -1):
        result.append((day + 1 - i) % 7)
    return result


def dayDropDown():
    import re

    options = getDropDown()
    terminal_menu = TerminalMenu(
        options,
        title="How Many Days Total",
        exit_on_shortcut=False,
        show_shortcut_hints_in_status_bar=False,
    )
    menu_entry_index = terminal_menu.show()
    ref = options[menu_entry_index]
    s = re.findall(r"\b\d+\b", ref)
    return s[0]


def lastnElements(n):
    arr1 = [0, 1, 2, 3, 4, 5, 6]
    k = weeks_past
    element_list = arr1 * k
    res = element_list[-n:]
    return res


def chooseHist():
    if "-s" in sys.argv:   
        main([dayNumber],lastnElements(1))
    n = int(dayDropDown())
    rng = last_n_days(dayNumber, n)
    elem = lastnElements(n)
    main(rng,elem)



def minmax():
    url=(
    "https://api.weather.com/v2/pws/observations/all/1day?stationId="
    + wu.default_station_id
    + "&format=json&units=e&apiKey="
    + wu.api_key
    + ""
    )
    resp = http.request("GET", url)
    data = resp.data
    ccurrent_ov = json.loads(data)
    ct=ccurrent_ov['observations']

    rs=len(ct)
    #ct[i]['obsTimeLocal']
    arr=[]
    ind=[]
    for i in range(0,rs):
        if ct[i]['imperial']['precipRate']==None:
            precip=0
        else:
            precip=ct[i]['imperial']['precipRate']
        arr.append(precip)
        ind.append(ct[i]['obsTimeLocal'])
    maxr=max(arr)
    index = arr.index(maxr) 
    indTime=ind[index]
    indTime=datetime.fromisoformat(indTime)
    time=indTime.strftime('%-I:%M %p')
    return maxr, time
    
    
def PrecipIndicator(n):
    n=float(n)
    if n>0:
        out=Fore.CYAN + str(n) + Style.RESET_ALL
    else:
        out=n
    rs="Precipitation rate = "+str(out)+" inches per hour"
    return rs
    

def nonzero(n):
    n=float(n)
    if n>0:
        out=Fore.CYAN +str(n) +Style.RESET_ALL
    else:
        out=n
    rs=str(out) 
    return rs
    
def main(rng,elem):
    #print(rng)
    #print(elem)
    #exit(0)
    dt2=datetime.now()
    dayTime = dt2.strftime("%-I:%M %p")
    tot = 0
    note = 0
    flag=0
    arr_date = []
    ct = len(rng)
    print()
    print('********************')
    print()
    for index, i in enumerate(rng):

        tdx = datetime.now() - timedelta(days=ct - index - 1)  # days ago
        td = tdx.strftime("%Y%m%d")
        td_i = tdx.strftime("%b-%-d")
        url = (
            "https://api.weather.com/v2/pws/history/daily?stationId="
            + wu.default_station_id
            + "&format=json&units=e&date="
            + td
            + "&apiKey="
            + wu.api_key
            + ""
        )

        resp = http.request("GET", url)

        data = resp.data

        ccurrent_tp = json.loads(data)

        if len(ccurrent_tp["observations"]) == 0:  # check to see if the return is empty
            note = 1
            continue

        arr_date.append(
            td_i
        )  # used to get active data points - used to identify first data point

        ccurrent = ccurrent_tp["observations"][0]

        if dow[i] == dow[dayNumber] and index == len(rng) - 1:
            wkday = "Today"
            flag=1
        else:
            wkday = str(dow[i]) + " - " + td_i
        h = elem[index]
        if flag==0:
            tot = tot + ccurrent["imperial"]["precipTotal"]
            print(nonzero(ccurrent["imperial"]["precipTotal"])+ " - " + wkday)
     #https://api.weather.com/v2/pws/observations/all/1day?stationId=KCASANTA4208&format=json&units=e&apiKey=9c0e747f7a9b4fdd8e747f7a9b5fdd89

       
    url2 = (
        "https://api.weather.com/v2/pws/observations/current?stationId="
        + wu.default_station_id
        + "&format=json&units=e&apiKey="
        + wu.api_key
        + ""
    )
    resp2 = http.request("GET", url2)
    data2 = resp2.data
    ccurrent_tp2 = json.loads(data2)
    ccurrent2 = ccurrent_tp2["observations"][0]

    tot = tot + ccurrent2["imperial"]["precipTotal"]
    print(nonzero(ccurrent2["imperial"]["precipTotal"])+ " - " + wkday)
    print()
    if rng!=[0]:
        print("Accumulated Rain Total = " + nonzero(str("%.2f" % tot)) + " inches since " +str(arr_date[0]))
        print()
    print(Fore.CYAN + "CURRENT CONDITIONS @ "+dayTime)
    print(str("Today's rain total = " + str(ccurrent2["imperial"]["precipTotal"])))
    prate=ccurrent2["imperial"]["precipRate"]
    print(PrecipIndicator(prate))
    maxr,time=minmax()
    print(f"Highest precipitation rate today = {maxr} inches per hour at {time}")
    temp = str(ccurrent2["imperial"]["temp"])
    print(f"Temperature = {temp}\N{DEGREE SIGN}")
    windgust = str(ccurrent2["imperial"]["windGust"])
    windspeed = str(ccurrent2["imperial"]["windSpeed"])
    print(f"Wind speed = {windspeed} mph and wind gust = {windgust} mph")
    print()
    earliest_date = arr_date[0]
    if note == 1:
        print(
            Fore.RED
            + f"Note that one or more historical days are missing due to a lack of data.\nThe earlist date with your data is {earliest_date} but you requested {date_asked}.\n"
        )
    print('https://www.wunderground.com/dashboard/pws/KCASANTA4208')
    fc=str(input('See a forecast (f), search a date (d), rain since..(h), start again (s), exit (x) or hit return to refresh? ') or 'a')
 
    if fc=='f':
        weatherForecast(6)
        exit(0)
    elif fc=='a':
        main([dayNumber],elem)
    elif fc=='d':
        searchHist()
    elif fc=='s':
        chooseHist()
    elif fc=='h':
        getAllDates()
    elif fc=='x':
        exit(0)
 
 
def weatherForecast(n):
     url='https://api.weather.com/v3/wx/forecast/daily/5day?geocode='+const['coord']+'&format=json&units=e&language=en-US&apiKey='+wu.api_key
     resp = http.request("GET", url)
     data = resp.data
     forecast = json.loads(data)
     print()
     print("***************FORECAST********************")
     print()
     #print('******************')
     #print('TODAY')
     #print('******************')
     for i in range(0,n):
         
         if str(forecast['daypart'][0]['dayOrNight'][i])=='N':
             print('NIGHT')
         elif str(forecast['daypart'][0]['dayOrNight'][i])=='D':
             print('******************')
             print(forecast['daypart'][0]['daypartName'][i].upper())
             print('******************')
             print("DAY")
         else:
             print('**********TODAY**********')
    
         #print(forecast['daypart'][0]['daypartName'][i])
         print(str(forecast['daypart'][0]['precipChance'][i])+'%')
         print(forecast['daypart'][0]['precipType'][i])
         print()
     if n==6:
         lf=input("Longer forecast (y) or b: " or exit(0))
         if lf=='y' :
             weatherForecast(11)
         elif lf=='b':
             main([dayNumber],lastnElements(1))
             exit(0)
     else:
         main([dayNumber],lastnElements(1))
 

def getAllDates():
    from datetime import date, timedelta
    print()
    totalPrecip=0
    print("What is beginning date?")
    yr=input("Year (YYYY):")
    mo=input("Month (MM):")
    dy=input("Day (DD): ")
    start_date = date(int(yr), int(mo), int(dy)) 
    endDate_yr= datetime.now().year
    endDate_mo= datetime.now().month
    endDate_day= datetime.now().day
    end_date=date(endDate_yr,endDate_mo,endDate_day)

    
    
    delta = end_date - start_date   # returns timedelta

    for i in range(delta.days + 1):
        day = start_date + timedelta(days=i)
   
        td=str(day.year)+str('%02d' % day.month)+str('%02d' % day.day)

        url = (
            "https://api.weather.com/v2/pws/history/daily?stationId="
            + wu.default_station_id
            + "&format=json&units=e&date="
            + td
            + "&apiKey="
            + wu.api_key
            + ""
        )

        resp = http.request("GET", url)
        data = resp.data
        ccurrent = json.loads(data)
        if len(ccurrent["observations"]) == 0:  # check to see if the return is empty
            print("You do not have data for this date")
            exit(0)

        obs=ccurrent["observations"][0]
        totPrecip=obs['imperial']['precipTotal']
        totalPrecip+=totPrecip
    print()
    print(format(totalPrecip,'.2f')+' inches')
    print('Over '+str(i)+' days')
    print()
        

def searchHist():
     print()
     yr=input("Year (YYYY): ")
     mo=input("Month (MM): ")
     dy=input("Day (DD): ")
     
     if len(str(yr))!=4 or len(str(mo))!=2 or len(str(dy))!=2:
         print('You need to put in the correct format for the numbers.  Try again')
         yr=input("Year (YYYY):")
         mo=input("Month (MM):")
         dy=input("Day (DD): ")
     
     td=str(yr)+str(mo)+str(dy)
     
     url = (
         "https://api.weather.com/v2/pws/history/daily?stationId="
         + wu.default_station_id
         + "&format=json&units=e&date="
         + td
         + "&apiKey="
         + wu.api_key
         + ""
     )

     resp = http.request("GET", url)


     data = resp.data

     ccurrent = json.loads(data)
     if len(ccurrent["observations"]) == 0:  # check to see if the return is empty
         print("You do not have data for this date")
         
     else:
         obs=ccurrent["observations"][0]
         print()
         print('Total precipitation: '+str(obs['imperial']['precipTotal']))
         print('Max precipitation rate: '+str(obs['imperial']['precipRate']))
         print()
     fc=str(input('Back to today (b) or search another date (s) ') or 'a')
     if fc=='b':
         main([dayNumber],lastnElements(1))
     elif fc=='s':
         searchHist()
     elif fc=='x':
         exit(0)
     
     
     

if __name__ == "__main__":
    chooseHist()

    