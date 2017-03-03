from http.server import BaseHTTPRequestHandler, HTTPServer
import logging
import json
import ssl


logging.getLogger('my_server').setLevel(logging.DEBUG)


class custom_handler(BaseHTTPRequestHandler):
    def _set_headers(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def do_GET(self):
        self._set_headers()
        self.wfile.write("<html><body><h1>Boo!</h1></body></html>".encode())

    def do_HEAD(self):
        self._set_headers()

    def do_POST(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        json_data = json.loads(post_data.decode())
        S = lambda_handler(json_data, None)
        self.send_response(200, 'OK')
        self.send_header('Content-Type', 'text/html; charset=utf-8')
        self.send_header('Content-Length', len(str(S)))
        self.end_headers()
        self.wfile.write(json.dumps(S).encode())


def run(server_class=HTTPServer, handler_class=custom_handler):
    serv = ('localhost', 8080)
    keyfile = r'C:/Users/jlasher/Documents/conf/ssl.key/server.key'
    certfile = r'C:/Users/jlasher/Documents/conf/ssl.crt/server.crt'
    httpd = server_class(serv, handler_class)
    httpd.socket = ssl.wrap_socket(httpd.socket,keyfile,certfile,server_side=True)
    print('Starting httpd...')
    httpd.serve_forever()


def lambda_handler(event, context):
    print('event.session.application.applicationId=' + event['session']['application']['applicationId'])

    """ The below statement is to ensure that only Alexa is talking to the device. Uncomment to
    enable this functionality. """
    # if (event['session']['application']['applicationId'] != "amzn1.echo-sdk-ams.app.[unique-value-here]"):
    #     raise ValueError("Invalid Application ID")

    if event['session']['new']:
        on_session_started({'requestId': event['request']['requestId']}, event['session'])

    if event['request']['type'] == "LaunchRequest":
        return on_launch(event['request'], event['session'])
    elif event['request']['type'] == "IntentRequest":
        return on_intent(event['request'], event['session'])
    elif event['request']['type'] == "SessionEndedRequest":
        return on_session_ended(event['request'], event['session'])


def on_session_started(session_started_request, session):
    print('requestId= ' + session_started_request['requestId'] + ', sessionId= ' + session['sessionId'])


def on_launch(launch_request, session):
    print('on_launch requestId= ' + launch_request['requestId'] + ', sessionId= ' + session['sessionId'])
    return get_welcome_response()


def on_intent(intent_request, session):
    print('on_intent requestId= ' + intent_request['requestId'] + ', sessionId= ' + session['sessionId'])
    intent = intent_request['intent']
    intent_name = intent_request['intent']['name']

    if intent_name == 'HelloWorldIntent':
        return hello_world_response(intent, session)
    elif intent_name == 'SwitcherIntent':
        return update_switcher(intent, session)
    elif intent_name == 'AMAZON.CancelIntent' or intent_name == 'AMAZON.StopIntent':
        return handle_session_end_request()
    else:
        raise ValueError('Invalid intent name')


def on_session_ended(session_end_request, session):
    print('on_session_ended requestId= ' + session_end_request['requestId'] + ', sessionId= ' + session['sessionId'])


# ----------------------------------------------------------------------------------------------------------------- #
def get_welcome_response():
    session_attributes = {}
    card_title = 'Welcome'
    speech_output = 'Please choose a switcher operation'
    reprompt_text = 'You can update the switcher by saying, change switcher input number to output number'
    should_end_session = False
    return speech_builder(session_attributes, json_speechlet_response(card_title, speech_output, reprompt_text, should_end_session))


def hello_world_response(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    speech_text = 'Hello there, world'
    return speech_builder(session_attributes, json_speechlet_response(card_title,speech_text, None, should_end_session))


def update_switcher(intent, session):
    card_title = intent['name']
    session_attributes = {}
    should_end_session = False
    speech_text = 'Updating the switcher with your selection.'

    return speech_builder(session_attributes, json_speechlet_response(card_title, speech_text, None, should_end_session))


def handle_session_end_request():
    card_title = 'Session Ended'
    speech_output = 'Exiting the control function application.'
    should_end_session = True
    return speech_builder({}, json_speechlet_response(card_title, speech_output, None, should_end_session))


# ----------------------------------------------------------------------------------------------------------------- #
def speech_builder(session_attributes, speechlet_response):
    return {
        'version': '1.0',
        'sessionAttributes': session_attributes,
        'response': speechlet_response
    }


def json_speechlet_response(title, output, reprompt_text, should_end_session):
    return {
        'outputSpeech': {
            'type': 'PlainText',
            'text': output
        },
        'card': {
            'type': 'Simple',
            'title': 'SessionSpeechlet - ' + title,
            'content': 'SessionSpeechlet - ' + output
        },
        'reprompt': {
            'outputSpeech': {
                'type': 'PlainText',
                'text': reprompt_text
            }
        },
        'shouldEndSession': should_end_session
    }

run()
