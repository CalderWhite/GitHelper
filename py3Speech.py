import speech_recognition, pyttsx, sys

def get_mics():
        audio_devices = speech_recognition.Microphone.list_microphone_names()
        mics = []
        for i in range(0,len(audio_devices)):
                name = audio_devices[i]
                if name.lower().find("microphone") > -1:
                        mic_pack = {
                                "index" : i,
                                "name" : name
                                }
                        mics.append(mic_pack)
                        
        return mics

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

class ArtificialIntelligence(object):
        def __init__(self,mic,name,user_name,assistance_package):
                self.mic_index = mic
                self.recognizer = speech_recognition.Recognizer()
                self.user_name = user_name
                self.name = name
                self.speech_engine = pyttsx.init('sapi5') # see http://pyttsx.readthedocs.org/en/latest/engine.html#pyttsx.init
                self.speech_engine.setProperty('rate', 150)
                self.assistance_package = __import__("assistant_drivers." + assistant_package)
        def say(self,text):
                """play audio for whatever text is given; say it."""
                self.speech_engine.say(text)
                self.speech_engine.runAndWait()
        def listen(self,command=None,print_status=False):
                if print_status:
                        print("retriving audio...")
                with speech_recognition.Microphone(self.mic_index) as source:
                        if print_status:
                                print("adjusting to ambient noise...")
                        self.recognizer.adjust_for_ambient_noise(source)
                        if print_status:
                                print("listening, say things now.")
                        if command != None:
                                self.say(command)
                        audio = self.recognizer.listen(source)
                if print_status:
                        print("processing audio...")
                
                try:
                        # return recognizer.recognize_sphinx(audio)
                        return self.recognizer.recognize_google(audio)
                        # will not work offline ^ (google)
                except speech_recognition.UnknownValueError:
                        print("Could not understand audio")
                except speech_recognition.RequestError as e:
                        print("Recog Error; {0}".format(e))
                
                return ""
        def choose_mic(self):
                mics = get_mics()
                if len(mics) < 1:
                        self.say("Error: no microphones to take input!")
                        raise Exception("No microphones to take audio (speech) input.")
                for i in mics:
                        print("%s | mic: [%s] index: %s" % (mics.index(i),i["name"],i["index"]))
                self.say("which microphone will you use?")
                
                micNum = int(input("which mic will you use? (int):"))
                self.mic_index = mics[micNum]["index"]
        def give_assistance(self,message=None):
                if message != None:
                        self.say(message)
                response = self.listen(command="Yes Sir?")
                self.assistance_package.run(response)
        def assistance_loop(self):
                """run a loop, and when the bot name is said, it will ask if anything is needed and listen"""
                looping = True
                while looping:
                        audio = self.listen()
                        audio = audio.lower()
                        if audio != "":
                                print(audio)
                        if audio.find(self.name.lower()) > -1:
                                self.give_assistance(message="Just a moment Sir.")
                        elif audio.find("shut down") > -1 or audio.find("shutdown") > -1:
                                looping = False
                                sys.exit()
                pass
        def run(self):
                self.choose_mic()
                self.say("I'm llistening whenever you need me Sir!")
                self.assistance_loop()
                pass
def main():
        jarvis = ArtificialIntelligence(1,"Jarvis","Calder")
        jarvis.run()

if __name__ == '__main__':
        main()
