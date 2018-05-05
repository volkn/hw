import sys
import time
import threading
from PyQt5 import QtWidgets, QtGui, QtCore
#from PyQt5.QtWidgets import QApplication, QWidget, QInputDialog, QLineEdit, QLabel, QPushButton
from PyQt5.QtWidgets import *
import requests
import matplotlib

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar

#matplotlib.use("Qt5Agg")
import matplotlib.pyplot as plt
import matplotlib.figure as Figure

import matplotlib as mpl

class App(QWidget):

    def __init__(self):
        
        super().__init__()
        self.top = 10
        self.left = 10
        self.width = 400
        self.height = 330
#        self.figure = plt.figure()
#        self.canvas = FigureCanvas(self.figure)
#       # self.toolbar = NavigationToolbar(self.canvas, self)
#        self.press = None
#        self.cur_xlim = None
#        self.cur_ylim = None
#        self.x0 = None
#        self.y0 = None
#        self.x1 = None
#        self.y1 = None
#        self.xpress = None
#        self.ypress = None
#        
 
        self.window()

    def window(self):
        
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.plot_button = QPushButton("PLOT",self)
        self.button = QPushButton('List', self)
        self.button.move(20,80)
        self.plot_button.move(140,80)

        self.textbox = QLineEdit(self)
        self.textbox.move(20, 20)
        self.textbox.resize(120,40)
        self.textbox2 = QLineEdit(self)
        self.textbox2.move(140, 20)
        self.textbox2.resize(120, 40)

        self.listWidget = QtWidgets.QListWidget()
        self.listing = QtWidgets.QListWidget()

        list_box = QtWidgets.QVBoxLayout()
        list_box.addStretch()
        list_box.addWidget(self.listing)
        self.setLayout(list_box)

        self.plot_button.clicked.connect(self.ploting)
        self.button.clicked.connect(self.list_available_things)
        self.show()

    def list_available_things(self):
        global thing
        self.thing = self.textbox.text()
        url = "https://bittrex.com/api/v1.1/public/getmarketsummaries"
        answer = requests.get(url)
        some = answer.json()

        if self.thing == "BTC":
            self.listing.clear()
            for i in range(len(some['result'])):
                if some['result'][i]["MarketName"][:3] == self.thing:
                    self.listing.addItem(some["result"][i]["MarketName"][4:])

        elif self.thing == "ETH":
            self.listing.clear()
            for i in range(len(some['result'])):
                if some['result'][i]["MarketName"][:3] == self.thing:
                    self.listing.addItem(some["result"][i]["MarketName"][4:])

        elif self.thing == "USDT":
            self.listing.clear()
            for i in range(len(some['result'])):
                if some['result'][i]["MarketName"][:4] == self.thing:
                    self.listing.addItem(some["result"][i]["MarketName"][5:])
        else:
            for i in range(100):
                self.listing.addItem("please insert one of the three 'BTC, ETH, USDT'")

    def ploting(self):
        self.thing2 = self.textbox2.text()
        url = "https://bittrex.com/api/v1.1/public/getmarkethistory?market={}-{}".format(self.thing,self.thing2)
        data = requests.get(url).json()["result"]
        time_list = []
        price_list = []

        for i in range(len(data)):
            if "TimeStamp" in data[i]:
                time_list.append(data[i]["TimeStamp"][11:19])
                price_list.append(data[i]["Price"])
        time_list.reverse()
        price_list.reverse()

        plt.plot(time_list, price_list)
        plt.ylabel("PRICE")
        plt.xlabel("TIME")
        plt.yscale('linear')
        plt.xscale('linear')

        plt.show()



#    def zoom_factory(self, ax, base_scale=2.):
#        def zoom(event):
#            cur_xlim = ax.get_xlim()
#            #cur_ylim = ax.get_ylim()
#            xdata = event.xdata
#            #ydata = event.ydata
#            if event.button == 'down':
#                scale_factor = base_scale
#            elif event.button == 'up':
#                scale_factor = 1 / base_scale
#            else:
#                scale_factor = 1
#            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
#            #new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
#            relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
#            #rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])
#            ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * (relx)])
#            #ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * (rely)])
#            ax.figure.canvas.draw()
#
#        fig = ax.get_figure()
#        fig.canvas.mpl_connect('scroll_event', zoom)
#        return zoom
#
#    def pan_factory(self, ax):
#        def onPress(event):
#            if event.inaxes != ax: return
#            self.cur_xlim = ax.get_xlim()
#            #self.cur_ylim = ax.get_ylim()
#            self.press = self.x0,event.xdata,
#            #self.press = self.y0,event.ydata
#            self.x0, self.xpress, = self.press
#            #self.y0,self.ypress =self.press
#
#        def onRelease(event):
#            self.press = None
#            ax.figure.canvas.draw()
#
#        def onMotion(event):
#            if self.press is None: return
#            if event.inaxes != ax: return
#            dx = event.xdata - self.xpress
#            #dy = event.ydata - self.ypress
#            self.cur_xlim -= dx
#            #self.cur_ylim -= dy
#            ax.set_xlim(self.cur_xlim)
#            #ax.set_ylim(self.cur_ylim)
#            ax.figure.canvas.draw()
#
#        def enter_figure(event):
#            #event.canvas.figure.patch.set_facecolor('red')
#            event.canvas.draw()
#    
#        fig = ax.get_figure()
#        fig.canvas.mpl_connect('button_press_event', onPress)
#        fig.canvas.mpl_connect('button_release_event', onRelease)
#        fig.canvas.mpl_connect('motion_notify_event', onMotion)
#        fig.canvas.mpl_connect('figure_enter_event', enter_figure)
#        return onMotion
#


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())                           
