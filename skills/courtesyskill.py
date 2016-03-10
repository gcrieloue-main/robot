__author__ = 'seanfitz'
# coding=UTF-8
"""
A sample program that uses multiple intents and disambiguates by
intent confidence
try with the following:
PYTHONPATH=. python examples/multi_intent_parser.py "what's the courtesy like in tokyo"
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

class CourtesySkill(object):

    def __init__(self):
        self.stored_calculation = 0

        self.intent = 'courtesyIntent'

        # define vocabulary
        self.courtesy_keyword = [
                "bonjour"
                ]

        # structure intent
        self.courtesy_intent = IntentBuilder(self.intent)\
                .require("CourtesyKeyword")\
                .build()

    def register(self, engine):
        for wk in self.courtesy_keyword:
            engine.register_entity(wk, "courtesyKeyword")
        engine.register_intent_parser(self.courtesy_intent)

    def process(self, json):
         result = sympy.sympify(json.get('CourtesyKeyword'))
         if json.get('CourtesyKeyword') == "bonjour":
             return "Bonjour monsieur"

if __name__ == "__main__":
    engine = IntentDeterminationEngine()
    skill = courtesySkill()
    skill.register(engine)
    for intent in engine.determine_intent(' '.join(sys.argv[1:])):
        if intent and intent.get('confidence') > 0:
            print(json.dumps(intent, indent=4))
