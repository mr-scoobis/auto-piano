from utils import pressKey, releaseKey, releaseAllKeys, printControls

from threading import Timer
from random import random, uniform

from pynput.keyboard import Key, Listener

import midiToQwerty

global current_note_index
current_note_index = 0

global playback_speed
playback_speed = 1

global is_playing
is_playing = False



def cacheQwertyNotes():

	with open("output.txt", "r") as qwertyNotes:
		lines = qwertyNotes.read().split("\n")
		length = (len(lines) - 1)

		cachedNotes = []
		for index, line in enumerate(lines):
			line = line.split(" ")
			nextLine = lines[min([length, index + 1])].split(" ")

			delay = (float(nextLine[0]) - float(line[0]))
			pressedNotes = line[1][1:]
			releasedNotes = line[2][1:]

			cachedNotes.append([delay, pressedNotes, releasedNotes])
		
	return cachedNotes



def playNextNote():
	global current_note_index

	if not is_playing:
		releaseAllKeys()
		return False

	if current_note_index >= (len(cachedNotes) - 1):
		current_note_index = 0
		releaseAllKeys()
		return False

	delay = cachedNotes[current_note_index][0] / playback_speed

	for releasedKey in cachedNotes[current_note_index][2]:
		releaseKey(releasedKey)

	for pressedKey in cachedNotes[current_note_index][1]:
		pressKey(pressedKey)
	
	current_note_index += 1
	Timer(delay, playNextNote).start()



def togglePlaying():
	global is_playing
	is_playing = not is_playing

	if is_playing:
		playNextNote()
		print("Playing...")
	else:
		print("Stopping...")

def escape():
	return False

def speedUp(increase):
	global playback_speed
	playback_speed *= increase

	print(f"Playback speed is now {playback_speed}")

def slowDown(decrease):
	global playback_speed
	playback_speed /= decrease

	print(f"Playback speed is now {playback_speed}")

def resetSpeed(normal):
	global playback_speed
	playback_speed = normal

	print("Resetting playback speed...")

def fastForward(time):
	global current_note_index
	current_note_index = min([(current_note_index + time), (len(cachedNotes) - 1)])

	print(f"Skipped to {current_note_index}")

def rewind(time):
	global current_note_index
	current_note_index = max([(current_note_index - time), 0])

	print(f"Rewound to {current_note_index}")

def restart():
	global current_note_index
	current_note_index = 0

	print(f"Restarted song.")

key_bindings = {
	"Key.end": [escape, True],
	"Key.insert": [togglePlaying, True],
	
	"Key.up": [speedUp, True, [1.1]],
	"Key.down": [slowDown, True, [1.1]],
	"Key.home": [resetSpeed, True, [1]],

	"Key.right": [fastForward, True, [10]],
	"Key.left": [rewind, True, [10]],

	"Key.delete": [restart, True]
}



def onKeyPress(key):
	global is_playing

	try:

		keyString = str(key)
		if not keyString in key_bindings:
			return True

		allowWhilePlaying = key_bindings[keyString][1]
		if not allowWhilePlaying and is_playing:
			return True

		keyEvent = key_bindings[keyString][0]
		if len(key_bindings[keyString]) >= 3:
			returnValue = keyEvent(*key_bindings[keyString][2])
		else:
			returnValue = keyEvent()
		if returnValue != None:
			return returnValue

	except AttributeError:
		pass



def main():
	global cachedNotes, is_playing, current_note_index
	cachedNotes = cacheQwertyNotes()

	printControls()

	with Listener(on_press=onKeyPress) as listener:
		listener.join()

	is_playing = False
	current_note_index = 0

	releaseAllKeys()

	midiToQwerty.main()

if __name__ == "__main__":
	main()