__author__ = 'seanfitz'
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
import sympy
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

# Ajoute xxx sur ma liste de courses
# Je veux acheter xxx

class LightSkill(object):

    def __init__(self):
        self.intent = 'lightIntent'

        # define vocabulary
        self.light_keyword = [
                "allume",
                "éteins"
                ]

        self.room_keyword = [
                "salon",
                "cuisine"
                ]

        # structure intent
        self.light_intent = IntentBuilder(self.intent)\
                .require("LightKeyword")\
                .require("RoomKeyword")\
                .build()

    def register(self, engine):
        for wk in self.light_keyword:
            engine.register_entity(wk, "LightKeyword")
        for wk in self.room_keyword:
            engine.register_entity(wk, "RoomKeyword")
        engine.register_intent_parser(self.light_intent)

    def process(self, json):
         if json.get('LightKeyword') == "allume":
            return "J'allume '%s'" % json.get('RoomKeyword')
         if json.get('LightKeyword') == "éteins":
            return "J'éteins '%s'" % json.get('RoomKeyword')

if __name__ == "__main__":
    engine = IntentDeterminationEngine()
    skill = LightSkill()
    skill.register(engine)
    for intent in engine.determine_intent(' '.join(sys.argv[1:])):
        if intent and intent.get('confidence') > 0:
            print(json.dumps(intent, indent=4))
