#Parser for html
from lxml import html
#For Notifications on your desktop
from gi.repository import Notify
import requests
import time
from cricbuzz import *
from twilio.rest import TwilioRestClient

#Enter your Twilio account SID and Auth Token
accountSid = ""
authToken = ""
#Calling the Cricbuzz Parser from cricbuzz.py
cric = CricbuzzParser()
#Calling the Twilio API
twilioClient = TwilioRestClient(accountSid, authToken)
#Enter your Sender and receiver number
myTwilioNumber = "xxxx"
destCellPhone = "yyyy"

def func():
 #Gets the XML file from Cricbuzz
 match = cric.getXml()
 details = cric.handleMatches(match)
 #Parses it and filters the None Type Elements
 details = filter(None,details)
 message = ''
 count=0
 for i in details:
 #Traverses the list
      if i['Match Format']=='TEST':#added this only to get IND vs WI match score --> and (i['Batting team'] == 'IND' or i['Batting team'] == 'WI') and i['State'] != 'stump':
         count+=1
         message =  i['State']+'-'+ i['Match Format'] + '-' +' Match at: ' + i['Venue']+  "\n" +i['Batting team'] + ': ' + i['Batting Team Runs'] +'/'+i['Batting Team Wickets']
         print message
      elif 'Match State' in i:
         if i['Match State'] == 'inprogress' or i['Match State']=='rain':
          #If the match is in progress
             count+=1
             #Generate an appropriate message when a match is in progress
             message = message+"\n\n"+ i['Team']+ "      "+ i['Match Format'] + ' Match at ' + i['Venue']+  "\n" +i['Batting team'] + ' ' + i['Batting Team Runs'] +'/'+i['Batting Team Wickets'] + '  Overs: ' + i['Batting Team Overs'] + "\n" + i['Match Status']
         elif (i['Match State'] == 'complete' or i['Match State'] == 'result' or i['Match State'] == 'Result'):
         #Displays the result of already complete matches
             message =message+"\n\n"+i['Team']+"          "+ i['Match Format'] + ' Match at ' + i['Venue']+"\n"+i['Match Status']
             count+=1
 if count == 0 :
 #If no match is in progress, or if there is no other data to show
     message='No Match Available'
 Notify.init("Live Scores")
 #Initialise Notify
 Notify.Notification.new("Score Update: ",message).show()
 #Displaying the notification
 myMessage = twilioClient.messages.create(body = "Score Update:" + message, from_=myTwilioNumber, to=destCellPhone)
 #Sending a text message via Twilio
 if not message == 'No Match Available':
   time.sleep(3600)
   #Defines a time interval of 3600 seconds
 else:
   #If no match is available, it quits the script
   exit()
while True:
 func()
