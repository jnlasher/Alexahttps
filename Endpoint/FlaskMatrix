import logging
import socket
from flask import Flask
from flask_ask import Ask, request, session, question, statement


app = Flask(__name__)
ask = Ask(app, '/')
logging.getLogger('flask_ask').setLevel(logging.DEBUG)


@ask.launch
def launch():
    speech_text = 'Please choose a switcher operation'
    return question(speech_text).reprompt(speech_text).simple_card('HelloWorld', speech_text)


@ask.intent('HelloWorldIntent')
def hello_world():
    speech_text = 'Hello world'
    return statement(speech_text).simple_card('HelloWorld', speech_text)


@ask.intent('SwitcherIntent', mapping={'sw_input': 'Input', 'sw_output': 'Output'})
def switcher_update(sw_input, sw_output):
    speech_text = 'Updating the switcher with your selection.'

    s = socket.socket(socket.AF_INET)
    serverAddress = ('192.168.254.250', 8080)
    s.connect(serverAddress)
    s.sendall('Input: {}, Output: {}'.format(sw_input, sw_output).encode())

    return statement(speech_text)

@ask.session_ended
def session_ended():
    return "", 200

if __name__ == '__main__':
    app.run(debug=True)
