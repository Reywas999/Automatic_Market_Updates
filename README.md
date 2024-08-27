# Automatic_Market_Updates
Requisites: Whatsapp chatbot API, phone number
\
This script acts as a template for future Whatsapp notification systems when I have something I actually want to be notified
about.\
\
For now the script will send a message to your whatsapp number at 06:30 and 13:00 PST notifying you that the US stock market
is either opening or closing. The script will also print out the total change in SPY from the previous day close to the current
price. At market open this will display the change in after hours and pre-market, at close this will display the day-to-day
change. Values displayed are both full dollar current price and percent change.
The script does not account for holidays; its just a template script.\
\
\
FOR USE WITH CRON JOBS:\
\
This script will run on a schedule using cronjobs -- sending a message at 06:30 am PST every weekday to signal the stock
market opening, and again at 1300 PST to signal the market closing.

### The Cron Expression:

30 6,13 * * 1-5\
|  |  | |  |\
|  |  | |  +----- Day of the week (1-5 = Monday to Friday)\
|  |  | +------- Any month\
|  |  +--------- Any day of the month\
|  +------------ Hours (6 and 13)\
+--------------- Minutes (30)
