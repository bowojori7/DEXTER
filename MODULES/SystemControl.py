import re
from Mouth import Mouth
from Ears import Ears
import time
import pywinauto
import subprocess
import ctypes
import comtypes
from ctypes import wintypes
import win32api

MMDeviceApiLib = comtypes.GUID(
    '{2FDAAFA3-7523-4F66-9957-9D5E7FE698F6}')
IID_IMMDevice = comtypes.GUID(
    '{D666063F-1587-4E43-81F1-B948E807363F}')
IID_IMMDeviceCollection = comtypes.GUID(
    '{0BD7A1BE-7A1A-44DB-8397-CC5392387B5E}')
IID_IMMDeviceEnumerator = comtypes.GUID(
    '{A95664D2-9614-4F35-A746-DE8DB63617E6}')
IID_IAudioEndpointVolume = comtypes.GUID(
    '{5CDF2C82-841E-4546-9722-0CF74078229A}')
CLSID_MMDeviceEnumerator = comtypes.GUID(
    '{BCDE0395-E52F-467C-8E3D-C4579291692E}')

# EDataFlow
eRender = 0 # audio rendering stream
eCapture = 1 # audio capture stream
eAll = 2 # audio rendering or capture stream

# ERole
eConsole = 0 # games, system sounds, and voice commands
eMultimedia = 1 # music, movies, narration
eCommunications = 2 # voice communications

LPCGUID = REFIID = ctypes.POINTER(comtypes.GUID)
LPFLOAT = ctypes.POINTER(ctypes.c_float)
LPDWORD = ctypes.POINTER(wintypes.DWORD)
LPUINT = ctypes.POINTER(wintypes.UINT)
LPBOOL = ctypes.POINTER(wintypes.BOOL)
PIUnknown = ctypes.POINTER(comtypes.IUnknown)

class IMMDevice(comtypes.IUnknown):
    _iid_ = IID_IMMDevice
    _methods_ = (
        comtypes.COMMETHOD([], ctypes.HRESULT, 'Activate',
            (['in'], REFIID, 'iid'),
            (['in'], wintypes.DWORD, 'dwClsCtx'),
            (['in'], LPDWORD, 'pActivationParams', None),
            (['out','retval'], ctypes.POINTER(PIUnknown), 'ppInterface')),
        comtypes.STDMETHOD(ctypes.HRESULT, 'OpenPropertyStore', []),
        comtypes.STDMETHOD(ctypes.HRESULT, 'GetId', []),
        comtypes.STDMETHOD(ctypes.HRESULT, 'GetState', []))

PIMMDevice = ctypes.POINTER(IMMDevice)

class IMMDeviceCollection(comtypes.IUnknown):
    _iid_ = IID_IMMDeviceCollection

PIMMDeviceCollection = ctypes.POINTER(IMMDeviceCollection)

class IMMDeviceEnumerator(comtypes.IUnknown):
    _iid_ = IID_IMMDeviceEnumerator
    _methods_ = (
        comtypes.COMMETHOD([], ctypes.HRESULT, 'EnumAudioEndpoints',
            (['in'], wintypes.DWORD, 'dataFlow'),
            (['in'], wintypes.DWORD, 'dwStateMask'),
            (['out','retval'], ctypes.POINTER(PIMMDeviceCollection),
             'ppDevices')),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetDefaultAudioEndpoint',
            (['in'], wintypes.DWORD, 'dataFlow'),
            (['in'], wintypes.DWORD, 'role'),
            (['out','retval'], ctypes.POINTER(PIMMDevice), 'ppDevices')))
    @classmethod
    def get_default(cls, dataFlow, role):
        enumerator = comtypes.CoCreateInstance(
            CLSID_MMDeviceEnumerator, cls, comtypes.CLSCTX_INPROC_SERVER)
        return enumerator.GetDefaultAudioEndpoint(dataFlow, role)

