from __future__ import print_function
import os.path
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials

import logging

logging.basicConfig(filename="std.log", format='%(asctime)s %(message)s',filemode='w') 
logger=logging.getLogger() 
logger.setLevel(logging.DEBUG)

 
logger.info("This is just an information for you")

from tkinter import *
import time

w=Tk()

w.title("Google Drive API TEST")
w.configure(bg="powder blue")


#w.after(1000,functionName )


###################### Frames ####################################################################

TopFrame=Frame(w,width=700,height=500,bg='powder blue')
TopFrame.pack(side=TOP)

TopFrame2=Frame(w,width=700,height=100,bg='powder blue')
TopFrame2.pack(side=TOP)

TopFrame3=Frame(w,width=700,height=400,bg='powder blue')
TopFrame3.pack(side=TOP)

###############################  TopFrame : title ###################################################################

name=Label(TopFrame,text='GDrive API TEST',font=('arial',15,'bold'),fg='Steel Blue',bg='powder blue',bd=5,anchor='w')
LocalTime=time.asctime(time.localtime(time.time()))
time=Label(TopFrame,text=LocalTime,font=('arial',10,'bold'),fg='steel blue',bg='powder blue',bd=5,anchor='w')

name.grid(row=0,column=0)
time.grid(row=1,column=0)

####################################  TopFrame2:Buttons ######################################################

# Methods

# File List 
# If modifying these scopes, delete the file token.json.
SCOPES = ['https://www.googleapis.com/auth/drive.metadata.readonly']

def getFileList():
    """Shows basic usage of the Drive v3 API.
    Prints the names and ids of the first 10 files the user has access to.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    service = build('drive', 'v3', credentials=creds)

    # Call the Drive v3 API
    results = service.files().list(
        pageSize=10, fields="nextPageToken, files(id, name)").execute()
    items = results.get('files', [])

    if not items:
        print('No files found.')
        Listbox.insert(1,"No Activity Found")
    else:
        resett()
        #print('Files:')
        count = 1 
        Listbox.insert(0,"  Serial No."+"     "+" Name "+"                "+" ID        " )
        for item in items:
            Listbox.insert(count,"  "+str(count)+"                    "+item['name']+"          "+item['id'] )
            #print(count," ",u'{0} ({1})'.format(item['name'], item['id']))
            logger.info(u'{0} ({1})'.format(item['name'], item['id']))
            count= count + 1





# Activity
# If modifying these scopes, delete the file token.json.
SCOPES2 = ['https://www.googleapis.com/auth/drive.activity.readonly']

def getActivityList():
    """Shows basic usage of the Drive Activity API.

    Prints information about the last 10 events that occured the user's Drive.
    """
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token2.json', SCOPES2)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials2.json', SCOPES2)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open('token2.json', 'w') as token:
            token.write(creds.to_json())

    service = build('driveactivity', 'v2', credentials=creds)

    # Call the Drive Activity API
    results = service.activity().query(body={
        'pageSize': 100
    }).execute()
    activities = results.get('activities', [])

    print("-----------------------------------")
    print(activities)
    print("-----------------------------------")

    if not activities:
        print('No activity.')
        Listbox.insert(1,"No Activity Found")
    else:
        resett()
        Listbox.insert(0,"Serial No."+"                "+" Time "+"                        "+" Action "+"              "+" Actor"+"            "+"Targets       " )
        count = 1
        for activity in activities:
            time = getTimeInfo(activity)
            action = getActionInfo(activity['primaryActionDetail'])
            actors = map(getActorInfo, activity['actors'])
            targets = map(getTargetInfo, activity['targets'])
           # print(u'{0}: {1}, {2}, {3}'.format(time, truncated(actors), action,truncated(targets)))
            Listbox.insert(count,"  "+str(count)+"             "+str(time)+"        "+(action)+"          "+truncated(actors)+"   "+truncated(targets))
            logger.info(str(count)+" , "+str(time)+" , "+(action)+" , "+truncated(actors)+" , "+truncated(targets))
            count = count + 1
            


# Returns a string representation of the first elements in a list.
def truncated(array, limit=2):
    array = list(array)
    contents = ', '.join(array[:limit])
    more = '' if len(array) <= limit else ', ...'
    return u'[{0}{1}]'.format(contents, more)


# Returns the name of a set property in an object, or else "unknown".
def getOneOf(obj):
    for key in obj:
        return key
    return 'unknown'


# Returns a time associated with an activity.
def getTimeInfo(activity):
    if 'timestamp' in activity:
        return activity['timestamp']
    if 'timeRange' in activity:
        return activity['timeRange']['endTime']
    return 'unknown'


# Returns the type of action.
def getActionInfo(actionDetail):
    return getOneOf(actionDetail)


# Returns user information, or the type of user if not a known user.
def getUserInfo(user):
    if 'knownUser' in user:
        knownUser = user['knownUser']
        isMe = knownUser.get('isCurrentUser', False)
        return u'people/me' if isMe else knownUser['personName']
    return getOneOf(user)


# Returns actor information, or the type of actor if not a user.
def getActorInfo(actor):
    if 'user' in actor:
        return getUserInfo(actor['user'])
    return getOneOf(actor)


# Returns the type of a target and an associated title.
def getTargetInfo(target):
    if 'driveItem' in target:
        title = target['driveItem'].get('title', 'unknown')
        return 'driveItem:"{0}"'.format(title)
    if 'drive' in target:
        title = target['drive'].get('title', 'unknown')
        return 'drive:"{0}"'.format(title)
    if 'fileComment' in target:
        parent = target['fileComment'].get('parent', {})
        title = parent.get('title', 'unknown')
        return 'fileComment:"{0}"'.format(title)
    return '{0}:unknown'.format(getOneOf(target))



def resett():
    Listbox.delete(0,Listbox.size())

# View

btnGetFiles=Button(TopFrame2,text='Flie List',font=("arial",10,"bold"),bg='powder blue',fg='black',width=7,bd=5,command=getFileList)
btnGetActivity=Button(TopFrame2,text='Activity',font=("arial",10,"bold"),bg='powder blue',fg='black',width=7,bd=5,command=getActivityList)
btnReset=Button(TopFrame2,text='Reset',font=("arial",10,"bold"),bg='powder blue',fg='black',width=7,bd=5,command=resett)

btnGetFiles.grid(row=1,column=1,padx=(10,10),pady=(10,10))
btnGetActivity.grid(row=1,column=2,padx=(10,10),pady=(10,10))
btnReset.grid(row=1,column=3,padx=(10,10),pady=(10,10))


####################################  TopFrame3:Listbox ######################################################


Listbox= Listbox(TopFrame3,width=100, bg="powder blue", bd=1, fg="blue")
Listbox.pack()



w.mainloop()

###############################################################  End  ##################################################################






