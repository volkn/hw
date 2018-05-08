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

        figsrc, axsrc = plt.subplots()
        figzoom, axzoom = plt.subplots()

        for i in range(len(data)):
            if "TimeStamp" in data[i]:
                time_list.append(data[i]["TimeStamp"][11:19])
                price_list.append(data[i]["Price"])
        time_list.reverse()
        price_list.reverse()

        a = np.linspace(0, 100.0, num=len(time_list))
        b = np.array(price_list)

        def onpress(event):
            if event.button != 1:
                return
            x, y = event.xdata, event.ydata
            axzoom.set_xlim(x - 10, x + 10)
            axzoom.set_ylim(y-((price_list[0]+price_list[-1])/1000), y+((price_list[0]+price_list[-1])/1000))
            figzoom.canvas.draw()

        axsrc.plot(a, b)
        axzoom.plot(a,b)
        plt.ylabel("PRICE")
        plt.xlabel("TIME")

        plt.xscale('linear')

        figsrc.canvas.mpl_connect('button_press_event', onpress)
        plt.show()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
