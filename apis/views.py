from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import HttpResponse
import openai
import time
import json
import requests
import random

#openai.api_key = "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"
openai.api_key = "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"
#NWBAssistantKey
#ssbruno.001

# Create your views here.
def get_response(request):
    rsp = ''
    audio = ''
    if request.method == 'GET':
        transcript = request.GET['transcript']
        custname = request.GET['custname']
        rid = request.GET['rid']
        
        if transcript is not None:
            transcript = transcript.replace('-', ' ');
            print(transcript)
            jsnobj = process_message(transcript, rid, custname)
            rsp = jsnobj["response"]
            print(rsp)
            audio = getAudio(rsp)
            print(audio)
    return HttpResponse('{"text":"'+rsp+'","custname":"'+jsnobj["custname"]+'","rid":"'+jsnobj["nxtr"]+'", "audio":"'+audio+'"}')

#Main message
greetings = ["Hey there.! Hope you are having a good day!", "Good day!", "Hello there!", "Hi!"]
nameconf = ["Can I call you as <custname>?", "Is it fine to call you <custname>?", "Hope I can call you <custname>"]
idvq = ["For verification, can you please give last 4 digits of your account number?", 
        "We need last 4 digits of your account number for verification."]
yesstr = ["yes","yeah","yep","yeh","of course", "of course", "love to", "happy to","sure"]
nostr = ["no","nope","nah","not"]
def checkPresenseIn(user_input, lst):
    for i in lst:
        if user_input.count(i) > 0:
            return True
    return False

def process_message(user_input, rid, custname):
    response = ""
    nxtr = ""
    #freq = custinput["freq"]
    # Validations of customer input for each step
    if rid == "r0":
        #Give greetings and 
        response = random.choice(greetings)+" "+random.choice(nameconf)
        response = response.replace("<custname>", custname)
        nxtr = "r1"
    if rid == "r1":
        prompt = user_input + " - can this text be taken as a positive response? And get the preferred name in the text in JSON format"
        response = generate_ai_response(prompt).lower()
        # look for positive response
        print(response)
        if checkPresenseIn(response, yesstr) == True:
            #if response.count('{') > 0:
            #    namejsn = json.loads("{"+response.split('{')[1].split('}')[0]+"}")
            #    namekey = ""
            #    for k in namejsn.keys:
            #        if k.count('name') > 0:
            #            namekey = k
            #            break
            #    if namekey != "":
            #        custname = namejsn[namekey]
            response = "Thank you for confirming "+custname+". "+random.choice(idvq)
            nxtr = "r2"
        elif response.count("no") > 0:
            print("inside no")
            if response.count('{') > 0:
                namejsn = json.loads("{"+response.split('{')[1].split('}')[0]+"}")
                namekey = ""
                for k in namejsn.keys:
                    if k.count('name') > 0:
                        namekey = k
                        break
                if namekey != "":
                    custname = namejsn[namekey]
                response = "Thank you for confirming "+custname+". "+random.choice(idvq)
                nxtr = "r2"
                #custname = namejsn["preferredname"]
                #freq = int(freq)+1;
            else:
                response = "Apologies. How do you preferred to be called?"
                nxtr = "r1"
                #freq = int(freq)+1
        else:
            response = "Apologies. Dint quite get that. Will tranfer to supervisor!"
            rid = "r6"
    if rid == "r2":
        prompt = user_input + " - Get numbers from this text, append as a single string and give in a json key 'number'"
        response = generate_ai_response(prompt).lower()
        print(response)
        if response.count('{') > 0:
            acctjsn = json.loads("{"+response.split('{')[1].split('}')[0]+"}")
            acctnr = acctjsn["number"]
            print(len(acctnr))
            if len(acctnr) == 4:
                response = "Thank you for confirming the number. I can see there is a Fraud case created in your account. Would you like to know its status?"
                nxtr = "r3"
            else:
                response = "Apologies. Dint quite get the number. Will tranfer to supervisor!"
                rid = "r6"
    if rid == "r3":
        prompt = user_input + " - can this text be taken as a positive response?"
        response = generate_ai_response(prompt).lower()
        # look for positive response
        print(response)
        if checkPresenseIn(response, yesstr) == True:
            response = "Great. Thank you. Can you please share the case number?"
            nxtr = "r4"
        elif response.count("no") > 0:
            response = "Okay. If it's for something else, let me tranfer to supervisor! Please hold on!"
            rid = "r6"
        #elif response.count("yes") > 0 or response.count('affirmation": true') > 0:
        else:
            response = "Apologies. Dint quite get that. Will tranfer to supervisor!"
    if rid == "r4":
        prompt = user_input + " - Get numbers from this text, append as a single number and give in a json key 'number"
        response = generate_ai_response(prompt).lower()
        print(response)
        if response.count('{') > 0:
            acctjsn = json.loads("{"+response.split('{')[1].split('}')[0]+"}")
            acctnr = acctjsn["number"]
            if acctnr > 0:
                response = "Got the case number. Let me check certain details and confirm if this can be submitted. Shall I put you on hold for a minute?"
                nxtr = "r5"
            else:
                response = "Apologies. Dint quite get the number. Will tranfer to supervisor!"
                rid = "r6"
    if rid == "r5":
        prompt = user_input + " - can this text be taken as a positive response?"
        response = generate_ai_response(prompt).lower()
        # look for positive response
        print(response)
        if checkPresenseIn(response, yesstr) == True:
            response = "Great. Thank you for your patience. thank you for sharing the details, we will progress this case and you will get an update instantly in email. Thank you. Good bye!"
            nxtr = "r6"
        elif response.count("no") > 0:
            response = "Okay. If it's urgent, let me tranfer to supervisor immediately!"
        #elif response.count("yes") > 0 or response.count('affirmation": true') > 0:
        #    response = "Great. Thank you for your patience. thank you for sharing the details, we will progress this case and you will get an update instantly in email"
        #    nxtr = "r6"
        else:
            response = "Apologies. Dint quite get that. Will tranfer to supervisor!"
            rid = "r6"
    if rid == "r5":
        response = "Over to Supervisor.!"
    return {"response":response, "nxtr":nxtr, "custname": custname}

