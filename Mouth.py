
import time
import boto3
import os
import inspect
import pygame
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class Mouth():
    def __init__(self):
        '''Initialize the Male and Female voices'''
		
		dex_aws_access = open('APIS/dex_aws_access.txt', 'r').read()
		dex_aws_secret = open('APIS/dex_aws_secret.txt', 'r').read()
		dee_aws_access = open('APIS/dee_aws_access.txt', 'r').read()
		dee_aws_secret = open('APIS/dee_aws_secret.txt', 'r').read()

        self.Dexter = boto3.client("polly", 'us-west-2', aws_access_key_id=dex_aws_access, aws_secret_access_key=dex_aws_secret)
        self.Deedee = boto3.client("polly", 'us-west-2', aws_access_key_id=dee_aws_access, aws_secret_access_key=dee_aws_secret)


    def speak(self, audioString, gender, dexActive):

        if gender == 'm' and dexActive == True:
            try:
                self.Dexter.Voice = self.Dexter.synthesize_speech(
                    Text=audioString,
                    OutputFormat="mp3",
                    VoiceId="Brian")
            except:
                logger.info('Sorry, Dexter\'s voice is not available.')
                exit(1)

            if "AudioStream" in self.Dexter.Voice:
                with open(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '\AUDIO\dexter_speech.mp3', 'wb') as f:
                    f.write(self.Dexter.Voice['AudioStream'].read())

                logger.info(audioString)

                pygame.mixer.init()
                pygame.mixer.music.load(os.path.dirname(
                    os.path.abspath(inspect.getfile(inspect.currentframe()))) + '\AUDIO\dexter_speech.mp3')
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() == True:
                    continue

                self.delete()
                time.sleep(0.2)


        if gender == 'f' and dexActive == True:
            try:
                self.Deedee.Voice = self.Deedee.synthesize_speech(
                    Text=audioString,
                    OutputFormat="mp3",
                    VoiceId="Amy")
            except:
                logger.info('Sorry, Dexter\'s voice is not available.')
                exit(1)

            if "AudioStream" in self.Deedee.Voice:
                with open(os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + '\AUDIO\dexter_speech.mp3', 'wb') as f:
                    f.write(self.Deedee.Voice['AudioStream'].read())

                pygame.mixer.init()
                pygame.mixer.music.load(os.path.dirname(
                    os.path.abspath(inspect.getfile(inspect.currentframe()))) + '\AUDIO\dexter_speech.mp3')
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy() == True:
                    continue

                self.delete()
                time.sleep(0.2)
            logger.info(audioString)

    def startMessage(self):
        self.speak('Initializing.', 'f', True)

    def greet(self):
        time.sleep(0.8)

        if os.path.isfile('Userdetails.txt') == True:
            user = open("Userdetails.txt", 'r')
            self.speak('Hello ' + user.read(), 'm', True)
        else:
            self.speak('Hello.', 'm', True)


    def delete(self):
        pygame.mixer.music.load(os.path.dirname(
                    os.path.abspath(inspect.getfile(inspect.currentframe()))) + '\AUDIO\highbeep.wav')
        os.remove(os.path.dirname(
                    os.path.abspath(inspect.getfile(inspect.currentframe()))) + '\AUDIO\dexter_speech.mp3')