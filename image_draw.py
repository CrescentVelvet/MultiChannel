#coding=utf-8
from PyQt5 import QtGui, QtCore
from PyQt5 import QtWidgets
from matplotlib.backends.backend_qt5agg \
import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
import pyqtgraph as pg
from pyqtgraph.Point import Point
import sys

# 主体界面显示，上图p1，下图p2
win = pg.GraphicsLayoutWidget(show=False)
win.setWindowTitle('wave display')
# 显示鼠标坐标
label = pg.LabelItem(justify='right')
win.addItem(label)
# 添加两个画图界面
p1 = win.addPlot(row=1, col=0)
p2 = win.addPlot(row=2, col=0)
region = pg.LinearRegionItem()

# matplotlib画布基类
class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure(facecolor = 'white')
        self.fig.set_label('time (s)')
        self.ax = self.fig.add_subplot(111) # abc，a*b网格的第c个图
        self.ax.set_title('Original Wave')
        self.ax.set_ylabel(r'$Amplitude(V)$')
        self.ax.set_xticklabels( ('0', '1.0', '2.0', '3.0', '4.0',  '5.0'))
        self.ax.xlable = ('time(s)')
        FigureCanvas.__init__(self, self.fig)
        FigureCanvas.setSizePolicy(self,
                                QtWidgets.QSizePolicy.Expanding,
                                QtWidgets.QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)

class DrawPicture(object):
    # 由下图选区更新上图
    def update():
        region.setZValue(10)
        minX, maxX = region.getRegion()
        p1.setXRange(minX, maxX, padding=0)

    # 由下图选区更新上图
    def updateRegion(window, viewRange):
        rgn = viewRange[0]
        region.setRegion(rgn)

    # 显示鼠标当前坐标
    def mouseMoved(evt):
        pos = evt[0]
        if p1.sceneBoundingRect().contains(pos):
            mousePoint = vb.mapSceneToView(pos)
            print(mousePoint)
            index = int(mousePoint.x())
            if index > 0 and index < len(data1):
                label.setText("<span style='font-size: 12pt'>x=%0.1f,   <span style='color: red'>y1=%0.1f</span>,   <span style='color: green'>y2=%0.1f</span>" % (mousePoint.x(), data1[index], data2[index]))
            vLine.setPos(mousePoint.x())
            hLine.setPos(mousePoint.y())

# 单个画布
# class MplWidget(QtWidgets.QWidget):
#     def __init__(self, parent = None):
#         QtWidgets.QWidget.__init__(self, parent)
        # 添加matplotlib画布
        # self.canvas = MplCanvas()
        # self.vbl = QtWidgets.QVBoxLayout()
        # self.vbl.addWidget(self.canvas)
        # self.setLayout(self.vbl)

# 单个画布
class MplWidget(QtWidgets.QWidget):
    def __init__(self, parent = None):
        QtWidgets.QWidget.__init__(self, parent)
        # 添加pyqtgraph画布
        layout = QtWidgets.QGridLayout()
        self.setLayout(layout)
        # 进行下图选区
        region.setZValue(10)
        p2.addItem(region, ignoreBounds=True)
        p1.setAutoVisible(y=True)
        # 设置选区初始范围
        region.setRegion([1000, 2000])  
        # 添加随机数据
        data1 = 10000 + 15000 * pg.gaussianFilter(np.random.random(size=10000), 10) + 3000 * np.random.random(size=10000)
        data2 = 15000 + 15000 * pg.gaussianFilter(np.random.random(size=10000), 10) + 3000 * np.random.random(size=10000)
        p1.plot(data1, pen="r")
        p1.plot(data2, pen="g")
        p2.plot(data1, pen="w")
        # 由下图选区更新上图
        region.sigRegionChanged.connect(DrawPicture.update)
        # p1.sigRangeChanged.connect(DrawPicture.updateRegion)  
        # 显示鼠标十字线
        vLine = pg.InfiniteLine(angle=90, movable=False)
        hLine = pg.InfiniteLine(angle=0, movable=False)
        p1.addItem(vLine, ignoreBounds=True)
        p1.addItem(hLine, ignoreBounds=True)
        vb = p1.vb
        # proxy = pg.SignalProxy(p1.scene().sigMouseMoved, rateLimit=60, slot=DrawPicture.mouseMoved)

        layout.addWidget(win)

# 用于测试绘图
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    # 主体界面显示，上图p1，下图p2
    win = pg.GraphicsLayoutWidget(show=True)
    win.setWindowTitle('wave display')
    # 显示鼠标坐标
    label = pg.LabelItem(justify='right')
    win.addItem(label)
    # 添加两个画图界面
    p1 = win.addPlot(row=1, col=0)
    p2 = win.addPlot(row=2, col=0)
    # 进行下图选区
    region = pg.LinearRegionItem()
    region.setZValue(10)
    p2.addItem(region, ignoreBounds=True)
    p1.setAutoVisible(y=True)
    # 添加随机数据
    data1 = 10000 + 15000 * pg.gaussianFilter(np.random.random(size=10000), 10) + 3000 * np.random.random(size=10000)
    data2 = 15000 + 15000 * pg.gaussianFilter(np.random.random(size=10000), 10) + 3000 * np.random.random(size=10000)
    p1.plot(data1, pen="r")
    p1.plot(data2, pen="g")
    p2.plot(data1, pen="w")
    # 由下图选区更新上图
    region.sigRegionChanged.connect(DrawPicture.update)
    p1.sigRangeChanged.connect(DrawPicture.updateRegion)
    # 设置选区初始范围
    region.setRegion([1000, 2000])
    # 显示鼠标十字线
    vLine = pg.InfiniteLine(angle=90, movable=False)
    hLine = pg.InfiniteLine(angle=0, movable=False)
    p1.addItem(vLine, ignoreBounds=True)
    p1.addItem(hLine, ignoreBounds=True)
    vb = p1.vb
    proxy = pg.SignalProxy(p1.scene().sigMouseMoved, rateLimit=60, slot=DrawPicture.mouseMoved)
    sys.exit(app.exec_())