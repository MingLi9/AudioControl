import serial
import time
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioSessionManager2, ISimpleAudioVolume, IAudioEndpointVolume

# Define the preset applications and their order
PRESET_APPS = ["master", "chrome.exe", "spotify.exe", "", "discord.exe"]

def read_potentiometers(serial_port):
    ser = serial.Serial(serial_port, 9600)
    time.sleep(2)
    while True:
        try:
            line = ser.readline().decode('utf-8').strip()
            # Assuming the microcontroller sends data in a format like "50|75|30|75|30"
            int_list = [int(item) for item in line.split('|')]
            yield int_list
        except KeyboardInterrupt:
            break

def set_application_volume(app_name, volume_level):
    if app_name == "master":
        # Get the master volume control
        device = AudioUtilities.GetSpeakers()
        interface = device.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        volume.SetMasterVolumeLevelScalar(volume_level / 100, None)
    elif app_name:
        # Control the volume of individual applications
        sessions = AudioUtilities.GetAllSessions()
        for session in sessions:
            if session.Process and session.Process.name().lower() == app_name.lower():
                # Query for ISimpleAudioVolume interface to control the volume
                volume_control = session.SimpleAudioVolume
                volume_control.SetMasterVolume(volume_level / 100, None)

if __name__ == "__main__":
    for pot_values in read_potentiometers('COM3'):
        for i, volume in enumerate(pot_values):
            if i < len(PRESET_APPS):
                set_application_volume(PRESET_APPS[i], volume)