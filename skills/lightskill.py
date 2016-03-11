__author__ = 'hellsdark'
# coding=UTF-8
"""
A sample program that uses multiple intents and disambiguates by
intent confidence
try with the following:
PYTHONPATH=. python examples/multi_intent_parser.py "what's the light like in tokyo"
PYTHONPATH=. python examples/multi_intent_parser.py "play some music by the clash"
"""

import json
import sys
from phue import Bridge
from adapt.entity_tagger import EntityTagger
from adapt.tools.text.tokenizer import EnglishTokenizer
from adapt.tools.text.trie import Trie
from adapt.intent import IntentBuilder
from adapt.parser import Parser
from adapt.engine import IntentDeterminationEngine

tokenizer = EnglishTokenizer()
trie = Trie()
tagger = EntityTagger(trie, tokenizer)
parser = Parser(tokenizer, tagger)

# Allume le salon

class LightSkill(object):

    def __init__(self):

        self.bridge = Bridge('192.168.1.10')
        self.bridge.connect()

        self.intent = 'lightIntent'

        # define vocabulary
        self.light_keyword = [
                "allume",
                "éteint",
                "baisse",
                "diminue",
                "augmente",
                "luminosité"
                ]

        self.room_keyword = [
                "salon",
                "cuisine"
                ]

        # structure intent
        self.light_intent = IntentBuilder(self.intent)\
                .require("LightKeyword")\
                .require("RoomKeyword")\
                .optionally("NumericValue")\
                .build()

    def register(self, engine):
        for wk in self.light_keyword:
            engine.register_entity(wk, "LightKeyword")
        for wk in self.room_keyword:
            engine.register_entity(wk, "RoomKeyword")
        engine.register_regex_entity("(?P<NumericValue>\d+)")
        engine.register_intent_parser(self.light_intent)

    def process(self, json):
         room = json.get('RoomKeyword')
         if json.get('LightKeyword') == "allume":
            self.bridge.set_light(room, 'on', True)
            return "J'allume '%s'" % room
         if json.get('LightKeyword') == "éteint":
            self.bridge.set_light(room, 'on', False)
            return "J'éteins '%s'" % room
         if json.get('LightKeyword') == "baisse":
             bri = self.bridge.get_light(room).get('state').get('bri')
             self.bridge.set_light(room, 'bri', bri-20)
             return "J'ai diminué la lumière dans le '%s'" % room

if __name__ == "__main__":
    engine = IntentDeterminationEngine()
    skill = LightSkill()
    skill.register(engine)
    for intent in engine.determine_intent(' '.join(sys.argv[1:])):
        if intent and intent.get('confidence') > 0:
            print(json.dumps(intent, indent=4))
