import argparse
import json
from src.core import ChatBot

parser = argparse.ArgumentParser(description='NLP Chatbot')
parser.add_argument('--config', help='Configuration file')
args = parser.parse_args()

with open(args.config, 'r') as f:
    config = json.load(f)

chatbot = ChatBot(config)

while True:
    user_input = input('User: ')
    response = chatbot.respond(user_input)
    print('Chatbot:', response)