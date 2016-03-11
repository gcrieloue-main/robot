# coding=UTF-8
import speech_recognition as sr
import requests
import skills
from skills import *
import sys, inspect
import pkgutil
from adapt.engine import IntentDeterminationEngine
import json
import signal
import sys
import time
import argparse

def signal_handler(signal, frame):
    print('Robot say goodbye.')
    sys.exit(0)
signal.signal(signal.SIGINT, signal_handler)

#url = 'http://192.168.1.14:8080'
#requests.get('%s/%s' % (url, 'text/test'))

engine = IntentDeterminationEngine()
skillDict = {}

print('== INIT ==')

for importer, modname, ispkg in pkgutil.iter_modules(skills.__path__):
    clsmembers = inspect.getmembers(sys.modules['skills.%s'%(modname)], inspect.isclass)
    for (name, value) in [(n, v) for (n, v) in clsmembers if n.endswith('Skill')]:
        print('register %s'%name)
        skill = value()
        skill.register(engine)
        if hasattr(skill, 'intent'):
            skillDict[skill.intent] = skill

print('== START ==')

# obtain audio from the microphone
#r = sr.Recognizer()

def phase1(source, r):
    #print("Say keyword !")
    #try:
    #audio = r.listen(source)
    #except WaitTimeoutError: # listening timed out, just try again
    #                            pass
    #text = r.recognize_sphinx(audio)
    text='robot'
    if text == 'robot':
        phase2(source, r)
    time.sleep(0.1)
    phase1(source,r)

def phase2(source, r):
    #print("Say command!")
    #audio = r.listen(source)
    #text = r.recognize_google(audio, language="fr-FR")
    text='what''s the weather like in tokyo'
    process(text)

def process(text):
    hasResult = False
    for intent in engine.determine_intent(text):
        if intent and intent.get('confidence') > 0:
            print(json.dumps(intent, indent=4))
            if intent.get('intent_type') in skillDict:
                obj = skillDict[intent.get('intent_type')]
                if hasattr(obj, 'process'):
                    result = obj.process(intent)
                    if result != None:
                        print(result)
                        hasResult = True
    if not hasResult:
        print('...')

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='')
    parser.add_argument('texts', metavar='text', type=str, nargs='*',
                    help='text to be evaluated')
    parser.add_argument('-d', action='store_true', help='enable dynamic interpreter')

    args = parser.parse_args()

    for arg in args.texts:
        print(arg)
        process(arg)

    if args.d:
        while (True):
            text = str(input("> "))
            process(text)

    #with sr.Microphone() as source:
    #   r.adjust_for_ambient_noise(source) # listen for 1 second to calibrate the energy threshold for ambient noise levels
    #source = None
    #r = None
    #phase1(source, r)
