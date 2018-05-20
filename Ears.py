import speech_recognition as SR
from Mouth import Mouth
import winsound
import os
import inspect
import logging


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

dexSay = Mouth()
BING_KEY = "ed706d100bc5471d996f49af80cf0961"

class Ears():
    def __init__(self):
        '''Initialize all the speech recognition reqs'''
        self.recognizer = SR.Recognizer()
        self.microphone = SR.Microphone()

    def listen(self, dexActive):

        with self.microphone as source:
            self.recognizer.adjust_for_ambient_noise(source)

            if dexActive:
                # VK_MEDIA_PLAY_PAUSE = 0xB3
                # hwcode = win32api.MapVirtualKey(VK_MEDIA_PLAY_PAUSE, 0)
                # win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, hwcode)

                winsound.PlaySound(
                    os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '\AUDIO\highbeep.wav',
                    winsound.SND_FILENAME)

            print("...")
            try:
                if dexActive:
                    user_speech = self.recognizer.listen(source, timeout=None, phrase_time_limit=5)
                else:
                    user_speech = self.recognizer.listen(source, timeout=1.6, phrase_time_limit=5)
            except:
                return None

        try:
            if dexActive:
                # VK_MEDIA_PLAY_PAUSE = 0xB3
                # hwcode = win32api.MapVirtualKey(VK_MEDIA_PLAY_PAUSE, 0)
                # win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, hwcode)

                winsound.PlaySound(
                    os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '\AUDIO\lowbeep.wav',
                    winsound.SND_FILENAME)

            dexRecog = self.recog_speech(self.recognizer, user_speech)
            logger.info(dexRecog)
        except SR.UnknownValueError:
            dexSay.speak("Didn't catch that.", 'm', dexActive)
            self.listen(dexActive)
        except SR.RequestError as e:
            dexSay.speak("Sorry. The internet isn't responding.", 'm', True)
            return 'RequestError'
        except:
            dexSay.speak("An unknown error has occurred.", 'm', True)
        else:
            return dexRecog

    def recog_speech(self ,recognizer, user_speech):

        try:
            logger.info("Google free")
            dexRecog = self.recognizer.recognize_google(user_speech)
        except:
            logger.info("BING")
            dexRecog = self.recognizer.recognize_bing(user_speech, key=BING_KEY)

        dexRecog = dexRecog.lower()
        return dexRecog
