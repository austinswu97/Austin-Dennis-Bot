# page access token for "test test test"
# EAAG44FaYQtQBAFWmt3wxGHFRE9HMEJymZBFLWPQoSEDPp9WUdPBM0wqGIwSgXKKRtYj49NkBXK66eGdmgN5PUZB7gX8CtneI4dwL991TuxZALw1b8KPs04GibQsBi9d0GG0U8eoIoyq2bpYA2b5s3E2o7rESBZB6DLRl3LJ5AgZDZD
#

from django.shortcuts import render
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from .models import Greeting
import requests
import json


# Create your views here.
def index(request):
#   return HttpResponse('Hello from Python! Austin')
    #return render(request, 'index.html')
    r = requests.get('http://httpbin.org/status/418')
    print r.text
    return HttpResponse('<pre>' + r.text + '</pre>')

@csrf_exempt
def webhook(request):
    if request.method == 'GET':
        return webhook_authorize(request)
    elif request.method == 'POST':
        return webhook_process_message(request)

def webhook_authorize(request):

    if request.GET is None:
        return HttpResponse("Error, missing required parameters such as hub.verify_token")

    vtoken = request.GET['hub.verify_token']

    print vtoken

    if (vtoken != None and vtoken == 'austinawesome'):
        return HttpResponse(request.GET['hub.challenge'])
    else:
        return HttpResponse("Error, wrong validation token")
   
def webhook_process_message(request):
    received_json_data = json.loads(request.body)
    print received_json_data

    events = received_json_data['entry'][0]['messaging'];
    for event in events:
        if 'message' in event and 'text' in event['message']:
            send_message(event['sender']['id'], event['message']['text'])
        
    return HttpResponse(content_type = "application/json", status =200)


def send_message(recipientID, text):
    print "sending a message to " + recipientID + " with origianl text=" + text

    ac_token = "EAADPXC2ERHUBAOLhhivVgZCEEBNwLA03yZANp0kWDyt5CLaZB5ZCOJIb6eawxXveK1yYhWknwof2G7Wi8pE866QEvISAIcsMOG87CKjJS4Hf9pMhUwnoAGX9ohDLHRSg7L9cEcyTO1ZCgMEXqE9rhu7NFnZB9gLL7Ud3eyXvTN1QZDZD"

    url = 'https://graph.facebook.com/v2.6/me/messages?access_token=' + ac_token


    data_1 = {'recipient': { 'id': recipientID }, 'message': {'text': 'yahoo'} }

    data_2 = {'recipient': { 'id': recipientID }, 
            "message": {
                "attachment":{
                   "type" : "image",
                   "payload":{
                       "url":"https://scontent.fsnc1-1.fna.fbcdn.net/v/t1.0-1/c40.0.160.160/p160x160/296689_1586399115681_1252262357_n.jpg?oh=404c5d6afe51a23772e8ff2f86ca1a07&oe=57DA172D"
                   }
                }
            }
           }
   
    data_3 = {
  "recipient":{
    "id": recipientID
  },

  "message":{
    "attachment":{
      "type":"template",
      "payload":{
        "template_type":"button",
        "text":"What do you want to do next?",
        "buttons":[
          {
            "type":"web_url",
            "url":"http://www.yahoo.com",
            "title":"Show Yahoo Website"
          },
          {
            "type":"postback",
            "title":"Start Chatting",
            "payload":"USER_DEFINED_PAYLOAD"
          }
        ]
      }
    }
  }
}
    headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}
    r = requests.post(url, data=json.dumps(data_1), headers=headers)
    
    print r
    return 
 

#
#
# When postback happens, server will receive
#{u'object': u'page', u'entry': [{u'messaging': [{u'postback': {u'payload': u'USER_DEFINED_PAYLOAD'}, u'sender': {u'id': u'10154156054213328'}, u'recipient': {u'id': u'138703426143987'}, u'timestamp': 1463808245370}], u'time': 1463808245370, u'id': 138703426143987}]}
#
#



def db(request):

    greeting = Greeting()
    greeting.save()

    greetings = Greeting.objects.all()

    return render(request, 'db.html', {'greetings': greetings})

