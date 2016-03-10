__author__ = 'gcrielou'
# coding=UTF-8

"""
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

class WeatherSkill(object):

    def __init__(self):

        # define vocabulary
        self.weather_keyword = [
                "weather",
                "temps",
                "météo"
                ]

        self.weather_types = [
                "snow",
                "rain",
                "wind",
                "sleet",
                "sun"
                ]

        self.locations = [
                "Seattle",
                "San Francisco",
                "Tokyo",
                "Nantes"
                ]

        # structure intent
        self.weather_intent = IntentBuilder("WeatherIntent")\
                .require("WeatherKeyword")\
                .optionally("WeatherType")\
                .require("Location")\
                .build()

    def register(self, engine):
        for l in self.locations:
            engine.register_entity(l, "Location")
        for wt in self.weather_types:
            engine.register_entity(wt, "WeatherType")
        for wk in self.weather_keyword:
            engine.register_entity(wk, "WeatherKeyword")
        engine.register_intent_parser(self.weather_intent)

if __name__ == "__main__":
    engine = IntentDeterminationEngine()
    skill = WeatherSkill()
    skill.register(engine)
    for intent in engine.determine_intent(' '.join(sys.argv[1:])):
        if intent and intent.get('confidence') > 0:
            print(json.dumps(intent, indent=4))
