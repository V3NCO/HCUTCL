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

logger.setLevel(logging.INFO) # set logger level
logFormatter = logging.Formatter\
("%(name)-12s %(asctime)s %(levelname)-8s %(filename)s:%(funcName)s %(message)s")
consoleHandler = logging.StreamHandler(stdout) #set streamhandler to stdout
consoleHandler.setFormatter(logFormatter)
logger.addHandler(consoleHandler)

app = App(token=os.environ.get("SLACK_BOT_TOKEN"), logger=logger)

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
    client.views_open(
        trigger_id=body["trigger_id"],
        view = {
            "type": "modal",
            "callback_id": "bftohcul_modal",
            "title": {
                "type": "plain_text",
                "text": ":pf: Brainfuck to HCUL",
                "emoji": True
            },
            "submit": {
                "type": "plain_text",
                "text": "Convert!"
            },
            "close": {
                "type": "plain_text",
                "text": "Cancel"
            },
            "blocks": [
                {
                    "type": "actions",
                    "block_id": "action_1",
                    "elements": [
                        {
                            "type": "conversations_select",
                            "default_to_current_conversation": True,
                            "action_id": "conv_select",
                            "response_url_enabled": True,
                            "placeholder": {
                                "type": "plain_text",
                                "text": "Select a conversation to send the output in"
                            },
                            "filter": {
                                "include": ["public"],
                                "exclude_bot_users": True
                            }
                        }
                    ]
                },
                {
                    "type": "input",
					"block_id": "brainfuck_input",
                    "element": {
                        "type": "plain_text_input",
                        "multiline": True,
                        "action_id": "brainfuck_subinput"
                    },
                    "label": {
                        "type": "plain_text",
                        "text": "Your code here :yay:",
                        "emoji": True
                    }
                }
            ]
        }
    )
    # user = app.client.users_info(user=command['user_id'])
    # respond(
    #     {
    #         "blocks" : [
    #             {"type": "context","elements": [{"type": "image","image_url": f"{user['user']['profile']['image_32']}","alt_text": f"{user['user']['profile']['display_name']}'s pfp"},{"type": "mrkdwn","text": f"*{user['user']['profile']['display_name']}* Asked: "}]},
    #             {"type": "section", "text": {"type": "mrkdwn", "text": f">:idea-dino: Convert this Brainfuck code into Hackclub Universal Language :\n{command['text']}"}},
    #             {"type": "divider"},
    #             {"type": "section", "text": {"type": "mrkdwn", "text": f"Output :\n{command_text}"}}
    #         ],
    #         "response_type": "in_channel"
    #     }
    # )


@app.view("bftohcul_modal")
def view_submission(ack, body, logger, respond, client):
    ack()
    submitted = body["view"]["state"]["values"]["brainfuck_input"]["brainfuck_subinput"]["value"]
    channel = body["view"]["state"]["values"]["action_1"]["conv_select"]
    logger.info(submitted)
    logger.info(channel)
    replacement = {":upvote:": ">", ":downvote:": "<", ":yay:": "+", ":heavysob:": "-", ":pf:": ".", ":3c:": ",", ":dino-drake-yea:": "[", ":dino-drake-nah:": "]"}
    command_text = submitted
    for o, n in replacement.items():
        command_text = command_text.replace(n, o)

    user = app.client.users_info(user=body["user"]["id"])
    try:
        client.chat_postMessage(channel=channel["selected_conversation"],
        blocks = [
                    {"type": "context","elements": [{"type": "image","image_url": f"{user['user']['profile']['image_32']}","alt_text": f"{user['user']['profile']['display_name']}'s pfp"},{"type": "mrkdwn","text": f"*{user['user']['profile']['display_name']}* Asked: "}]},
                    {"type": "section", "text": {"type": "mrkdwn", "text": f">:idea-dino: Convert this Brainfuck code into Hackclub Universal Language :\n{submitted}"}},
                    {"type": "divider"},
                    {"type": "section", "text": {"type": "mrkdwn", "text": f"Output :\n{command_text}"}}
                ]
        )
    except:
        logger.exception("Failed to post a message")

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
    user = app.client.users_info(user=command['user_id'])
    respond(
        {
            "blocks" : [
                {"type": "context","elements": [{"type": "image","image_url": f"{user['user']['profile']['image_32']}","alt_text": f"{user['user']['profile']['display_name']}'s pfp"},{"type": "mrkdwn","text": f"*{user['user']['profile']['display_name']}* Asked: "}]},
                {"type": "section", "text": {"type": "mrkdwn", "text": f">:idea-dino: Run this Hackclub Universal Turing Complete Language Code:\n{command['text']}"}},
                {"type": "divider"},
                {"type": "section", "text": {"type": "mrkdwn", "text": f"*Output* :\n`{anwser}`"}}
            ],
            "response_type": "in_channel"
        }
    )

