import tingbot
from tingbot import *

import json
import random
import time

import helpers
# setup code here
state = {}
state['lastquotetime'] = time.time()-100


screen_list = {
    0: 'show_quotes',
    1: 'list_quotes'
}
current_screen = 0
state['screen'] = screen_list[current_screen]
state['list_screen_status'] = "list"

intervaltext = ""
#load quotes
with open('duke_nukem_quotes.json') as json_data:
    quotes = json.load(json_data)
    #print(quotes)
temp_quotes = list(quotes)
random.shuffle(temp_quotes) 

#define intervallist
intervalposition = 2
intervals=[0,1,3,5,10,20,30,40,50,60]
previousintervalposition = 1

state['backgroundcolor'] = helpers.get_random_named_color()
state['foregroundcolor'] = helpers.get_random_named_color()

#define 4 menuitems_show
menuitems_show = ["pause","slower","faster","random"]
menuitems_list = ["back","up","down","show"]

#define listposition
listposition= 0

#functions
def print_quote(quote):
    state['backgroundcolor'] = helpers.get_random_named_color()
    state['foregroundcolor'] = helpers.get_random_named_color()

    while state['backgroundcolor'] == state['foregroundcolor']:
        state['foregroundcolor'] = helpers.get_random_named_color()

    screen.fill(color=state['backgroundcolor'])
    screen.text(quote,color=state['foregroundcolor'],font='GibonBold.otf',font_size=25)
    print(quote)

    if state['screen'] == 'show_quotes':
        helpers.draw_menu(screen,menuitems_show, state['backgroundcolor'],state['foregroundcolor'])
    if state['screen'] == 'list_quotes':
        helpers.draw_menu(screen,menuitems_list, state['backgroundcolor'],state['foregroundcolor'])

#buttons
@left_button.press
def pause():
    if state['screen'] == 'show_quotes':
        global intervalposition,previousintervalposition
        if intervalposition != 0:
            previousintervalposition = intervalposition
            intervalposition = 0
        else:
            intervalposition = previousintervalposition
    if state['screen'] == 'list_quotes':
        state['list_screen_status'] = 'list'

@left_button.hold
def switch_screen():
        global current_screen
        if current_screen == 1: 
            current_screen = 0
            random_quote()
        else: 
            current_screen = 1
        state['screen'] = screen_list[current_screen]

@midleft_button.press
def slower():
    if state['screen'] == 'show_quotes':
        global intervalposition
        if intervalposition < len(intervals)-1:
            intervalposition +=1
            if intervalposition >= len(intervals) : intervalposition=len(intervals)-1
            state['lastquotetime'] = time.time()-100
            previousintervalposition = intervalposition
    if state['screen'] == 'list_quotes':
        if state['list_screen_status'] == "list":
            global listposition
            if listposition > 0: listposition-=1

@midright_button.press
def faster():
    if state['screen'] == 'show_quotes':
        global intervalposition
        if intervalposition>1:
            intervalposition -=1
            if intervalposition <= 1: intervalposition=1
            state['lastquotetime'] = time.time()-100
            previousintervalposition = intervalposition
    if state['screen'] == 'list_quotes':
        if state['list_screen_status'] == "list":
            global listposition
            if listposition < len(quotes)-1: listposition+=1

@right_button.press
def random_quote():
    if state['screen'] == 'show_quotes':
        quote = random.choice(quotes)
        print_quote(quote['quote'])
        state['lastquotetime'] = time.time()
    if state['screen'] == 'list_quotes':
        print_quote(quotes[listposition]['quote'])
        state['list_screen_status'] = "detail"

#loop
@every(seconds=1/100)
def main():
    global intervaltext, temp_quotes,quotes

    if state['screen'] == 'show_quotes':

        if intervals[intervalposition] != 0:
            if time.time() - state['lastquotetime'] > intervals[intervalposition]:
                print len(temp_quotes)
                if len(temp_quotes) == 0 :
                    print "fill it up again"
                    temp_quotes = list(quotes)
                    random.shuffle(temp_quotes) 
                quote = temp_quotes.pop()
                print_quote(quote['quote'])
                state['lastquotetime'] = time.time()
            intervaltext = ("interval = %i seconds"% intervals[intervalposition])
        else:
            intervaltext = "Paused"

        screen.rectangle(xy=(0,helpers.screen_height()), size=(helpers.screen_width(),25), color=state['backgroundcolor'],align='bottomleft')
        screen.text(intervaltext,color=state['foregroundcolor'],xy=(0,helpers.screen_height()), font_size=20,align='bottomleft')
        #time.sleep(intervals[intervalposition])

    if state['screen'] == 'list_quotes':
        if state['list_screen_status'] == "list":
            #show list with all the quotes
            screen.fill(color=state['foregroundcolor'])
            helpers.draw_menu(screen,menuitems_list,state['foregroundcolor'], state['backgroundcolor'])
            
            if listposition >= 0:
                screen.rectangle(xy=(0,(helpers.screen_height()-25)/2+25), size=(helpers.screen_width(),27), color=state['backgroundcolor'], align='left')
                screen.text((" %s" %quotes[listposition]['quote']) ,color=state['foregroundcolor'],xy=(0,(helpers.screen_height()-25)/2+25), font_size=20,align='left')
            if listposition-1 >= 0:
                screen.text((" %s" %quotes[listposition-1]['quote']) ,color=state['backgroundcolor'],xy=(0,(helpers.screen_height()-25)/2-0), font_size=20,align='left')
            if listposition-2 >= 0:
                screen.text((" %s" %quotes[listposition-2]['quote']) ,color=state['backgroundcolor'],xy=(0,(helpers.screen_height()-25)/2-25), font_size=20,align='left')
            if listposition-3 >= 0:
                screen.text((" %s" %quotes[listposition-3]['quote']) ,color=state['backgroundcolor'],xy=(0,(helpers.screen_height()-25)/2-50), font_size=20,align='left')
            if listposition+1 < len(quotes):
                screen.text((" %s" %quotes[listposition+1]['quote']) ,color=state['backgroundcolor'],xy=(0,(helpers.screen_height()-25)/2+50), font_size=20,align='left')
            if listposition+2 < len(quotes):
                screen.text((" %s" %quotes[listposition+2]['quote']) ,color=state['backgroundcolor'],xy=(0,(helpers.screen_height()-25)/2+75), font_size=20,align='left')
            if listposition+3 < len(quotes):
                screen.text((" %s" %quotes[listposition+3]['quote']) ,color=state['backgroundcolor'],xy=(0,(helpers.screen_height()-25)/2+100), font_size=20,align='left')





tingbot.run()