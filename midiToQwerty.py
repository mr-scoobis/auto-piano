from os import listdir
from os.path import exists

from mido import MidiFile, tempo2bpm

import autoPiano



midi_to_piano_mapping = "1!2@34$5%6^78*9(0qQwWeErtTyYuiIoOpPasSdDfgGhHjJklLzZxcCvVbBnm"



def midiToQwerty(midi, output, hand):
	
	lines = []
	pressedNotes = ["+"]
	releasedNotes = ["-"]

	delay = 0
	oldDelay = None

	for message in MidiFile(midi):

		if not hasattr(message, 'note'):
			continue

		msgType = message.type
		if (not ((msgType == "note_on") or (msgType == "note_off"))):
			continue

		delay += message.time

		mapIndex = (message.note - 36)
		mapIndex = mapIndex % 61 if mapIndex != -1 else mapIndex + 12
		if hand != None:
			if getNoteSide(mapIndex) != hand:
				continue
		note = midi_to_piano_mapping[mapIndex]

		if delay != (oldDelay if oldDelay != None else delay):
			lines.append(f"{oldDelay} {"".join(pressedNotes)} {"".join(releasedNotes)}")
			pressedNotes = ["+"]
			releasedNotes = ["-"]

		if msgType == "note_on":
			pressedNotes.append(note)
		else:
			releasedNotes.append(note)

		oldDelay = delay
	
	with open(output, "w") as outputFile:
		outputFile.write("\n".join(lines))

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

	midiToQwerty(midiFile, "output.txt", hand)

	autoPiano.main()

if __name__ == "__main__":
	main()