from os import listdir
from os.path import exists

from mido import MidiFile, tempo2bpm

import autoPiano



midi_to_piano_mapping = "1!2@34$5%6^78*9(0qQwWeErtTyYuiIoOpPasSdDfgGhHjJklLzZxcCvVbBnm"



def cacheNotes(midi, hand):
	cachedNotes = []
	pressedNotes, releasedNotes = [], []

	delay, oldDelay = 0, None

	for message in MidiFile(midi):
		if ((not hasattr(message, "note")) or (not (message.type in {"note_on", "note_off"}))):
			continue

		delay += message.time

		mapIndex = (message.note - 36)
		mapIndex = (mapIndex % 61) if mapIndex != -1 else mapIndex + 12
		if ((hand != None) and (getNoteSide(mapIndex) != hand)):
			continue
		note = midi_to_piano_mapping[mapIndex]

		if delay != (oldDelay if oldDelay != None else delay):
			cachedNotes.append([(delay - oldDelay), pressedNotes, releasedNotes])
			pressedNotes, releasedNotes = [], []

		(pressedNotes if message.type == "note_on" else releasedNotes).append(note)

		oldDelay = delay

	return cachedNotes

def getNoteSide(index):

	if index <= 26:
		return "left"
	else:
		return "right"



def main():
	path = "midi"
	if not exists(path):
		print("Midi folder does not exist, stopping.")
		return False

	midiFiles = [mid for mid in listdir("midi") if mid.endswith('.mid')]
	for index, file in enumerate(midiFiles):
		print(f"{index + 1}: {file}")
	
	midiFile = ""
	while not exists(midiFile):
		
		try:
			midiFile = f"{path}/{midiFiles[int(input("> ")) - 1]}"
		except:
			pass
	
	hand = input("Use left or right hand? (leave blank for both): \n")
	if ((hand != "left") and (hand != "right")):
		hand = None
		
	autoPiano.main((cacheNotes(midiFile, hand)))

if __name__ == "__main__":
	main()