class IAudioEndpointVolume(comtypes.IUnknown):
    _iid_ = IID_IAudioEndpointVolume
    _methods_ = (
        comtypes.STDMETHOD(ctypes.HRESULT, 'RegisterControlChangeNotify', []),
        comtypes.STDMETHOD(ctypes.HRESULT, 'UnregisterControlChangeNotify', []),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetChannelCount',
            (['out', 'retval'], LPUINT, 'pnChannelCount')),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'SetMasterVolumeLevel',
            (['in'], ctypes.c_float, 'fLevelDB'),
            (['in'], LPCGUID, 'pguidEventContext', None)),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'SetMasterVolumeLevelScalar',
            (['in'], ctypes.c_float, 'fLevel'),
            (['in'], LPCGUID, 'pguidEventContext', None)),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetMasterVolumeLevel',
            (['out','retval'], LPFLOAT, 'pfLevelDB')),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetMasterVolumeLevelScalar',
            (['out','retval'], LPFLOAT, 'pfLevel')),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'SetChannelVolumeLevel',
            (['in'], wintypes.UINT, 'nChannel'),
            (['in'], ctypes.c_float, 'fLevelDB'),
            (['in'], LPCGUID, 'pguidEventContext', None)),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'SetChannelVolumeLevelScalar',
            (['in'], wintypes.UINT, 'nChannel'),
            (['in'], ctypes.c_float, 'fLevel'),
            (['in'], LPCGUID, 'pguidEventContext', None)),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetChannelVolumeLevel',
            (['in'], wintypes.UINT, 'nChannel'),
            (['out','retval'], LPFLOAT, 'pfLevelDB')),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetChannelVolumeLevelScalar',
            (['in'], wintypes.UINT, 'nChannel'),
            (['out','retval'], LPFLOAT, 'pfLevel')),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'SetMute',
            (['in'], wintypes.BOOL, 'bMute'),
            (['in'], LPCGUID, 'pguidEventContext', None)),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetMute',
            (['out','retval'], LPBOOL, 'pbMute')),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetVolumeStepInfo',
            (['out','retval'], LPUINT, 'pnStep'),
            (['out','retval'], LPUINT, 'pnStepCount')),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'VolumeStepUp',
            (['in'], LPCGUID, 'pguidEventContext', None)),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'VolumeStepDown',
            (['in'], LPCGUID, 'pguidEventContext', None)),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'QueryHardwareSupport',
            (['out','retval'], LPDWORD, 'pdwHardwareSupportMask')),
        comtypes.COMMETHOD([], ctypes.HRESULT, 'GetVolumeRange',
            (['out','retval'], LPFLOAT, 'pfLevelMinDB'),
            (['out','retval'], LPFLOAT, 'pfLevelMaxDB'),
            (['out','retval'], LPFLOAT, 'pfVolumeIncrementDB')))
    @classmethod
    def get_default(cls):
        endpoint = IMMDeviceEnumerator.get_default(eRender, eMultimedia)
        interface = endpoint.Activate(cls._iid_, comtypes.CLSCTX_INPROC_SERVER)
        return ctypes.cast(interface, ctypes.POINTER(cls))


dexSay = Mouth()
dexHear = Ears()

moduleID = '11'

activeControlRegexes = [
    r'(.*)(shut( )*down|log( )*off|log( )*out|hibernate|suspend|restart|lock)+(.*)(computer|pc|laptop|system)',
    r'(.*)(computer|pc|laptop|system)(.*)(sleep)',
    r'(.*)shut(.*)(computer|pc|laptop|system)( )*down',
    r'(.*)log(.*)(computer|pc|laptop|system)( )*off',
    r'(.*)(volume)(.*)',
r'(.*)(play|pause|stop|next|previous)(.*)',
]

systemPowerRegexes = [
    r'(.*)(shut( )*down|log( )*off|log( )*out|hibernate|suspend|restart|lock)+(.*)(computer|pc|laptop|system)',
    r'(.*)(computer|pc|laptop|system)(.*)(sleep)',
    r'(.*)shut(.*)(computer|pc|laptop|system)( )*down',
    r'(.*)log(.*)(computer|pc|laptop|system)( )*off',
]

systemVolumeRegexes = [
    r'(.*)(volume)(.*)'
]

mediaControlRegexes = [
    r'(.*)(play|pause|stop|next song|next video|next track|previous song|previous video|previous track)(.*)'
]
def getID():
    return moduleID

def validate(data, dexActive):
    '''Return true if the module can be used to handle the input'''
    if dexActive == False:
        return False
    if dexActive == True:
        for regex in activeControlRegexes:
            if re.search(regex, data, re.I):
                return True


        return False

def handle(data, dexActive):
    '''
    1. Figure out what control function is needed
    2. Call the function
    '''

    for regex in systemPowerRegexes:
        if re.search(regex, data, re.I):
            dexSystemPower(data)
            return 'task complete'
    for regex in systemVolumeRegexes:
        if re.search(regex, data, re.I):
            dexVolume(data)
            return 'task complete'
    for regex in mediaControlRegexes:
        if re.search(regex, data, re.I):
            dexMediaControl(data)
            return 'task complete'

