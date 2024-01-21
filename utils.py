from pynput.keyboard import Key, Controller
keyboard = Controller()

global active_keys
active_keys = []



def printControls():
	title = "Numpad Controls"
	controls = [
		("Num-1", "Exit"),
		("Num-0", "Play/Pause"),

		("Arrow-left", "Rewind"),
		("Arrow-right", "Advance"),

		("Num-7", "Reset Speed"),
		("Arrow-up", "Speed Up"),
		("Arrow-down", "Slow Down"),
		
		("Enter", "Restart")
	]

	print(f"\n{'=' * 20}\n{title.center(20)}\n{'=' * 20}")

	for key, action in controls:
		print(f"{key.ljust(10)} : {action}")

	print(f"{'=' * 20}\n")



lowercase_map = {
	'!': '1', 
	'@': '2', 
	'£': '3', 
	'$': '4', 
	'%': '5', 
	'^': '6', 
	'&': '7', 
	'*': '8', 
	'(': '9', 
	')': '0'
}



def requiresShift(character):

	asciiValue = ord(character)
	if(asciiValue >= 65 and asciiValue <= 90):
		return True

	if(character in "!@#$%^&*()_+{}|:\"<>?"):
		return True
	
	return False

def pressKey(key):
	global active_keys

	if requiresShift(key):

		if key in lowercase_map:
			key = lowercase_map[key]
		else:
			key = key.lower()

		keyboard.release(key)
		keyboard.press(Key.shift)
		keyboard.press(key)
		keyboard.release(Key.shift)

	else:
		keyboard.release(key)
		keyboard.press(key)

	if not key in active_keys:
		active_keys.append(key)
	
def releaseKey(key):
	global active_keys

	if requiresShift(key):

		if key in lowercase_map:
			key = lowercase_map[key]
		else:
			key = key.lower()

		keyboard.release(key)
	else:
		keyboard.release(key)
	
	if key in active_keys:
		active_keys.remove(key)

def releaseAllKeys():

	for key in active_keys:
		keyboard.release(key)
	active_keys.clear()