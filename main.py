from pylsl import StreamInlet

from PyQt5 import QtCore, QtWidgets
import pyqtgraph as pg

import pylslhandler

timestamp_arr, TP9_arr, AF7_arr, AF8_arr, TP10_arr, AUX_arr = ([] for i in range(6))

tickInterval = 1 #milliseconds
yRange = 1700 #microVolts
xRange = 500 #milliseconds of readings

class LiveEEGViewer(pg.GraphicsWindow):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.mainLayout = QtWidgets.QVBoxLayout()
        self.setLayout(self.mainLayout)
        
        self.timer = QtCore.QTimer(self)
        self.timer.setInterval(tickInterval)
        self.timer.start()
        self.timer.timeout.connect(self.pullData)

        self.plt = self.addPlot(title="Muse Raw EEG Stream (red: TP9, green: AF7, blue: AF8, pink: TP10)")
        
        self.plt.setLabel("left", "Potential (uV)", color="grey")
        
        self.plt.setYRange(-yRange, yRange)

        self.curve_TP9 = self.plt.plot(pen=pg.mkPen(color=(255, 0, 0)))
        self.curve_AF7 = self.plt.plot(pen=pg.mkPen(color=(0, 255, 0)))
        self.curve_AF8 = self.plt.plot(pen=pg.mkPen(color=(0, 0, 255)))
        self.curve_TP10 = self.plt.plot(pen=pg.mkPen(color=(255, 0, 255)))
        #self.curve_AUX = self.plt.plot(pen=pg.mkPen(color=(0, 255, 255)))

    def setData(self, x, yTP9, yAF7, yAF8, yTP10, yAUX):
        self.curve_TP9.setData(x, yTP9)
        self.curve_AF7.setData(x, yAF7)
        self.curve_AF8.setData(x, yAF8)
        self.curve_TP10.setData(x, yTP10)
        #self.curve_AUX.setData(x, yAUX)

    def pullData(self):
        sample, timestamp = inlet.pull_sample()
        
        if len(TP9_arr) >= xRange:
            TP9_arr.pop(0)
            AF7_arr.pop(0)
            AF8_arr.pop(0)
            TP10_arr.pop(0)
            #AUX_arr.pop(0)
            timestamp_arr.pop(0)

        #convert relative values to electrical potential (uV)
        #range=1000, voltage=3.3, gain of AFE=1961
        TP9_arr.append((sample[0]/1000)*3.3*(1/1961)*1000000)
        AF7_arr.append((sample[1]/1000)*3.3*(1/1961)*1000000)
        AF8_arr.append((sample[2]/1000)*3.3*(1/1961)*1000000)
        TP10_arr.append((sample[3]/1000)*3.3*(1/1961)*1000000)
        #AUX_arr.append((sample[4]/1000)*3.3*(1/1961)*1000000)
        timestamp_arr.append(timestamp)

        self.setData(timestamp_arr, TP9_arr, AF7_arr, AF8_arr, TP10_arr, AUX_arr)

def main():
    app = QtWidgets.QApplication([])
    window = LiveEEGViewer()
    window.show()
    window.resize(800,600)
    window.setWindowTitle('Muse Raw EEG Stream')
    window.raise_()
    app.exec_()

if __name__ == "__main__":
    #first resolve an EEG stream on the lab network
    streams = pylslhandler.resolve_conn()
    print("Connection established")

    #create a new inlet to read from the stream
    inlet = StreamInlet(streams[0])

    main()