def dexSystemPower(data):

    query = data

    if re.search(r'shut( )*(.*)down', query):
        query = re.sub(r'(.*)', 'shutdown', query, 1, re.I)
        query = query.strip()

        dexSay.speak("Do you want me to shut your system down?", 'm', True)
        dexSay.speak("All unsaved work will be lost", 'm', True)

        try:
            option = dexHear.listen(True)
        except OSError as e:
            if 'Invalid input device' in str(e):
                dexSay.speak('Your microphone is not working properly. Please check your audio settings.', 'f',
                             True)
            if 'Unanticipated host error' in str(e):
                dexSay.speak('Your microphone is not working properly.lease check your audio settings.', 'f',
                             True)
            if 'Stream closed' in str(e):
                dexSay.speak('Changing microphone.', 'f', True)

        if option == 'RequestError' or option == None:
            dexSay.speak('Something went wrong. Please type your answer. ', 'm', True)
            option = input('>> ')

        if re.search(r'(yes|shut( )*down)', option, re.I):
            dexSay.speak("Ok. Shutting down your computer", 'm', True)
            time.sleep(1)
            dexSay.speak("Terminating Dexter", 'f', True)
            subprocess.call(["shutdown", "/s"])
            return
        else:
            dexSay.speak("okay, I won't shut your computer down", 'm', True)

    if re.search(r'log( )*(.*)off', query):
        query = re.sub(r'(.*)', 'logoff', query, 1, re.I)
        query = query.strip()

        dexSay.speak("Do you want me to log off of your system now?", 'm', True)
        dexSay.speak("All unsaved work will be lost", 'm', True)

        try:
            option = dexHear.listen(True)
        except OSError as e:
            if 'Invalid input device' in str(e):
                dexSay.speak('Your microphone is not working properly. Please check your audio settings.', 'f',
                             True)
            if 'Unanticipated host error' in str(e):
                dexSay.speak('Your microphone is not working properly.lease check your audio settings.', 'f',
                             True)
            if 'Stream closed' in str(e):
                dexSay.speak('Changing microphone.', 'f', True)

        if option == 'RequestError' or option == None:
            dexSay.speak('Something went wrong. Please type your answer. ', 'm', True)
            option = input('>> ')

        if re.search(r'(yes|log( )*off)', option, re.I):
            dexSay.speak("Ok. Logging off from your account", 'm', True)
            time.sleep(1)
            dexSay.speak("Terminating Dexter", 'f', True)
            subprocess.call(["shutdown", "/l"])
            return
        else:
            dexSay.speak("okay, I won't log you off", 'm', True)

    if re.search(r'log( )*(.*)out', query):
        query = re.sub(r'(.*)', 'logout', query, 1, re.I)
        query = query.strip()

        dexSay.speak("Do you want me to log you out from your system now?", 'm', True)
        dexSay.speak("All unsaved work will be lost", 'm', True)

        try:
            option = dexHear.listen(True)
        except OSError as e:
            if 'Invalid input device' in str(e):
                dexSay.speak('Your microphone is not working properly. Please check your audio settings.', 'f',
                             True)
            if 'Unanticipated host error' in str(e):
                dexSay.speak('Your microphone is not working properly.lease check your audio settings.', 'f',
                             True)
            if 'Stream closed' in str(e):
                dexSay.speak('Changing microphone.', 'f', True)

        if option == 'RequestError' or option == None:
            dexSay.speak('Something went wrong. Please type your answer. ', 'm', True)
            option = input('>> ')

        if re.search(r'(yes|log( )*out)', option, re.I):
            dexSay.speak("Ok. Logging you out from your account", 'm', True)
            time.sleep(1)
            dexSay.speak("Terminating Dexter", 'f', True)
            subprocess.call(["shutdown", "/l"])
            return
        else:
            dexSay.speak("okay, I won't log you out", 'm', True)

    if re.search(r'suspend', query):
        query = re.sub(r'(.*)', 'suspend', query, 1, re.I)
        query = query.strip()

        dexSay.speak("Do you want me to suspend your computer?", 'm', True)

        try:
            option = dexHear.listen(True)
        except OSError as e:
            if 'Invalid input device' in str(e):
                dexSay.speak('Your microphone is not working properly. Please check your audio settings.', 'f',
                             True)
            if 'Unanticipated host error' in str(e):
                dexSay.speak('Your microphone is not working properly.lease check your audio settings.', 'f',
                             True)
            if 'Stream closed' in str(e):
                dexSay.speak('Changing microphone.', 'f', True)

        if option == 'RequestError' or option == None:
            dexSay.speak('Something went wrong. Please type your answer. ', 'm', True)
            option = input('>> ')

        if re.search(r'(yes|suspend)', option, re.I):
            dexSay.speak("Ok. Suspending computer", 'm', True)
            time.sleep(1)
            subprocess.call('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
            return
        else:
            dexSay.speak("Alright, I won't suspend your computer", 'm', True)

    if re.search(r'sleep', query):
        query = re.sub(r'(.*)', 'sleep', query, 1, re.I)
        query = query.strip()

        dexSay.speak("Do you want me to put your computer to sleep?", 'm', True)

        try:
            option = dexHear.listen(True)
        except OSError as e:
            if 'Invalid input device' in str(e):
                dexSay.speak('Your microphone is not working properly. Please check your audio settings.', 'f',
                             True)
            if 'Unanticipated host error' in str(e):
                dexSay.speak('Your microphone is not working properly.lease check your audio settings.', 'f',
                             True)
            if 'Stream closed' in str(e):
                dexSay.speak('Changing microphone.', 'f', True)

        if option == 'RequestError' or option == None:
            dexSay.speak('Something went wrong. Please type your answer. ', 'm', True)
            option = input('>> ')

        if re.search(r'(yes|sleep)', option, re.I):
            dexSay.speak("Ok. Giving your computer sleeping pills", 'm', True)
            time.sleep(1)
            subprocess.call('rundll32.exe powrprof.dll,SetSuspendState 0,1,0')
            return
        else:
            dexSay.speak("okay, I won't put your computer to sleep", 'm', True)

    if re.search(r'hibernate', query):
        query = re.sub(r'(.*)', 'hibernate', query, 1, re.I)
        query = query.strip()

        dexSay.speak("Do you want me to hibernate your computer?", 'm', True)

        try:
            option = dexHear.listen(True)
        except OSError as e:
            if 'Invalid input device' in str(e):
                dexSay.speak('Your microphone is not working properly. Please check your audio settings.', 'f',
                             True)
            if 'Unanticipated host error' in str(e):
                dexSay.speak('Your microphone is not working properly.lease check your audio settings.', 'f',
                             True)
            if 'Stream closed' in str(e):
                dexSay.speak('Changing microphone.', 'f', True)

        if option == 'RequestError' or option == None:
            dexSay.speak('Something went wrong. Please type your answer. ', 'm', True)
            option = input('>> ')

        if re.search(r'(yes|hibernate)', option, re.I):
            dexSay.speak("Ok. Bringing winter", 'm', True)
            time.sleep(0.5)
            dexSay.speak("Hibernating", 'm', True)
            time.sleep(1)
            subprocess.call(["shutdown", "/h"])
            return
        else:
            dexSay.speak("okay, I won't hibernate your computer", 'm', True)

    if re.search(r'restart', query):
        query = re.sub(r'(.*)', 'restart', query, 1, re.I)
        query = query.strip()

        dexSay.speak("Do you want me to restart your system?", 'm', True)
        dexSay.speak("All unsaved work will be lost", 'm', True)

        try:
            option = dexHear.listen(True)
        except OSError as e:
            if 'Invalid input device' in str(e):
                dexSay.speak('Your microphone is not working properly. Please check your audio settings.', 'f',
                             True)
            if 'Unanticipated host error' in str(e):
                dexSay.speak('Your microphone is not working properly.lease check your audio settings.', 'f',
                             True)
            if 'Stream closed' in str(e):
                dexSay.speak('Changing microphone.', 'f', True)

        if option == 'RequestError' or option == None:
            dexSay.speak('Something went wrong. Please type your answer. ', 'm', True)
            option = input('>> ')

        if re.search(r'(yes|shut( )*down)', option, re.I):
            dexSay.speak("Ok. Restarting down your computer", 'm', True)
            time.sleep(1)
            subprocess.call(["shutdown", "/r"])
            return
        else:
            dexSay.speak("okay, I won't restart your computer", 'm', True)

    if re.search(r'lock', query):
        query = re.sub(r'(.*)', 'lock', query, 1, re.I)
        query = query.strip()

        dexSay.speak("Do you want me to lock your system?", 'm', True)

        try:
            option = dexHear.listen(True)
        except OSError as e:
            if 'Invalid input device' in str(e):
                dexSay.speak('Your microphone is not working properly. Please check your audio settings.', 'f',
                             True)
            if 'Unanticipated host error' in str(e):
                dexSay.speak('Your microphone is not working properly.lease check your audio settings.', 'f',
                             True)
            if 'Stream closed' in str(e):
                dexSay.speak('Changing microphone.', 'f', True)

        if option == 'RequestError' or option == None:
            dexSay.speak('Something went wrong. Please type your answer. ', 'm', True)
            option = input('>> ')

        if re.search(r'(yes|lock)', option, re.I):
            dexSay.speak("Removing access to your computer", 'm', True)
            time.sleep(1)
            subprocess.call('rundll32.exe user32.dll,LockWorkStation')
            return
        else:
            dexSay.speak("okay, I won't lock your computer", 'm', True)

def dexVolume(data):
    ev = IAudioEndpointVolume.get_default()
    query = data


    if 'increase' in query or 'raise' in query or 'up' in query or 'higher' in query or 'turn up' in query:
        dexSay.speak("Okay", 'm', True)
        ev.VolumeStepUp()
        ev.VolumeStepUp()
        ev.VolumeStepUp()
        ev.VolumeStepUp()
        ev.VolumeStepUp()
        ev.VolumeStepUp()
        ev.VolumeStepUp()
        ev.VolumeStepUp()
        ev.VolumeStepUp()
        ev.VolumeStepUp()
    if 'decrease' in query or 'reduce' in query or 'down' in query or 'lower' in query or 'turn down' in query:
        dexSay.speak("Okay", 'm', True)
        ev.VolumeStepDown()
        ev.VolumeStepDown()
        ev.VolumeStepDown()
        ev.VolumeStepDown()
        ev.VolumeStepDown()
        ev.VolumeStepDown()
        ev.VolumeStepDown()
        ev.VolumeStepDown()
        ev.VolumeStepDown()
        ev.VolumeStepDown()
    if '0' in query or 'mute'in query or 'minimum' in query or 'lowest' in query or 'kill' in query:
        dexSay.speak("Okay", 'm', True)
        ev.SetMasterVolumeLevelScalar(0.0)
    if '10' in query:
        dexSay.speak("Okay",'m',True)
        ev.SetMasterVolumeLevelScalar(0.1)
    if '20' in query:
        dexSay.speak("Okay",'m',True)
        ev.SetMasterVolumeLevelScalar(1.0)
    if '30' in query:
        dexSay.speak("Okay",'m',True)
        ev.SetMasterVolumeLevelScalar(0.3)
    if '40' in query:
        dexSay.speak("Okay",'m',True)
        ev.SetMasterVolumeLevelScalar(0.4)
    if '50' in query:
        dexSay.speak("Okay",'m',True)
        ev.SetMasterVolumeLevelScalar(0.5)
    if '60' in query:
        dexSay.speak("Okay",'m',True)
        ev.SetMasterVolumeLevelScalar(0.6)
    if '70' in query:
        dexSay.speak("Okay",'m',True)
        ev.SetMasterVolumeLevelScalar(0.7)
    if '80' in query:
        dexSay.speak("Okay",'m',True)
        ev.SetMasterVolumeLevelScalar(0.8)
    if '90' in query:
        dexSay.speak("Okay",'m',True)
        ev.SetMasterVolumeLevelScalar(0.9)
    if '100' in query or 'max' in query or 'maximum' in query or 'highest' in query:
        dexSay.speak("Okay",'m',True)
        ev.SetMasterVolumeLevelScalar(1.0)

def dexMediaControl(data):
    query = data

    if 'play' in query or 'pause' in query:
        VK_MEDIA_PLAY_PAUSE = 0xB3
        hwcode = win32api.MapVirtualKey(VK_MEDIA_PLAY_PAUSE, 0)
        win32api.keybd_event(VK_MEDIA_PLAY_PAUSE, hwcode)
    if 'stop' in query:
        VK_MEDIA_STOP = 0xB2
        hwcode = win32api.MapVirtualKey(VK_MEDIA_STOP, 0)
        win32api.keybd_event(VK_MEDIA_STOP, hwcode)
    if 'next' in query:
        VK_MEDIA_NEXT_TRACK = 0xB0
        hwcode = win32api.MapVirtualKey(VK_MEDIA_NEXT_TRACK, 0)
        win32api.keybd_event(VK_MEDIA_NEXT_TRACK, hwcode)
    if 'prev' in query:
        VK_MEDIA_PREV_TRACK = 0xB1
        hwcode = win32api.MapVirtualKey(VK_MEDIA_PREV_TRACK, 0)
        win32api.keybd_event(VK_MEDIA_PREV_TRACK, hwcode)