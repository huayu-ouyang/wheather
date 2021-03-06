from flask import Flask, render_template, request
from twilio.rest import Client
from keys import *
import requests
import zipcode
import datetime
# import sqlalchemy
import os
# import pymysql
import schedule
import time
import threading
# pymysql.install_as_MySQLdb()

from uszipcode import ZipcodeSearchEngine

import multiprocessing
import math


app = Flask(__name__, static_folder="fullstack_template/static/dist", \
            template_folder="fullstack_template/static")

app.config['TEMPLATES_AUTO_RELOAD'] = 0


# app.config['SQLALCHEMY_DATABASE_URI'] = os.environ['SQLALCHEMY_DATABASE_URI']

# db = SQLAlchemy(app)

client = Client(account_sid, auth_token)

users = {}

# renders the index page
@app.route("/")
def index():
    return render_template("index.html")

# renders the info/message page
@app.route("/submit")
def submit():
    return render_template("submit.html")


@app.route("/_info",  methods = ['GET', 'POST'])
def driver():


    content = request.get_json()
    phone_num = "+1" + content['phonenum']
    location = content['zipcode'] 
    # pair = phoneNum(phonenum = phone_num, zipcode = location)

    # db.session.add(pair)
    # db.session.commit()

    '''
    if activeHours == None:
        db.session.insert(user).values(phone_num = phoneNumber, lastLocation = location)
    else:
        db.session.sql.insert(user).values(phone_num = phoneNumber, lastLocation = location, hours_awake  =activeHours)
    '''
    if not content['phonenum'].isdigit() or len(content['phonenum']) != 10:
        return 'Please enter a valid US phone number with the area code.'

    data = parser(location)
    if data == 'ERROR':
        return 'Sorry, we couldn\'t locate your zipcode. Try another one nearby.'
    weightedTempDays = results(data)
    outputStrs = languageOutput(weightedTempDays)

    users[phone_num] = location

    client.api.account.messages.create(
        to=phone_num,
        from_=fromNumber,
        body=outputStrs
        )

    return ""

def sendMessage():
    for i in list(users): 
        phone_num = i
        location = users[i]
        data = parser(location)
        if data == 'ERROR':
            return 'ERROR'
        weightedTempDays = results(data)
        outputStrs = languageOutput(weightedTempDays)

        client.api.account.messages.create(
            to= phone_num,
            from_= fromNumber,
            body=outputStrs
            )

# @app.route("/_confirm", method = ['POST'])
# def confirm(VerificationStatus):
#     if VerificationStatus == "success":
#         return "You have successfully verified your phone number"
#     else:
#         return "Sorry, we were not able to verify your phone number. Please try again"

# @app.route("/_sendMessage", method = ['POST'])
# def sendMessage():

#     client.api.account.messages.create(
#         to=phoneNumber,
#         from_= fromNumber,
#         body=outputStrs
#         )
#     return

# @app.route("/_verifyNumber", method = ['POST'])
# def verifyNumber(phoneNumber):
#     # validation_request = client.validation_requests \
#     #                        .create(phoneNumber)
#     validation_request = client.validation_requests \
#                            .create(phoneNumber, None, None, None, app.root_path+"/_confirm")

#     return validation_request.validation_code

def parser(location):
    ''' Parse the json for needed data'''
    # We are given an string of the zip.
    # to use the api, we need to change it to lat/lon

    search = ZipcodeSearchEngine()
    curZipcode = search.by_zipcode(location)
    # print(curZipcode)

    if curZipcode['City'] is None:
        return 'ERROR'
    lat = curZipcode['Latitude']
    lon = curZipcode['Longitude']

    # API url
    url = 'https://api.darksky.net/forecast/73e7ea4a962e1d8c65470b15ceda0965/'
    url = url + str(lat) + ',' + str(lon)

    # Calling the API and parsing it
    weather = get(url)
    if 'error' in weather:
        return 'ERROR'
    totalHourlyInfo = weather['hourly']
    hourlyData = totalHourlyInfo['data']
    # This is the relevent hourly data for the current location
    data = []
    for curHourData in hourlyData:
    # (time, apparentTemp, summary)
    # time is in unix timestamp, second counting from 1970 1/1
    # Summary is the condition
        condition = curHourData['icon']
        time = curHourData['time']
        apparentTemp = curHourData['apparentTemperature']
        uvIndex = curHourData['uvIndex']
        data.append((datetime.datetime.fromtimestamp(time), apparentTemp, condition, uvIndex, curZipcode['City']))
    return data

