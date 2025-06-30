from dotenv import load_dotenv
import os
import logging
from sys import stdout
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
from hcul import InputFieldCountException, NoInputFieldException, hcul
try:
    load_dotenv()
except:
    pass

logger = logging.getLogger('mylogger')

logger.setLevel(logging.DEBUG) # set logger level
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
    respond(f"{command_text}")

@app.command("/brainfuck-to-hcul")
def brainfuck_to_hcul(ack, respond, command):
    ack() # Acknowledge request for slack
    logger.info(f"Received {command} and acknowledged it")
    command_text = f"{command['text']}"

    replacement = {":upvote:": ">", ":downvote:": "<", ":yay:": "+", ":heavysob:": "-", ":pf:": ".", ":3c:": ",", ":dino-drake-yea:": "[", ":dino-drake-nah:": "]"}

    for o, n in replacement.items():
        command_text = command_text.replace(n, o)
    logger.info(f"Input : {command['text']}")
    logger.info(f"Output : {command_text}")
    respond(f"{command_text}")

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
