"""

Animation of propagating plane wave electric and magnetic fields.
Feb. 27, 2015
G. Nordin

"""

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np

app = QtGui.QApplication([])
w = gl.GLViewWidget()
#w.opts['distance'] = 3
w.resize(800,600)
w.show()
w.setWindowTitle('Propagating plane wave')

g = gl.GLGridItem()
w.addItem(g)

ax = gl.GLAxisItem()
ax.setSize(1.5,4,1.5)
w.addItem(ax)
  
def efield(t,z):
    x = np.cos(2*np.pi*(t-z))
    y = np.zeros(len(z))
    z = z
    return x, y, z
  
# Make a linear space from 0 to 4pi (i.e. 2 revolutions), get coords
z = np.linspace(0, 8, 200)
x, y, z = efield(0.0,z)

pts = np.vstack([y,z,x]).transpose()
#plt = gl.GLLinePlotItem(pos=pts, color=pg.mkColor(0,0,255), width=2., antialias=True)
plt = gl.GLLinePlotItem(pos=pts, width=1., antialias=True)
w.addItem(plt)

frametime = 50 # frame refresh time in ms
velocity = 1./frametime
counter = 0

def update():
    global z, velocity, plt, counter
    counter +=1
    time = float(counter)/frametime % 1
    x, y, z = efield(time,z)
    pts = np.vstack([y,z,x]).transpose()
    plt.setData(pos=pts)
    
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
