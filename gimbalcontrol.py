import keyboard
import serial
import time

ser = serial.Serial('/dev/ttyUSB0', 19200)
time.sleep(2)

min_pan, max_pan = 0x0, 0x800
min_tilt, max_tilt = 0x0, 0x600
panval, tiltval = 0x400, 0x200
panstep, tiltstep = 0x10, 0x10

def send_serial_command(prefix, value=None):
	if value is not None:
		hex_value = f"{value:03X}"[-3:]
		command = f"O{prefix}{hex_value}\n"
	else:
		command = "L\n"
	ser.write(command.encode('UTF-8'))
	print(f"Sent command: {command}")
	
def adjust_pan(increment=True):
	global panval
	if increment:
		panval = min(panval + panstep, max_pan)
	else:
		panval = max(panval - panstep, min_pan)
	send_serial_command('0', panval)
	
def adjust_tilt(increment=True):
	global tiltval
	if increment:
			tiltval = min(tiltval + tiltstep, max_tilt)
	else:
		tiltval = max(tiltval - tiltstep, min_tilt)
	send_serial_command('1', tiltval)
	
keyboard.on_press_key('up', lambda _: adjust_tilt(increment=False))
keyboard.on_press_key('down', lambda _: adjust_tilt(increment=True))
keyboard.on_press_key('right', lambda _: adjust_pan(increment=True))
keyboard.on_press_key('left', lambda _: adjust_pan(increment=False))
keyboard.on_press_key('space', lambda _: send_serial_command('F'))

try:
	print("Press arrow key to adjust values. Press 'Esc' to exit.")
	while True:
		if keyboard.is_pressed('esc'):
			break
finally:
	ser.close()
