# Alexahttps
Groundwork for Amazon Alexa HTTPS endpoint voice automation

## Introduction
This outlines how to implement the Alexa Skills Kit with an independent controller using Flask for ASK. 

## Getting Started

* Make sure you have a computer running Python 3.4 or higher
* Add Python to your environment's PATH variable
* Have pip install manager running

## Preliminary Setup

Flask is a lightweight Python microframework that allows for quick development of mobile and web applications. Flask now supports rapid development with Alexa Skills Kit (ASK) as well. 
Navigate to your Python3 directory and run:
```bash
python -m pip install flask-ask
```

Now run the file in the Endpoint directory listed as ```FlaskMatrix.py```

Flask will generate a localhost server for testing on Port 5000. Amazon's Alexa will only communicate with a [secure endpoint][1], which means endpoint setup will be required. 

## Server testing

Fortunately, for quick testing we can use ngrok. This tool can wrap our local port behind an SSL-encrypted port and expose it to a temporary HTTPS endpoint.

Download and install the [ngrok][2] client to your OS. Open the executable and run:

```bash
ngrok.exe http:5000
```

Once this connects, you will be presented with a Forwarding address to an HTTPS endpoint from localhost:5000.

## Alexa Setup

Log in to the [Amazon Developer Portal][3] and create a new Skill. Enter a name for your skill and an invocation name that [follows the Amazon guidelines][4].
For the interation model, copy the intents.json file contents into your Intent Schema
Copy the utterances.txt file contents into the Sample Utterances file
For Configuration, choose the HTTPS radio button. If you are using the ngrok setup, enter your HTTPS endpoint here.
Under SSL Certificate, use the option "My development endpoint is a sub-domain of a domian that has a wildcard certificate from a certificate authority."

## Test

After following the above steps, we have an SSL-wrapped endpoint and our Skill running on localhost:5000. 
To simulate this, enter "say hello" into the Text box and click "Ask (instance name)"
This should return a JSON file wtih the contents "Hello world."

Triggering the Switcher Intent (e.g. switch input X to output Y) will send a packet containing the input and output you wish to switch to the designated port. 

Your controller should be running either a server or a client that can read this data and parse it accordingly. The Python to do this is not included in this repository. 


[1]: https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/developing-an-alexa-skill-as-a-web-service#requirements-for-your-web-service
[2]: https://ngrok.com/download
[3]: https://developer.amazon.com
[4]: https://developer.amazon.com/public/solutions/alexa/alexa-skills-kit/docs/choosing-the-invocation-name-for-an-alexa-skill
