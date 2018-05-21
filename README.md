# DEXTER
Starting out as a simple python Windows PC Personal Assistant. Helping him grow. 

#.	USER GUIDE OF THE SYSTEM

#.1	System Setup

Install Python 3.5, this version is necessary because it is the only version of python this application has been tested on. 
Install all the dependencies needed by the application through PIP
-	List of dependencies
o	Navigate to this page and get the pyqt for python version 3.5 http://www.lfd.uci.edu/~gohlke/pythonlibs/#pyqt4. Navigate to the directory where the downloaded file is, open a command prompt window at that location and run pip install PyQt4-4.11.4-cp35-none-win_amd64.whl
o	pip install SpeechRecognition
o	pip install boto3
o	pip install wolframalpha
o	pip install wikipedia
o	pip install winshell
o	pip install regex
o	pip install win32api
o	pip install pywinauto
o	pip install keyboard

Sign up for amazon Polly web service to get access to Dexter's voices, After getting the access keys, copy the access and secret keys into the appropriate files in the APIS/ directory and delete the comments to get Dexter's voice to work. 

Start Dexter. Open command window in Dexter.py location (hold shift, right click in the folder and select ‘open command prompt window here’), Type the following into the command prompt window. 
	‘python Dexter.py’
On First Run, You have to select operation mode (do not worry you can change this at any time). Choose ‘always listen’ if you want Dexter to always listen to you and answer when you call his name or     choose ‘push to talk’ if you want to use a keyboard  shortcut when you need Dexter. 
The default keyboard shortcut – ‘Control’ + ‘Caps Lock’ twice.

#.2	Command List
Guide - | means or

#.2.1	Activate Dexter
To activate Dexter or call him to attention, or give him a command you have two options. These are called operation modes:
1.	Always Listen Mode
2.	Push to talk Mode
When you start Dexter for the first time, you are asked what mode you want Dexter to operate in. Pick always listen to have Dexter always try to listen to you with all the noise and try to decipher when you have called for him.
Use Push to talk to have a call button for Dexter. Just press Ctrl+ Caps lock twice on the keyboard to call Dexter and give him a command. 
Always Listen mode has various options for calling Dexter:
	 Just say his name Dexter
	Just say any phrase with his name attached and he will answer.

#.2.2	Controlling Dexter
You can tell Dexter when you want him to terminate, go away, or change his operation mode. 
Tell Dexter to terminate and close himself
- Close|terminate|die|quit Dexter
Passive mode
-	Thank you|Thanks|Bye|shut up|go away|goodbye|later Dexter

#.2.3	Asking Dexter for the time or date
You can ask Dexter for the time or date just like how you would ask any other person for the time or date. Just tell him
-	What’s the time now?
-	What’s today’s date?


#.2.4	Help with math?
You can ask Dexter to solve a math problem. For example:
	- What is 2 plus 2
- What is the derivative of 2x squared

#.2.5	Ask Dexter to find something for you
Whether online or on your computer. You can ask Dexter to look for anything for you. Search google or youtube by saying “Search google/youtube for ….” And he will open the web page with your test results for you. Say “Search my computer for …” and he will open the search results for you on your computer. 
#.2.6	Launch Program
Need to launch a program? Just say:
- Launch|Open|Start your program name

#.2.7	Open a system location
You can open the following system locations by telling Dexter (open …. The system location ….)
-	My Music
-	My Pictures
-	My Videos
-	My documents
-	Program Files
-	Program Files (x86)
-	Control Panel
-	My computer
-	Open Drive (eg C:\\, E:\\)
-	Downloads Folder

#.2.8	System Control
You can tell Dexter to control your computer in a different number of ways:
You can say:
-	Shut down my computer
-	Log out from my system
-	Lock my pc
-	Hibernate my laptop
-	Restart my computer
-	You can ask Dexter to increase/reduce/mute your system volume
-	Play media
-	Pause song
-	Next track
-	Previous video

#.2.9	Set an alarm
You can tell Dexter to set an alarm for you for any day and he will remind you
-	Set an alarm for eight am on Wednesday
-	Set an alarm for ten thirty pm throughout this week
-	Set an alarm for two am

#.2.10	Set a reminder
You can tell Dexter to remind you about something at a particular period and he will remind you
-	Remind me to finish the report at one twenty six pm 
-	Remind me to water the plants tomorrow at one
-	Remind me to play basketball at six pm tonight
