__author__ = 'seanfitz'
# coding=UTF-8
"""
A sample program that uses multiple intents and disambiguates by
intent confidence
try with the following:
PYTHONPATH=. python examples/multi_intent_parser.py "what's the shoppingList like in tokyo"
PYTHONPATH=. python examples/multi_intent_parser.py "play some music by the clash"
"""

import json
import sys
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

class ShoppingListSkill(object):

    def __init__(self):

        self.intent = 'shoppingListIntent'

        # define vocabulary
        self.shoppingList_keyword = [
                "courses",
                "Acheter",
                "Achete"
                ]

        # structure intent
        self.shoppingList_intent = IntentBuilder(self.intent)\
                .require("shoppingListKeyword")\
                .require("Item")\
                .build()

    def register(self, engine):
        for wk in self.shoppingList_keyword:
            engine.register_entity(wk, "shoppingListKeyword")
        engine.register_intent_parser(self.shoppingList_intent)
        engine.register_regex_entity(".*achet[a-z]* (?P<Item>.*)")
        engine.register_regex_entity(".*ajout[a-z]* (?P<Item>.*) sur.*")

    def process(self, json):
        return "j'ai ajouté %s à votre liste de course" % json.get('Item')

if __name__ == "__main__":
    engine = IntentDeterminationEngine()
    skill = ShoppingListSkill()
    skill.register(engine)
    for intent in engine.determine_intent(' '.join(sys.argv[1:])):
        if intent and intent.get('confidence') > 0:
            print(json.dumps(intent, indent=4))
