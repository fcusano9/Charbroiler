
import json
import random

# Application entry point
def lambda_handler(event, context):
    if event['request']['type'] == "LaunchRequest":
        return on_launch()
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'])
        

# Called on receipt of an intent
def on_intent(request, session):

    intent = request['intent']
    intent_name = request['intent']['name']

    #if 'dialogState' in request:
        # Delegate to Alexa until dialog sequence is complete
    #    if request['dialogState'] == "STARTED" or request['dialogState'] == "IN_PROGRESS":
    #        return dialog_response("", False)
            
    # Process the user intents
    if intent_name == "RoastIntent":
        return roast_brother(request)
    elif intent_name == "AMAZON.HelpIntent":
        return do_help()
    elif intent_name == "AMAZON.StopIntent":
        return do_stop()
    elif intent_name == "AMAZON.CancelIntent":
        return do_stop()
    else:
        # Invalid intent, reply with help message
        return do_help()


# Return a roast of the brother requested
def roast_brother(request):
    attributes = {}

    # Get the name of the requested brother
    brother = request['intent']['slots']['brother']['resolutions']['resolutionsPerAuthority'][0]['values'][0]['value']['name']

    with open("brothers.json", 'r') as jsonfile:
        brothers = json.load(jsonfile)

    # Get the list of roasts for the requested brother
    roasts = brothers[brother]['roasts']

    # If there are no roasts return a message
    if len(roasts) == 0:
        return response(attributes, response_plain_text("There are no roasts for this brother yet, please submit suggestions to Frank.", True))

    # Choose a random roast that Alexa will respond with
    roast = random.choice(roasts)
    
    return response(attributes, response_plain_text(roast, True))


#---------------------------------------------------------------------------------------------------
# Response Handlers
#---------------------------------------------------------------------------------------------------

# Create a simple json plain text response for Alexa
def response_plain_text(output, endsession):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'shouldEndSession': endsession
    }

# Create a response using Speech Synthesis Markup Language (SSNL) to be able to change Alexa's voice 
def response_ssml(output, endsession):
    return {
        'outputSpeech': {
            'type': 'SSML',
            'ssml': output
        },
        'shouldEndSession': endsession
    }

# Create a simple json response
def response(attributes, speech_response):
    return {
        'version': '1.0',
        'sessionAttributes': attributes,
        'response': speech_response
    }

def dialog_response(attributes, endsession):
    return {
        'version': '1.0',
        'sessionAttributes': attributes,
        'response':{
            'directives': [
                {
                    'type': 'Dialog.Delegate'
                }
            ],
            'shouldEndSession': endsession
        }
    }