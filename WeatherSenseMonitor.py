from __future__ import print_function
import traceback
import apscheduler.events
from apscheduler.schedulers.background import BackgroundScheduler
import time
import MySQLdb as mdb
import wirelessSensors
import sys
from datetime import datetime
import pytz

SOFTWAREVERSION = "V021"


try:
    import conflocal as config
except ImportError:
    import config


# WeatherSense SQL Database
try:

    con = mdb.connect(
        "localhost",
        "root",
        config.MySQL_Password,
        "WeatherSenseWireless"
    )

except BaseException:
    # print(traceback.format_exc())
    print("--------")
    print("MySQL Database WeatherSenseWireless Not Installed.")
    print("Run this command:")
    print("sudo mysql -u root -p < WeatherSenseWireless.sql")
    print("WeatherSenseMonitor Stopped")
    print("--------")
    sys.exit("WeatherSenseMonitor Requirements Error Exit")

# Check for updates having been applied
try:

    con = mdb.connect(
        "localhost",
        "root",
        config.MySQL_Password,
        "WeatherSenseWireless"
    )
    cur = con.cursor()
    query = "SELECT * FROM RAD433MHZ"
    cur.execute(query)

except BaseException:
    # print(traceback.format_exc())
    print("--------")
    print("MySQL Database WeatherSenseWireless Updates Not Installed.")
    print("Run this command:")
    print("sudo mysql -u root -p WeatherSenseWireless < updateWeatherSenseWireless.sql")
    print("WeatherSenseMonitor Stopped")
    print("--------")
    sys.exit("WeatherSenseMonitor Requirements Error Exit")


print("-----------------")
print("WeatherSense Monitoring Software")
print("Software Version ", SOFTWAREVERSION)
print("-----------------")


##########
# set up scheduler


# Scheduler Helpers

# print out faults inside events
def ap_my_listener(event):
    if event.exception:
        print(event.exception)
        print(event.traceback)


scheduler = BackgroundScheduler()

# for debugging
scheduler.add_listener(ap_my_listener, apscheduler.events.EVENT_JOB_ERROR)

# read wireless sensor package
scheduler.add_job(wirelessSensors.readSensors)  # run in background

scheduler.print_jobs()

# start scheduler
scheduler.start()
print("-----------------")
print("Scheduled Jobs")
print("-----------------")
scheduler.print_jobs()
print("-----------------")


# Main Loop

while True:

    time.sleep(1.0)
    newYorkTz = pytz.timezone("America/New_York") 
    easternTime = datetime.now(newYorkTz)
    currentTime = easternTime.strftime("%H:%M")

    if (currentTime == "23:58" or currentTime == "23:59") :
       sys.exit("Daily Restart")
