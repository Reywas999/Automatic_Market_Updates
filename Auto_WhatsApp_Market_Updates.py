#!/usr/bin/env python
# coding: utf-8

# In[ ]:


# This script acts as a template for future Whatsapp notification systems when I have something I actually want to be notified
# about. For now the script will send a message to my number at either 06:30 or 13:00 PST notifying me that the US stock market
# is either opening or closing. The script will also print out the total change in SPY from the previous day close to the current
# price. At market open this will display the change in after hours and pre-market, at close this will display the day-to-day
# change. Values displayed are both full dollar current price and percent change.
# The script does not account for holidays; its just a template script, so I'm not too concerned
# about the precision here...


# In[ ]:


# Necessary Imports
import requests # to retrieve the URL and send the message
import datetime # To figure out the current time and compare to the time I set to send the message
import pytz # To set the timezone to PST
import yfinance as yf # For retrieving SPY data

# Note, this script will run on a schedule using cronjobs -- sending a message at 06:30 am PST every weekday to signal the stock
# Market opening, and again at 1300 PST to signal the market closing.

# The Cron Expression:

# 30 6,13 * * 1-5
# |  |  | |  |
# |  |  | |  +----- Day of the week (1-5 = Monday to Friday)
# |  |  | +------- Any month
# |  |  +--------- Any day of the month
# |  +------------ Hours (6 and 13)
# +--------------- Minutes (30)


# In[ ]:


# Setting the timezone and API key from callmebot via Whatsapp
time_zone = pytz.timezone('US/Pacific')
phone_num = 'YOURPHONENUMBER'
API_Key = 
open_message = 'Ding Ding! The US Stock Market is open!'
close_message = 'Ding Ding! The US Stock Market is closed!'


# In[ ]:


def get_spy_data():
    '''
    This function will likely raise an error over holidays. Fix with try perhaps.
    '''
    try:
        # Get the data for SPY
        spy = yf.Ticker("SPY")
        data = spy.history(period="2d")

        # Get the current price and previous close price
        current_price = data['Close'][1]
        previous_close_price = data["Close"][0]

        # Calculate the dollar and percent change
        dollar_change = current_price - previous_close_price
        percent_change = (dollar_change / previous_close_price) * 100
    except:
        current_price = 'NaN'
        dollar_change = 'NaN'
        percent_change = 'NaN'
    
    return current_price, dollar_change, percent_change


# In[ ]:


def send_notification(API = API_Key, phone_num = phone_num):
    '''
    Should there be a lag when sending the request, it is highly possible that the closing notification will be sent in error,
    but this is again a template script for the future...
    '''
    # Retrieving the SPY data 
    current_price, dollar_change, percent_change = get_spy_data()
    
    message_open = (open_message + 
                   f" The current price of SPY is ${current_price:.2f}" +
                   f" The dollar change from yesterday's close is ${dollar_change:.2f}" +
                   f" The percent change from yesterday's close is {percent_change:.2f}%")
    
    message_close = (close_message + 
                   f" The current price of SPY is ${current_price:.2f}" +
                   f" The dollar change from yesterday's close is ${dollar_change:.2f}" +
                   f" The percent change from yesterday's close is {percent_change:.2f}%")
    
    # Set the time zone
    time_zone = pytz.timezone('US/Pacific')

    # Set the time to send the market open notification
    open_notification_time = datetime.time(hour=6, minute=30)
    
    # Setting an arbitrary midday time to buffer a lagging request
    midday = datetime.time(hour=9, minute=45)
    
    # Set the time to send the market closed notification
    close_notification_time = datetime.time(hour=13, minute=0)

    # Get the current time in the specified time zone
    current_time = datetime.datetime.now(time_zone)
    
    # Setting the URL to send the message
    url = "https://api.callmebot.com/whatsapp.php?phone=whatsapp_number&text=your_message&apikey=KEY"
    url = url.replace('KEY', str(API))
    url = url.replace('whatsapp_number', phone_num)
    
    # Check the time to see if the market is opening or closing
    if current_time.time() >= open_notification_time and current_time.time() < midday:
        # Send the market open message
        url = url.replace("your_message", message_open)
        requests.get(url)
    else:
        # Send the market close message
        url = url.replace("your_message", message_close)
        requests.get(url)


# In[ ]:


send_notification()

