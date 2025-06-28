from dotenv import load_dotenv
import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

app = App(token=os.environ.get("SLACK_BOT_TOKEN"))

@app.command("/hcul-to-brainfuck")
def hcul_to_brainfuck(ack, respond, command):
    ack() # Acknowledge request for slack
    command_text = f"{command['text']}"

    replacement = {":upvote:": "<", ":downvote:": ">", ":yay:": "+", ":heavysob:": "-", ":pf:": ".", ":3c:": ",", ":dino-drake-yea:": "[", ":dino-drake-nah:": "]", " ": ""}

    for o, n in replacement.items():
        command_text = command_text.replace(o, n)

    respond(f"{command_text}")
    print(f"{command_text}")

@app.command("/brainfuck-to-hcul")
def brainfuck_to_hcul(ack, respond, command):
    ack() # Acknowledge request for slack
    command_text = f"{command['text']}"

    replacement = {":upvote:": "<", ":downvote:": ">", ":yay:": "+", ":heavysob:": "-", ":pf:": ".", ":3c:": ",", ":dino-drake-yea:": "[", ":dino-drake-nah:": "]"}

    for o, n in replacement.items():
        command_text = command_text.replace(n, o)

    respond(f"{command_text}")
    print(f"{command_text}")

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
