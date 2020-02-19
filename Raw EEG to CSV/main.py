from pylsl import StreamInlet, resolve_stream
from pynput import mouse
from datetime import date
import time
import pandas as pd
import matplotlib.pyplot as plt
pd.set_option('float_format', '{:f}'.format)

timeout = 1 #seconds

streams = resolve_stream('type', 'EEG')
timestamp = 0
sample = []

def on_click(x, y, button, pressed):
    raw_eeg_data.append([timestamp,*sample,1])

raw_eeg_data = []

listener = mouse.Listener(
    on_click=on_click)
listener.start()

inlet = StreamInlet(streams[0])
print('Recording began. To insert a marker, click left mouse button.')

cur_time = inlet.pull_sample()[1]

while True:
    sample, timestamp = inlet.pull_sample()
    raw_eeg_data.append([timestamp,*sample,0])
    
    if timestamp > cur_time + timeout:
        listener.stop()
        break

raw_eeg_data = sorted(raw_eeg_data, key=lambda x: x[0])

df = pd.DataFrame(data=raw_eeg_data)
df = df.drop_duplicates(0, keep='last')

print('Recording complete. Number of samples collected: ', len(df.index))

today = date.today().strftime('%d%m%Y')
file_name = '%s_%s_%s.csv' % ('p300', today, 'test')

df.to_csv(file_name, index=False, header=['timestamp','tp9','af7','af8','tp10','aux','marker'])

print('Recording has been saved to %s file in the current directory.' % (file_name))
print('Exiting...')