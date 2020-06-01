from random import randint
import requests as req

from flask import Flask, request, url_for
from twilio.twiml.voice_response import VoiceResponse, Gather

app = Flask(__name__)

EXCUSES = {
    1: "That's not a bug it's a feature",
    2: "The system is working as designed",
    3: "just download it into an excel sheet and re-upload it",
    4: "Just remember not to do that",
}

@app.route('/test', methods=['GET', 'POST'])
def test():
    return get_insult()

@app.route("/greeting", methods=['GET', 'POST'])
def greeting():
    """Respond to incoming phone calls with a brief message."""
    # Start our TwiML response
    resp = VoiceResponse()
    welcome_msg = """
    Thank you for calling Clear Spider, where we believe great software, 
    like a good whiskey, should be locked in a basement and not touched for eight teen years. 
    If you would like to report a bug, please press 1. If you would like to leave a 
    message letting us know how great we are press 2. If you would like to talk to a
    real person press 3.
    """
    # Read a message aloud to the caller
    gather = Gather(num_digits=1, action='/bug_report')
    gather.say(welcome_msg, voice='man')
    resp.append(gather)

    resp.redirect('/greeting')

    return str(resp)


@app.route("/bug_report", methods=['GET', 'POST'])
def bug_report():
    rick_roll = url_for('static', filename='rick_roll.mp3')
    resp = VoiceResponse()

    if 'Digits' in request.values:
        choice = request.values['Digits']

        if choice == '1':
            resp.say('Please describe the bug.', voice='man')
            resp.pause(5)
            excuse = EXCUSES[randint(1, 4)]
            resp.say('Here is a thoughtful solution to that bug: ', voice='man')
            resp.say(excuse, voice='man')
            resp.redirect('/greeting')
        elif choice == '2':
            insult = get_insult()
            resp.say('Please extol our virtues', voice='man')
            resp.pause(5)
            resp.say('Thanks for that. Here is a random thought we have about you: ', voice='man')
            resp.say(insult, voice='man')
            resp.redirect('/greeting')
        elif choice == '3':
            resp.say('Wait for it', voice='man')
            resp.play('https://demo.twilio.com/docs/classic.mp3')
            resp.redirect('/greeting')

    resp.redirect('/greeting')

    return str(resp)


def get_insult():
    insult = req.get('https://insult.mattbas.org/api/en/insult.json')
    insult_data = insult.json()
    return insult_data['insult']


if __name__ == "__main__":
    app.run()