#Open AI Functions 
def generate_ai_response_old(prompt):
    response = openai.Completion.create(
        engine = "text-davinci-003",
        prompt = prompt,
        max_tokens = 1000,
        n = 1,
        stop = None,
        temperature = 0.5
    )
    return response["choices"][0]["text"]

def generate_ai_response(input_msg):
    try:
      gptChat = openai.ChatCompletion.create(
      model="gpt-3.5-turbo",
      messages=[{"role": "user", "content": input_msg}])
      resp = gptChat.choices[0].message.content
      return resp
    except Exception as e:
      print(f"Error: {e}")

def start_conversation():
    response = generate_ai_response('greet me pleasantly')
    response = response.replace('Absolutely!', '').replace('Of course!','').strip()
    return response

#Eden AI Functions
def getAudio(transcript):
    headers = {"Authorization": "Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiZGYyYjdhNWQtNTkwMS00MTNkLThjMzAtMmY4ZDI2ZjA3YmRjIiwidHlwZSI6ImFwaV90b2tlbiJ9.YgNRsD4eDuU1lW7vFB9ZOMMkZUfcG_4C4_EfPQwsZ-8"}

    url ="https://api.edenai.run/v2/audio/text_to_speech"
    payload={"show_original_response": False,"fallback_providers": "","providers": "google,amazon", "language": "en-US", "option":"FEMALE", "text": transcript}

    response = requests.post(url, json=payload, headers=headers)

    result = json.loads(response.text)
    basse64str = result['google']['audio']
    return basse64str