from dotenv import load_dotenv
import os
import logging
from sys import stdout
import json
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from hcul import InputFieldCountException, NoInputFieldException, hcul
try:
    load_dotenv()
except:
    pass

logger = logging.getLogger('mylogger')

logger.setLevel(logging.INFO) # set logger level
logFormatter = logging.Formatter\
("%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s")
consoleHandler = logging.StreamHandler(stdout) #set streamhandler to stdout
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)


app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.command("/hcul-to-brainfuck")
def hcul_to_brainfuck(ack, respond, command):
    ack() # Acknowledge request for slack
    logger.info(f"Received {command} and acknowledged it")
    command_text = f"{command['text']}"

    replacement = {":upvote:": ">", ":downvote:": "<", ":yay:": "+", ":heavysob:": "-", ":pf:": ".", ":sadge:": ".", ":3c:": ",", ":dino-drake-yea:": "[", ":dino-drake-nah:": "]", " ": ""}

    for o, n in replacement.items():
        command_text = command_text.replace(o, n)

    logger.info(f"Input : {command['text']}")
    logger.info(f"Output : {command_text}")
    user = app.client.users_info(user=command['user_id'])
    respond(
        {
            "blocks" : [
                {"type": "context","elements": [{"type": "image","image_url": f"{user['user']['profile']['image_32']}","alt_text": f"{user['user']['profile']['display_name']}'s pfp"},{"type": "mrkdwn","text": f"*{user['user']['profile']['display_name']}* Asked: "}]},
                {"type": "section", "text": {"type": "mrkdwn", "text": f">:idea-dino: Convert this Hackclub Universal Langugage code into Brainfuck :\n{command['text']}"}},
                {"type": "divider"},
                {"type": "section", "text": {"type": "mrkdwn", "text": f"Output :\n{command_text}"}}
            ],
            "response_type": "in_channel"
        }
    )

@app.command("/brainfuck-to-hcul")
def brainfuck_to_hcul(ack, respond, command, body, client):
    ack()
    logger.info(f"Received {command} and acknowledged it")
    command_text = f"{command['text']}"

    replacement = {":upvote:": ">", ":downvote:": "<", ":yay:": "+", ":heavysob:": "-", ":pf:": ".", ":3c:": ",", ":dino-drake-yea:": "[", ":dino-drake-nah:": "]"}

    for o, n in replacement.items():
        command_text = command_text.replace(n, o)
    logger.info(f"Input : {command['text']}")
    logger.info(f"Output : {command_text}")
    user = app.client.users_info(user=command['user_id'])
    respond(
        {
            "blocks" : [
                {"type": "context","elements": [{"type": "image","image_url": f"{user['user']['profile']['image_32']}","alt_text": f"{user['user']['profile']['display_name']}'s pfp"},{"type": "mrkdwn","text": f"*{user['user']['profile']['display_name']}* Asked: "}]},
                {"type": "section", "text": {"type": "mrkdwn", "text": f">:idea-dino: Convert this Brainfuck code into Hackclub Universal Language :\n{command['text']}"}},
                {"type": "divider"},
                {"type": "section", "text": {"type": "mrkdwn", "text": f"Output :\n{command_text}"}}
            ],
            "response_type": "in_channel"
        }
    )

@app.view("view-id")
def view_submission(ack, body, logger):
    ack()
    logger.info(body["view"]["state"]["values"])

@app.command("/run-hcutcl")
def run_code(ack, respond, command):
    ack()
    logger.info(f"Received {command} and acknowledged it")
    anwser = "An exception occurred"
    try:
        anwser = hcul(command['text'])
    except InputFieldCountException:
        anwser = "You can only have one input field that is opened with :uuh: and is closed with :noooovanish:"
    except NoInputFieldException:
        anwser = "You tried to get data from an input that does not exist."
    logger.info(f"Input : {command['text']}")
    logger.info(f"Anwser : {anwser}")
    respond(anwser)

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
