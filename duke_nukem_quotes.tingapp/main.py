import tingbot
from tingbot import *

import json
import random
import time

import helpers
# setup code here
state = {}
state['lastquotetime'] = time.time()-100
intervaltext = ""

#load quotes
with open('duke_nukem_quotes.json') as json_data:
    quotes = json.load(json_data)
    #print(quotes)

#define intervallist
intervalposition = 2
intervals=[0,1,3,5,10,20,30,40,50,60]
previousintervalposition = 1

state['backgroundcolor'] = helpers.get_random_named_color()
state['foregroundcolor'] = helpers.get_random_named_color()

#define 4 menuitems
menuitems = ["pause","slower","faster","random"]

#functions
def print_quote(quote):
    state['backgroundcolor'] = helpers.get_random_named_color()
    state['foregroundcolor'] = helpers.get_random_named_color()

    while state['backgroundcolor'] == state['foregroundcolor']:
        state['foregroundcolor'] = helpers.get_random_named_color()
            
    screen.fill(color=state['backgroundcolor'])
    screen.text(quote,color=state['foregroundcolor'],font='GibonBold.otf',font_size=25)
        
    helpers.draw_menu(screen,menuitems, state['backgroundcolor'],state['foregroundcolor'])

#buttons
@left_button.press
def pause():
    global intervalposition,previousintervalposition
    if intervalposition != 0:
        previousintervalposition = intervalposition
        intervalposition = 0
    else:
        intervalposition = previousintervalposition
    
@midleft_button.press
def slower():
    global intervalposition
    if intervalposition < len(intervals)-1:
        intervalposition +=1
        if intervalposition >= len(intervals) : intervalposition=len(intervals)-1
        state['lastquotetime'] = time.time()-100
        previousintervalposition = intervalposition

@midright_button.press
def faster():
    global intervalposition
    if intervalposition>1:
        intervalposition -=1
        if intervalposition <= 1: intervalposition=1
        state['lastquotetime'] = time.time()-100
        previousintervalposition = intervalposition
    
@right_button.press
def random_quote():
    quote = random.choice(quotes)
    print_quote(quote['quote'])    
    state['lastquotetime'] = time.time()
    
#loop
@every(seconds=1/100)
def main():
    global intervaltext
    
    if intervals[intervalposition] != 0:
        if time.time() - state['lastquotetime'] > intervals[intervalposition]:
            quote = random.choice(quotes)
            print_quote(quote['quote'])
            state['lastquotetime'] = time.time()
        intervaltext = ("interval = %i seconds"% intervals[intervalposition])
    else:
        intervaltext = "Pause"
        
    screen.rectangle(xy=(0,helpers.screen_height()), size=(helpers.screen_width(),25), color=state['backgroundcolor'],align='bottomleft')
    screen.text(intervaltext,color=state['foregroundcolor'],xy=(0,helpers.screen_height()), font_size=20,align='bottomleft')
    #time.sleep(intervals[intervalposition])

tingbot.run()