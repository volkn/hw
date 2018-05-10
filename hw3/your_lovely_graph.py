import sys
import time
import threading
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import *
import requests
import matplotlib

matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np

BTC = "BTC"
ETH = "ETH"
USDT = "USDT"

class App(QWidget):

    def __init__(self):
        super().__init__()
        self.top = 10
        self.left = 10
        self.width = 400
        self.height = 330
        self.window()

    def window(self):
        self.setGeometry(self.left, self.top, self.width, self.height)
        
        #self.plot_button = QPushButton("PLOT",self)
        #self.plot_button2 = QPushButton("PLOT WITH ZOOM EVENT",self)
        
        self.listWidget = QtWidgets.QListWidget()
        #self.listWidget2 = QtWidgets.QListWidget()
        self.listWidget.addItem(BTC)
        self.listWidget.addItem(ETH)
        self.listWidget.addItem(USDT)

        self.listing = QtWidgets.QListWidget()

        list_box = QtWidgets.QVBoxLayout()
        list_box.addStretch()
        list_box.addWidget(self.listWidget)
        list_box.addStretch()
        list_box.addWidget(self.listing)
        list_box.addStretch()
        #list_box.addWidget(self.plot_button)
        #list_box.addStretch()
        #list_box.addWidget(self.plot_button2)
        self.setLayout(list_box)
        
        self.listWidget.itemClicked.connect(self.list_available_things)
        self.listing.itemClicked.connect(self.ploting2)
        self.show()

    def list_available_things(self):
        self.thing = self.listWidget.currentItem()
        url = "https://bittrex.com/api/v1.1/public/getmarketsummaries"
        answer = requests.get(url)
        some = answer.json()

        if self.thing.text() == "BTC":
            self.listing.clear()
            for i in range(len(some['result'])):
                if some['result'][i]["MarketName"][:3] == self.thing.text():
                    self.listing.addItem(some["result"][i]["MarketName"][4:])
        elif self.thing.text()== ETH:
            self.listing.clear()
            for i in range(len(some['result'])):
                if some['result'][i]["MarketName"][:3] == self.thing.text():
                    self.listing.addItem(some["result"][i]["MarketName"][4:])
        elif self.thing.text == USDT:
            self.listing.clear()
            for i in range(len(some['result'])):
                if some['result'][i]["MarketName"][:4] == self.thing.text():
                    self.listing.addItem(some["result"][i]["MarketName"][5:])
        else:
            for i in range(100):
                self.listing.addItem("please insert one of the three 'BTC, ETH, USDT'")
#
#    def ploting(self):
#        self.thing2 = self.listing.currentItem()
#        url = "https://bittrex.com/api/v1.1/public/getmarkethistory?market={}-{}".format(self.thing.text(),self.thing2.text())
#        data = requests.get(url).json()["result"]
#        time_list = []
#        price_list = []
#        figsrc, axsrc = plt.subplots()
#        figzoom, axzoom = plt.subplots()
#
#        for i in range(len(data)):
#            if "TimeStamp" in data[i]:
#                time_list.append(data[i]["TimeStamp"][11:19])
#                price_list.append(data[i]["Price"])
#        time_list.reverse()
#        price_list.reverse()
#        a = np.linspace(0, 100.0, num=len(time_list))
#        b = np.array(price_list)
#
#        def onpress(event):
#            if event.button != 1:
#                return
#            x, y = event.xdata, event.ydata
#            axzoom.set_xlim(x - 10, x + 10)
#            axzoom.set_ylim(y-((price_list[0]+price_list[-1])/1000), y+((price_list[0]+price_list[-1])/1000))
#            figzoom.canvas.draw()
#
#        axsrc.plot(a, b)
#        axzoom.plot(a,b)
#        plt.ylabel("PRICE")
#        plt.xlabel("TIME")
#        plt.xscale('linear')
#        figsrc.canvas.mpl_connect('button_press_event', onpress)
#        plt.show()
#

    def ploting2(self):
        self.thing3 = self.listing.currentItem()
        url = "https://bittrex.com/api/v1.1/public/getmarkethistory?market={}-{}".format(self.thing.text(),self.thing3.text())
        data = requests.get(url).json()["result"]
        time_list = []
        price_list = []
        #figsrc, axsrc = plt.subplots()
        #figzoom, axzoom = plt.subplots()

        for i in range(len(data)):
            if "TimeStamp" in data[i]:
                time_list.append(data[i]["TimeStamp"][11:19])
                price_list.append(data[i]["Price"])
        time_list.reverse()
        price_list.reverse()
        a = np.linspace(0, 100.0, num=len(time_list))
        b = np.array(price_list)
        
        fig = plt.figure()
        ax = fig.add_subplot(111)
        ax.plot(a,b)
        ax.set_title('Click to zoom')
        scale = 1.1
        zp = ZoomPan()
        plt.ylabel("PRICE")
        plt.xlabel("TIME")
        plt.xscale('linear')
        figZoom = zp.zoom_factory(ax, base_scale = scale)
        figPan = zp.pan_factory(ax)
        plt.show()
        
        
class ZoomPan:
    def __init__(self):
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None

    
    def zoom_factory(self, ax, base_scale = 2.):
        def zoom(event):
            cur_xlim = ax.get_xlim()
            cur_ylim = ax.get_ylim()
    
            xdata = event.xdata # get event x location
            ydata = event.ydata # get event y location
    
            if event.button == 'down':
                # deal with zoom in
                scale_factor = 1 / base_scale
            elif event.button == 'up':
                # deal with zoom out
                scale_factor = base_scale
            else:
                # deal with something that should never happen
                scale_factor = 1
       #         print event.button
    
            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
    
            relx = (cur_xlim[1] - xdata)/(cur_xlim[1] - cur_xlim[0])
            rely = (cur_ylim[1] - ydata)/(cur_ylim[1] - cur_ylim[0])
    
            ax.set_xlim([xdata - new_width * (1-relx), xdata + new_width * (relx)])
            ax.set_ylim([ydata - new_height * (1-rely), ydata + new_height * (rely)])
            ax.figure.canvas.draw()
    
        fig = ax.get_figure() # get the figure of interest
        fig.canvas.mpl_connect('scroll_event', zoom)
    
        return zoom
    
    def pan_factory(self, ax):
        def onPress(event):
            if event.inaxes != ax: return
            self.cur_xlim = ax.get_xlim()
            self.cur_ylim = ax.get_ylim()
            self.press = self.x0, self.y0, event.xdata, event.ydata
            self.x0, self.y0, self.xpress, self.ypress = self.press
    
        def onRelease(event):
            self.press = None
            ax.figure.canvas.draw()
    
        def onMotion(event):
            if self.press is None: return
            if event.inaxes != ax: return
            dx = event.xdata - self.xpress
            dy = event.ydata - self.ypress
            self.cur_xlim -= dx
            self.cur_ylim -= dy
            ax.set_xlim(self.cur_xlim)
            ax.set_ylim(self.cur_ylim)
    
            ax.figure.canvas.draw()
    
        fig = ax.get_figure() # get the figure of interest
    
        # attach the call back
        fig.canvas.mpl_connect('button_press_event',onPress)
        fig.canvas.mpl_connect('button_release_event',onRelease)
        fig.canvas.mpl_connect('motion_notify_event',onMotion)
    
        #return the function
        return onMotion
    


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
