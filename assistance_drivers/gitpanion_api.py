from gitpanion import github_api
from random import randrange
import os, ctypes, json
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
#            data             #
###############################
windows_folder_libraries = [
        "Desktop",
        "Documents",
        "Downloads",
        "Music",
        "Pictures",
        "Videos"
        ]
###############################
#      command functions      #
###############################
def get_all_windows_open():
        """returns all windows currently open on computer using PyWin32"""
        EnumWindows = ctypes.windll.user32.EnumWindows
        EnumWindowsProc = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.POINTER(ctypes.c_int), ctypes.POINTER(ctypes.c_int))
        GetWindowText = ctypes.windll.user32.GetWindowTextW
        GetWindowTextLength = ctypes.windll.user32.GetWindowTextLengthW
        IsWindowVisible = ctypes.windll.user32.IsWindowVisible
        
        titles = []
        def foreach_window(hwnd, lParam):
        	if IsWindowVisible(hwnd):
        		length = GetWindowTextLength(hwnd)
        		buff = ctypes.create_unicode_buffer(length + 1)
        		GetWindowText(hwnd, buff, length + 1)
        		titles.append(buff.value)
        	return True
        EnumWindows(EnumWindowsProc(foreach_window), 0)
        return titles
def get_current_project():
        """attempt to find what project the user is currently working on"""
        user_path = os.path.expanduser("~")
        # get all windows open
        windows = get_all_windows_open()
        # see which window title has the user's path in it
        good_windows = []
        for i in windows:
                if i.find(user_path) > -1:
                        good_windows.append(i)
        if len(good_windows) < 1:
                # no open projects!
                return None
        path_names = []
        for base_title in good_windows:
                place = base_title.find(user_path)
                # this should work, since we already refined those that didn't have user_path earlier
                base_path = base_title[place:len(base_title)]
                base_path = base_path.split(" ")[0]
                init_path = base_path
                init_path = init_path.replace("\\","/")
                base_path = base_path.replace(user_path,"")
                base_path = base_path.replace("\\","/")
                # I could use os.listdir(user_path), but I don't want to risk
                # it if the user is working out of their user directiory.
                # (then it wouldn't work)
                for i in windows_folder_libraries:
                        base_path = base_path.replace("/" + i + "/","")
                paths = base_path.split("/")
                path_names.append({"name" : paths[0],"path" : init_path,"count" : 0})
        """
        joined_paths = ""
        for i in path_names:
                joined_paths = joined_paths + i["name"]
        if joined_paths == path_names[0]["name"] * len(path_names):
                me_path = path_names[0]["path"].split("/")
                me_path.pop(-1)
                me_path = "/".join(me_path)
                pkg = {
                        "name" : path_names[0]["name"],
                        "path" : me_path
                        }
                return pkg
        else:
        """
        if True:
                for i in path_names:
                        for j in path_names:
                                if i["name"] == j["name"]:
                                        i["count"] += 1
                #for i in path_names:
                #        print(i["name"],i["count"])
                path_names.sort(key=lambda r: r["count"],reverse=True)
                pkg = path_names[0]
                repath = pkg["path"].split("/")
                repath.pop(-1)
                repath = "/".join(repath)
                pkg["path"] = repath
                return pkg
                                        
        # ---------
        return None
def remember_current_project(pkg):
        pkg = {
                "name" : pkg["name"],
                "path" : pkg["path"]
                }
        #pkg_str = json.dumps(pkg,indent=4)
        r = open('memory/memories.json','r')
        # no ../ since this code will be run from py3Speech
        mem = json.loads(r.read())
        r.close()
        if mem.__contains__("this"):
                # if the names are the same don't push one back to the "that" position
                if mem["this"]["name"] != pkg["name"]:
                        mem["that"] = mem["this"]
                        mem["this"] = pkg
                else:
                        mem["this"] = pkg
        else:
                # this is really just for the first time you use the script
                mem["this"] = pkg
        wstr = json.dumps(mem,indent=4)
        w = open('memory/memories.json','w')
        w.write(wstr)
        w.close()
        #print(wstr)
def get_prev_project():
        r = open("memory/memories.json")
        j = json.loads(r.read())
        if j.__contains__("that"):
                return j["that"]
        else:
                # default to the current project
                return None