def results(data):
    '''This function looks at the apparent temperature, and decides the
        level of clothing needed. It will also note rainy, snowny, and sleey
        conditions'''
    weightedTempDays = []
    weightedTempOneDay = []

    # Perhaps allow user to enter in when they sleep or are more active?
    # can just shift the weights easily.
    N = 0.01
    weight = {0: N*2, 1: N, 2: N, 3: N, 4: N, 5: N, 6: N*2, 7: N*2, \
    8: N*2, 9: N*3, 10: N*4, 11: N*6, 12: N*8, 13: N*8, 14: N*8, 15: N*8, \
    16: N*7, 17: N*7, 18: N*7, 19: N*6, 20: N*5, 21: N*4, 22: N*3, 23: N*3}
    # counter = 0
    rain = False
    sleet = False
    snow = False
    uv = False
    for j in range(0, 23):
        # it would be nice if we can associate the time of the rain/snow/etc
        i = data[j]
        hour = i[0].hour
        day = i[0].day
        weightedTempOneDay.append(weight[hour]*i[1])
        # print(i[2])
        if i[3] > 5:
            uv = uv or True
        if i[2] == 'rain':
            rain = rain or True
        if i[2] == 'sleet':
            sleet = sleet or True
        if i[2] == 'snow':
            snow = snow or True
    weightTemp = sum(weightedTempOneDay)
    weightedTempOneDay = []
    level = 0
    if weightTemp <= 39:
        # winter coar and jacket
        level = 1
    elif weightTemp <= 55:
        # heavy coat
        level = 2
    elif weightTemp <= 69:
        # light jacket
        level = 3
    else:
        # t shirt mannnnn
        level = 4
        # i[1] is apparent temp, i[4] is city
    weightedTempDays.append((level, rain, sleet, snow, uv, weightTemp, i[4]))
        # if counter <= 24:
        #     rain = False
        #     sleet = False
        #     snow = False
        #     uv = False
        #     hour = i[0].hour
        #     day = i[0].day
        #     if counter == 24:
        #         counter = 0
        #         # How do we calculate the weighted temperature??
        #         # right now the placeholder for that is ...
        #         # Winter coat, jacket, boots, gloves, hats
        #         # print(weightedTempOneDay)
                
        #         weightTemp = sum(weightedTempOneDay)
        #         weightedTempOneDay = []
        #         level = 0
        #         if weightTemp <= 39:
        #             # winter coar and jacket
        #             level = 1
        #         elif weightTemp <= 55:
        #             # heavy coat
        #             level = 2
        #         elif weightTemp <= 69:
        #             # light jacket
        #             level = 3
        #         else:
        #             # t shirt mannnnn
        #             level = 4
        #             # i[1] is apparent temp, i[4] is city
        #         weightedTempDays.append((level, rain, sleet, snow, uv, weightTemp, i[4]))
        #     weightedTempOneDay.append(weight[hour]*i[1])
        #     print(i[2])
        #     if i[3] > 5:
        #         uv = True
        #     if i[2] == 'rain':
        #         rain = True
        #     if i[2] == 'sleet':
        #         sleet = True
        #     if i[2] == 'snow':
        #         snow = True
        #     counter += 1
    return weightedTempDays

def languageOutput(weightedTempDays):
    # print(weightedTempDays)
    '''Need a way to output in grammatically correct sentences'''
    day = weightedTempDays[0]    
    output = "It'll be about " + str(int(round(day[5]))) + "F" + " in " + day[6] + " today. "
    level = day[0]
    if level == 1:
        # do we also want to print out what the average temp or high/low temp is?
        output += "You should bundle up with a winter coat and jacket, gloves, hat, scarf, and boots.\n"
    elif level == 2:
        output += "You should probably wear a heavy jacket.\n"
    elif level == 3:
        output += "A light jacket should be sufficient.\n"
    elif level == 4:
        output += "It's t-shirt and shorts weather!\n"

    if day[1]:
        output += "It also looks like there might be rain, so wear rain boots and bring an umbrella!\n"
    elif day[2]:
        output += "It also looks like sleet today - wear snow boots!\n"
    elif day[3]:
        output += "It also might snow today - don't forget your hat and snow boots!\n"
    if day[4]:
        #do we want to print out what the UV index is/ what hours you should wear it
        output += "There's also a high UV index. Make sure to wear sunscreen, a hat, and sunglasses!\n"
    return output


# Get the jsoned weather data
def get(url):
    try:
        res = requests.get(url)
        return res.json()
    except:
        return False


@app.before_first_request
def activate_job():
    def run_job():
        while True:
            schedule.run_pending()
            time.sleep(1)
    thread = threading.Thread(target= run_job)
    thread.start()

def start_runner():
    def start_loop():
        not_started = True
        while not_started:
            print('In start loop')
            try:
                r = requests.get('http://moonlit-creek-187814.appspot.com/')
                if r.status_code == 200:
                    print('Server started, quitting start_loop')
                    not_started = False
                print(r.status_code)
            except:
                print('Server not yet started')
            time.sleep(2)

    print('Started runner')
    thread = threading.Thread(target=start_loop)
    thread.start()
if __name__ == "__main__":
    start_runner() 
    schedule.every().day.at("8:00").do(sendMessage)

    app.run(debug=True)
