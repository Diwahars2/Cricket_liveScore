#Parser for html
from lxml import html
#For Notifications on your desktop
#from gi.repository import Notify
import requests
import time
#download the cricbuzz library and do pip install cricbuzz
from cricbuzz import *
#The Twilio API
from twilio.rest import TwilioRestClient

#Enter your Twilio account SID and Auth Token
accountSid = "ACa9b3e81772d45e7ef13da76e0cd907f3"
authToken = "6c5cfe377eb5ff9b79ddf1a371320178"

#Calling the Cricbuzz Parser from cricbuzz.py
cric = CricbuzzParser()
#Calling the Twilio API
twilioClient = TwilioRestClient(accountSid, authToken)
#Enter your phone number and that of the receiver
myTwilioNumber = "+1201-992-8417"
destCellPhone = "+919901035150"

#Special parser for test matches
def test(**match):
#Takes a dict as input
 if match['State']=='Result':
   #Generates the message
   s = match['Match']+ "Test Match at "+match['Venue']+"\n"+match['Status']
   return s

def func():
 #Gets the XML file from Cricbuzz
 match = cric.getXml()
 details = cric.handleMatches(match)
 #Parses it and filters the None Type Elements
 details = filter(None,details)
 print details
 message = ''
 count=0
 for i in details:
 #Traverses the list
      if i['Match Format']=='TEST':
      #If it is a test match, sends it to the special function
         count+=1
         #generates the message from test()
         message = test(**i)
      #elif 'Match State' in i:
      elif i['Match State'] == 'inprogress' or i['Match State']=='rain':
          #If the match is in progress
             count+=1
             print count
             #Generate an appropriate message when a match is in progress
             message = message+"\n\n"+ i['Team']+ "      "+ i['Match Format'] + ' Match at ' + i['Venue']+  "\n" +i['Batting team'] + ' ' + i['Batting Team Runs'] +'/'+i['Batting Team Wickets'] + '  Overs: ' + i['Batting Team Overs'] + "\n" + i['Match Status']
    #  elif (i['Match State'] == 'complete' or i['Match State'] == 'result' or i['Match State'] == 'Result'):
         #Displays the result of already complete matches
     #        message =message+"\n\n"+i['Team']+"          "+ i['Match Format'] + ' Match at ' + i['Venue']+"\n"+i['Match Status']
      #       count+=1
 if count == 0 :
 #If no match is in progress, or if there is no other data to show
     message='No Match Available'
 #Notify.init("Live Scores")
 #Initialise Notify
 #Notify.Notification.new("Score Update: ",message).show()
 #Displaying the notification
 myMessage = twilioClient.messages.create(to = "+919901035150", from_="+12019928417", body = "Score Update:" + message)
 #Sending a text message via Twilio
 if not message == 'No Match Available':
   time.sleep(600)
   #Defines a time interval of 60 seconds
 else:
   #If no match is available, it quits the script
   exit()
while True:
 func()