def local_to_github_upload(pkg,bot):
        """the package (the only required positional argument) must have the name of the repo, and the path to the file in a dictionary such as this:\n{\n      "name" : <repo name>,\n         "path" : <local file path>\n}"""
        github_path = pkg["path"][pkg["path"].find(pkg["name"]) + len(pkg["name"]) + 1 : ]
        # add 1 to the first argument of the substring so we get rid of the / character.
        cmsg = "commit from " + bot.name + " AI"
        print("reading...   | " + pkg["path"])
        global r
        global rr
        try:
                r = open(pkg["path"],'r')
                rr = r.read()
        except UnicodeDecodeError:
                r = open(pkg["path"],'rb')
                rr = r.read()
        # I do this now, so that if there's an error, it will occur after the print: "reading..."
        # not the print : "uploading..."
        # this way the user has a bit more knowledge on when and why and error occured
        print("uploading... | " + github_path)
        github_user.commit_file(github_path,cmsg,rr,pkg["branch"],pkg["name"])
def start_dir_upload(project,bot):
        path = project["path"]
        folders = next(os.walk(path))[1]
        files = next(os.walk(path))[2]
        #print(folders)
        #print("------------")
        for folder in folders:
                current_pkg = {
                        "name" : project["name"],
                        "path" : path + "/" + folder,
                        "branch" : project["branch"]
                        }
                start_dir_upload(current_pkg,bot)
        for file in files:
                file_package = {
                        "name" : project["name"],
                        "path" : path + "/" + file,
                        "branch" : project["branch"]
                        }
                local_to_github_upload(file_package,bot)
###############################
#       github functions      #
###############################
def upload_folder(pkg,bot):
        start_dir_upload(pkg,bot)
        pass
###############################
#         if callbacks        #
###############################
def back_up_prev_cb(text,bot):
        bot.say("Right away " + bot.pronoun)
        project = get_prev_project()
        if project == None:
                project = get_current_project()
                if project == None:
                        bot.say("Sir, I'm not quite sure what project you're talking about.")
                else:
                        # now user the current project
                        bot.say("I'll remember that.")
                        remember_current_project(project)
        else:
                bot.say("I know what you're talking about, but the feature isn't implimented at this time.")
        pass
def back_up_curr_cb(text,bot):
        #bot.say("Right away " + bot.pronoun)
        project = get_current_project()
        print(project["path"])
        if project == None:
                bot.say("Sir, I'm not quite sure what project you're talking about.")
        else:
                if text.find("branch") > -1:
                                bot.say("not implimented")
                                print("not implimented")
                else:
                        project["branch"] = "master"
                        remember_current_project(project)
                        upload_folder(project,bot)
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
        },
        {
                "list" : [
                        github_words["upload"],
                        github_pronouns["current_repo"]
                        ],
                "callback" : back_up_curr_cb
        },
        {
                "list" : [
                        github_words["upload"],
                        github_pronouns["previous_repo"]
                        ],
                "callback" : back_up_prev_cb
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

def for_if(string,pantheon,find=False):
        equals = False
        if type(pantheon) == type({}):
                for i in pantheon:
                        if find:
                                if string.find(i) > -1:
                                        equals = True
                        if string == pantheon[i]:
                                equals = True
        else:
                for i in pantheon:
                        if find:
                                if string.find(i) > -1:
                                        equals = True
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
                                if for_if(text,j,find=True):
                                        word_count[if_lists.index(i)] += 1
                        else:
                                if text.find(j) > -1:
                                        word_count[if_lists.index(i)] += 1
        # check if any of the checks went perfectly
        run = False
        for i in word_count:
                if i == len(if_lists[word_count.index(i)]):
                        if_lists[word_count.index(i)]["callback"].__call__(text,bot)
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

def init(bot):
        global github_user
        bot.say("If this is your first time using the gitpanion driver, \
        you may have to sign in through the web browser I'm about to open. \
        copy the code from that web page \
        and paste it in the terminal to get started using github with me.")
        oauth_token = github_api.check_oauth_token()
        github_user = github_api.GitHubUser(oauth_token)

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
if __name__ == '__main__':
        print(get_current_project())

