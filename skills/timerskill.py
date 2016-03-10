__author__ = 'seanfitz'
# coding=UTF-8
"""
A sample program that uses multiple intents and disambiguates by
intent confidence
try with the following:
PYTHONPATH=. python examples/multi_intent_parser.py "what's the timer like in tokyo"
PYTHONPATH=. python examples/multi_intent_parser.py "play some music by the clash"
"""

import json
import sys
import datetime
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

class TimerSkill(object):

    def __init__(self):

        self.intent = "timerIntent"

        # define vocabulary
        self.timer_keyword = [
                "préviens",
                "timer",
                "compte à rebours",
                "heure"
                ]


        self.questions = [
                "quelle",
        ]

        # structure intent
        self.timer_intent = IntentBuilder(self.intent)\
                .require("TimerKeyword")\
                .optionally("Delay")\
                .optionally("Question")\
                .build()

    def register(self, engine):
        for wk in self.timer_keyword:
            engine.register_entity(wk, "TimerKeyword")
        for wk in self.questions:
            engine.register_entity(wk, "Question")
        engine.register_intent_parser(self.timer_intent)
        engine.register_regex_entity(".*prévien[a-z]* moi dans (?P<Delay>.*)")
        engine.register_regex_entity(".*timer de (?P<Delay>.*)")
        engine.register_regex_entity(".*rebours de (?P<Delay>.*)")

    def process(self, json):
        if json.get('Question') == 'quelle':
            return datetime.datetime.strftime(datetime.datetime.now(), "il est %H:%M")

if __name__ == "__main__":
    engine = IntentDeterminationEngine()
    skill = TimerSkill()
    skill.register(engine)
    for intent in engine.determine_intent(' '.join(sys.argv[1:])):
        if intent and intent.get('confidence') > 0:
            print(json.dumps(intent, indent=4))
