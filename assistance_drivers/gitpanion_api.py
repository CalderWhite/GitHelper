from gitpanion import github_api
from random import randrange

###############################
#        swap words           #
###############################
github_words = {
    "repository" : [
        "repository",
        "repo",
        "project"
        ],
    "upload" : [
        "upload",
        "save",
        "back up",
        "backup"
        ]
    }
github_pronouns = {
        "previous_repo" : [
                "that"
                ],
        "current_repo" : [
                "this"
                ]
        }
words = {
    "callings" : [
        "hey",
        "yo",
        "ay"
        ]
    }
###############################
#         if callbacks        #
###############################
def back_up_prev_cb(text):
        pass
def back_up_curr_cb(text):
        pass
###############################
#           if list           #
###############################
if_lists = [
        {
                "list" : [
                        "back",
                        "up",
                        github_pronouns["previous_repo"]
                        ],
                "callback" : back_up_prev_cb
        },
        {
                "list" : [
                        "back",
                        "up",
                        github_pronouns["current_repo"]
                        ],
                "callback" : back_up_curr_cb
        }
        ]
###############################
#     phrase variations       #
###############################
phrases = {
        "confusion" : [
                "<pronoun>,I have no idea what you're talking about",
                "I'm afraid you're going to have to rephrase that <pronoun>.",
                "I'm not quite sure what you said <pronoun>.",
                "What do you need <pronoun>?"
                ]
        }
###############################
#        functions            #
###############################

def phrase_percent(text,desired_text):
        punc = [".",",","?","!"]
        for i in punc:
                text = text.replace(i,"")
        text = text.lower()
        t = text.split(" ")
        for i in punc:
                desired_text = desired_text.replace(i,"")
        desired_text = desired_text.lower()
        dt = desired_text.split(" ")
        percent = 0
        
        # first the short pass, 100% accuracy
        if text == desired_text:
                percent = 100
                return percent
        # next see how many correct words are in the string
        wrdc = 0
        for i in dt:
                if text.find(i) > -1:
                        wrdc += 1
        wrdp = ( wrdc / len(t) ) * 100
        # divide by text in case there are extra words in text, resulting in a larger numerator and an unfair denominator
        # now see what words are spot on with where they should be in the sentance (and is supposed to be there)
        pwrdc = 0
        for i in range(0,len(t)):
                wrd = t[i]
                global err
                err = False
                try:
                        dwrd = dt[i]
                except IndexError:
                        print("err: " + str(i))
                        err = True
                if err == False:
                        if wrd == dwrd:
                                pwrdc +=1
        pwp = ( pwrdc / len(t) ) * 100
        # divide by text in case there are extra words in text, resulting in a larger numerator and an unfair denominator
        avg = ( (wrdp / 1.5) + (pwp * 1.5) ) / 2
        return avg

def for_if(string,pantheon):
        equals = False
        if type(pantheon) == type({}):
                for i in pantheon:
                        if string == pantheon[i]:
                                equals = True
        else:
                for i in pantheon:
                        if string == i:
                                equals = True
        return equals
def fuzzy_logic_v2(text,bot):
        word_count = []
        # populate the list
        for i in if_lists:
                word_count.append(0)
        # go through each dictionary (and then its list) and try to match words
        for i in if_lists:
                for j in i["list"]:
                        if type(j) == type([]):
                                if for_if(text,j):
                                        word_count[if_lists.index(i)] += 1
                        else:
                                if text.find(j) > -1:
                                        word_count[if_lists.index(i)] += 1
        # check if any of the checks went perfectly
        run = False
        for i in word_count:
                if i == len(if_lists[word_count.index(i)]):
                        if_lists[word_count.index(i)]["callback"](text)
                        run = True
                        break
        if run == False:
                # the AI did not get to a conclusion it understands, so it will tell the
                # user a random phrase, that displays its confusion.
                phrase = phrases["confusion"][randrange(0,len(phrases["confusion"]))]
                phrase = phrase.replace("<pronoun>",bot.pronoun)
                bot.say(phrase)
                # return false because it didn't find a command it should run out of what the user said
                return False
        else:
                # return true since it ran a command off of what the user said
                return True

def run(text,bot):
        """evaluates the <text> string and acts apon it"""
        """
        ---DEPRACATED---
        # first run through all the swap words
        text = text.split(" ")
        newString = None
        if text[0] == bot.name:
                newString == text[1:]
        elif for_if(text[0],words["callings"]):
                # I could do more, such as:
                # find jarvis, find its position in the array, and then set the
                # newString to everything after <the name>
                newString = text[2:]
        else:
                pass
        if newString == None:
                phrase = phrases["confusion"][randrange(0,len(phrases["confusion"]))]
                phrase = phrase.replace("<pronoun>",bot.pronoun)
                print(phrase)
                bot.say(phrase)
        ---DEPRACATED---
        """
        # use new version of finding words in the phrase
        if text == False:
                phrase = phrases["confusion"][randrange(0,len(phrases["confusion"]))]
                phrase = phrase.replace("<pronoun>",bot.pronoun)
                bot.say(phrase)
                res = False
        else:
                res = fuzzy_logic_v2(text,bot)
        return res
                
                

