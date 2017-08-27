
from __future__ import print_function
import httplib2
import os

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage
import time
import serial 
import serial.tools.list_ports

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/gmail-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/gmail.readonly'
CLIENT_SECRET_FILE = 'client_secret.json'
APPLICATION_NAME = 'Gmail API Python Quickstart'


def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'gmail-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()


    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        print (flow)
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials
from apiclient import errors

def ListMessagesMatchingQuery(service, user_id, query=''):
    """List all Messages of the user's mailbox matching the query.

    Args:
      service: Authorized Gmail API service instance. 
      user_id: User's email address. 
      query: String used to filter messages returned. 

    Returns:
      List of Messages that match the criteria of the query.  
      The returned list contains Message IDs, use get with the ID
      to get the details of the Message. 

    """
    try:
        response = service.users().messages().list(userId=user_id, q=query).execute()
        messages = []
        if 'messages' in response:
            messages.extend(response['messages'])

        return messages
    except errors.HttpError, error:
        print ("An error occurred: %s" % error)

def GetMessage(service, user_id, msg_id):
  """Get a Message with given ID.

  Args:
    service: Authorized Gmail API service instance.
    user_id: User's email address. The special value "me"
    can be used to indicate the authenticated user.
    msg_id: The ID of the Message required.

  Returns:
    A Message.
  """
  try:
    message = service.users().messages().get(userId=user_id, id=msg_id).execute()

    print ('Message snippet: %s' % message['snippet'])

    return message
  except errors.HttpError, error:
    print ('An error occurred: %s' % error)

def main():
    """ loops through list of emails received and pings arduino if a new message is received
    """
    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    service = discovery.build('gmail', 'v1', http=http)
    ports = list(serial.tools.list_ports.comports())
    port = ""
    # looks for port associated with arduino 
    for p in ports:
        if 'Arduino' in p[1] or "Generic" in p[1]:
            port=p[0]

    starttime = time.time()
    prev = 0
    ser = serial.Serial(port, 9600)
    while True:
        hold = ListMessagesMatchingQuery(service, "me")
        if hold[0]!=prev:
            #print ("New Message")
            ser.write('1')
            prev = hold[0]
        else:
            ser.write('0')

        time.sleep(3.0 - ((time.time() - starttime)%3.0))



if __name__ == '__main__':
    main()