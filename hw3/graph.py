import requests
import sys
from PyQt5.QtWidgets import QDialog, QApplication, QPushButton, QVBoxLayout


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
import matplotlib.pyplot as plt
from matplotlib.figure import Figure
from matplotlib import style

import matplotlib.dates as mdates

class Window(QDialog):
    def __init__(self, parent=None):
        super(Window, self).__init__(parent)
        self.figure = plt.figure()
        self.canvas = FigureCanvas(self.figure)
       # self.toolbar = NavigationToolbar(self.canvas, self)
        self.press = None
        self.cur_xlim = None
        self.cur_ylim = None
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.xpress = None
        self.ypress = None
        
        self.button = QPushButton('Plot')
        self.button.clicked.connect(self.plot)
        

        layout = QVBoxLayout()
#        layout.addWidget(self.toolbar)
        layout.addWidget(self.canvas)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def MainWindow():
        pass

    def getText(self):
        self.a = input()
        self.b = input()
 
    def plot(self):
        self.getText()
        url = "https://bittrex.com/api/v1.1/public/getmarkethistory?market={}-{}".format(self.a,self.b)
        row_data = requests.get(url).json()["result"]
        time_list = []
        price_list = []

        for i in range(len(row_data)):
            if "TimeStamp" in row_data[i]:
                time_list.append(row_data[i]['TimeStamp'][14:19])#11
            if "Price" in row_data[i]:
                price_list.append(row_data[i]['Price'])
        time_list.reverse()
        price_list.reverse()

        style.use('ggplot')
        ax = self.figure.add_subplot(1,1,1)
        scale=1.1
        
        figZoom = self.zoom_factory(ax, base_scale=scale)
        figPan = self.pan_factory(ax)

        plt.plot(time_list, price_list)
        self.canvas.draw()

    def zoom_factory(self, ax, base_scale=2.):
        def zoom(event):
            cur_xlim = ax.get_xlim()
            #cur_ylim = ax.get_ylim()
            xdata = event.xdata
            #ydata = event.ydata
            if event.button == 'down':
                scale_factor = base_scale
            elif event.button == 'up':
                scale_factor = 1 / base_scale
            else:
                scale_factor = 1
            new_width = (cur_xlim[1] - cur_xlim[0]) * scale_factor
            #new_height = (cur_ylim[1] - cur_ylim[0]) * scale_factor
            relx = (cur_xlim[1] - xdata) / (cur_xlim[1] - cur_xlim[0])
            #rely = (cur_ylim[1] - ydata) / (cur_ylim[1] - cur_ylim[0])
            ax.set_xlim([xdata - new_width * (1 - relx), xdata + new_width * (relx)])
            #ax.set_ylim([ydata - new_height * (1 - rely), ydata + new_height * (rely)])
            ax.figure.canvas.draw()

        fig = ax.get_figure()
        fig.canvas.mpl_connect('scroll_event', zoom)
        return zoom

    def pan_factory(self, ax):
        def onPress(event):
            if event.inaxes != ax: return
            self.cur_xlim = ax.get_xlim()
            #self.cur_ylim = ax.get_ylim()
            self.press = self.x0,event.xdata,
            #self.press = self.y0,event.ydata
            self.x0, self.xpress, = self.press
            #self.y0,self.ypress =self.press

        def onRelease(event):
            self.press = None
            ax.figure.canvas.draw()

        def onMotion(event):
            if self.press is None: return
            if event.inaxes != ax: return
            dx = event.xdata - self.xpress
            #dy = event.ydata - self.ypress
            self.cur_xlim -= dx
            #self.cur_ylim -= dy
            ax.set_xlim(self.cur_xlim)
            #ax.set_ylim(self.cur_ylim)
            ax.figure.canvas.draw()

        def enter_figure(event):
            #event.canvas.figure.patch.set_facecolor('red')
            event.canvas.draw()
    
        fig = ax.get_figure()
        fig.canvas.mpl_connect('button_press_event', onPress)
        fig.canvas.mpl_connect('button_release_event', onRelease)
        fig.canvas.mpl_connect('motion_notify_event', onMotion)
        fig.canvas.mpl_connect('figure_enter_event', enter_figure)
        return onMotion

        
if __name__ == '__main__':
    app = QApplication(sys.argv)

    main = Window()
    main.show()

    sys.exit(app.exec_())