@app.command("/hcul-help")
def help(ack, respond, command):
    ack()
    respond(
        {
	"blocks": [
		{
			"type": "header",
			"text": {
				"type": "plain_text",
				"text": ":skulk: Emojis list",
				"emoji": True
			}
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "mrkdwn",
					"text": "*Emoji*"
				},
				{
					"type": "mrkdwn",
					"text": "*Function*"
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "plain_text",
					"text": ":upvote:",
					"emoji": True
				},
				{
					"type": "mrkdwn",
					"text": "`>` from Brainfuck"
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "plain_text",
					"text": ":downvote:",
					"emoji": True
				},
				{
					"type": "mrkdwn",
					"text": "`<` from Brainfuck"
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "plain_text",
					"text": ":yay:",
					"emoji": True
				},
				{
					"type": "mrkdwn",
					"text": "`+` from Brainfuck"
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "plain_text",
					"text": ":heavysob:",
					"emoji": True
				},
				{
					"type": "mrkdwn",
					"text": "`-` from Brainfuck"
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "plain_text",
					"text": ":pf:",
					"emoji": True
				},
				{
					"type": "mrkdwn",
					"text": "`.` from Brainfuck, outputs as an ASCII Character"
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "plain_text",
					"text": ":sadge:",
					"emoji": True
				},
				{
					"type": "mrkdwn",
					"text": "`.` from Brainfuck, outputs as a number"
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "plain_text",
					"text": ":3c:",
					"emoji": True
				},
				{
					"type": "mrkdwn",
					"text": "`,` from Brainfuck"
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "plain_text",
					"text": ":dino-drake-yea:",
					"emoji": True
				},
				{
					"type": "mrkdwn",
					"text": "`[` from Brainfuck"
				}
			]
		},
		{
			"type": "divider"
		},
		{
			"type": "section",
			"fields": [
				{
					"type": "plain_text",
					"text": ":dino-drake-nah:",
					"emoji": True
				},
				{
					"type": "mrkdwn",
					"text": "`]` from Brainfuck"
				}
			]
		},
		{
			"type": "divider"
		},
		{
					"type": "section",
					"fields": [
						{
							"type": "plain_text",
							"text": ":uuh:",
							"emoji": True
						},
						{
							"type": "mrkdwn",
							"text": "Open the input field which will be used to give data to `:3c:`."
						}
					]
		},
		{
			"type": "divider"
		},
		{
					"type": "section",
					"fields": [
						{
							"type": "plain_text",
							"text": ":noooovanish:",
							"emoji": True
						},
						{
							"type": "mrkdwn",
							"text": "Close the input field which will be used to give data to `:3c:`."
						}
					]
		},
		{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": "If you use :3c: at any point *you need* to add an input field with :uuh:Yourtexthere:noooovanish:"
					}
		},
		{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": "You can only have one input field and you obviously *have to open and close it*"
					}
		},
		{
					"type": "section",
					"text": {
						"type": "mrkdwn",
						"text": "Commands list: `/hcul-help`, `/brainfuck-to-hcul`, `/hcul-to-brainfuck`, `/run-hcutcl`"
					}
		}
	]
        }
    )

if __name__ == "__main__":
    SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"]).start()
