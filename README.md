# Muse EEG LSL Monitor
This project uses pylsl and pyqt5 to connect to a Muse EEG headband over LSL protocol and display real-time EEG data. For this demo, BlueMuse by kowalej was used, a Windows 10 app that streams data from Muse headset over Bluetooth via LSL (Lab Streaming Layer). Due to BlueMuse, the code does not rely on any specific Bluetooth hardware, and should work with any module supporting BT 4.0. The monitor displays real-time raw EEG waveforms at accurate electrical potentials, at maximum frequency supported by the device, with minimal latency. 

## Demo
![Muse EEG LSL Monitor - animated gif demo](demo.gif)

Displayed electrodes are as follows TP9 (red), AF7 (green), AF8 (blue), TP10 (pink). AUX channel is disabled for this demo.

## Requirements
Assumes installation of Python 3.7 on Windows 10, owning a Muse EEG headband and Bluetooth 4.0 PC module.

To run the monitor:
* Get BlueMuse at https://github.com/kowalej/BlueMuse
* pip install -r requirements.txt

## Instructions
* Turn on Muse Headband and set it to pairing mode (do not pair Muse with your Bluetooth module).
* Open BlueMuse, wait for list to update, click on your Muse device and then click `Start Streaming`
* Once Muse headset is online and streaming, in the project directory run `python main.py`
* After use, close the monitor before disconnecting Muse device.


Additionally: by default the monitor displays 4 main electrode channels, to display input from the auxillary channel, you'll need to uncomment lines that mention `AUX`.

## Known Issues
* Resizing the window will introduce delay to data render, restarting the monitor resets it.

## License
The code in this project is licensed under the MIT License. See [LICENSE](LICENSE) for details.
