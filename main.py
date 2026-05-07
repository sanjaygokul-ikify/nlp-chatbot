import argparse
import json
from src.core import ChatBot
from src.gui import ChatGUI

parser = argparse.ArgumentParser(description='NLP Chatbot')
parser.add_argument('--config', help='Configuration file', default=None)
args = parser.parse_args()

config = {}
if args.config:
    with open(args.config, 'r') as f:
        config = json.load(f)

chatbot = ChatBot(config)

app = ChatGUI(chatbot)
app.run()
