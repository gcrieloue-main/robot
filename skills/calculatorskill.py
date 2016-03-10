__author__ = 'seanfitz'
# coding=UTF-8
"""
A sample program that uses multiple intents and disambiguates by
intent confidence
try with the following:
PYTHONPATH=. python examples/multi_intent_parser.py "what's the calculator like in tokyo"
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

class CalculatorSkill(object):

    def __init__(self):
        self.stored_calculation = 0

        self.intent = 'calculatorIntent'

        # define vocabulary
        self.calculator_keyword = [
                "combien",
                "calcule",
                "ajoute",
                "soustrait",
                "enlève"
                ]

        # structure intent
        self.calculator_intent = IntentBuilder(self.intent)\
                .require("CalculatorKeyword")\
                .require("Item")\
                .build()

    def register(self, engine):
        for wk in self.calculator_keyword:
            engine.register_entity(wk, "CalculatorKeyword")
        engine.register_intent_parser(self.calculator_intent)
        engine.register_regex_entity("Combien f[a-z]+ (?P<Item>.*)")
        engine.register_regex_entity("Ajoute (?P<Item>.*)")

    def process(self, json):
         result = sympy.sympify(json.get('Item'))
         if json.get('CalculatorKeyword') == "combien":
            self.stored_calculation = result
         if json.get('CalculatorKeyword') == "ajoute":
            self.stored_calculation += result
         print("cela fait %s" % self.stored_calculation)

if __name__ == "__main__":
    engine = IntentDeterminationEngine()
    skill = CalculatorSkill()
    skill.register(engine)
    for intent in engine.determine_intent(' '.join(sys.argv[1:])):
        if intent and intent.get('confidence') > 0:
            print(json.dumps(intent, indent=4))
