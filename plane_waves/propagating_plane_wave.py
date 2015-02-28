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
w.opts['distance'] = 8
w.resize(800,600)
w.show()
w.setWindowTitle('Propagating plane wave')

g = gl.GLGridItem()
#g.rotate(90,1,0,0)
w.addItem(g)

ax = gl.GLAxisItem()
ax.setSize(1.5,4,1.5)
w.addItem(ax)
  
def efield(t,z,amplitude):
    x = amplitude * np.cos(2*np.pi*(t-z))
    y = np.zeros(len(z))
    z = z
    return x, y, z

amplitude = 2.0
z = np.linspace(-10, 10, 500)
x, y, z = efield(0.0,z,amplitude)
pts_e = np.vstack([y,z,x]).transpose()
pts_h = np.vstack([x,z,y]).transpose()

efield_color = (255, 0, 0, 255)
hfield_color = (0, 0, 255, 255)
linewidth = 2.0

plt_e = gl.GLLinePlotItem(pos=pts_e, color=efield_color, width=linewidth, antialias=True)
w.addItem(plt_e)
plt_h = gl.GLLinePlotItem(pos=pts_h, color=hfield_color, width=linewidth, antialias=True)
w.addItem(plt_h)

## make z-axis
zaxis = np.linspace(-10,10,10)
x_zaxis = np.zeros(10)
y_zaxis = np.zeros(10)
pts_zaxis = np.vstack([x_zaxis,zaxis,y_zaxis]).transpose()
plt_zaxis = gl.GLLinePlotItem(pos=pts_zaxis, width=linewidth, antialias=True)
w.addItem(plt_zaxis)
## make y-axis
yaxis = np.linspace(-5,5,10)
x_yaxis = np.zeros(10)
z_yaxis = np.zeros(10)
pts_yaxis = np.vstack([yaxis,z_yaxis,x_yaxis]).transpose()
plt_yaxis = gl.GLLinePlotItem(pos=pts_yaxis, width=linewidth, antialias=True)
w.addItem(plt_yaxis)
## make x-axis
xaxis = np.linspace(-10,10,10)
y_xaxis = np.zeros(10)
z_xaxis = np.zeros(10)
pts_xaxis = np.vstack([y_xaxis,z_xaxis,xaxis]).transpose()
plt_xaxis = gl.GLLinePlotItem(pos=pts_xaxis, width=linewidth, antialias=True)
w.addItem(plt_xaxis)

'''## make images
image_shape = (6,6)
uniform_values = np.ones(image_shape) * 255
uniform_image_transparent = pg.makeARGB(uniform_values)[0]
uniform_image_transparent[:,:,3] = 230
v1 = gl.GLImageItem(uniform_image_transparent)
v1.translate(-image_shape[0]/2, -image_shape[1]/2, 0)
v1.rotate(90, 1,0,0)
w.addItem(v1)'''

frametime = 50 # frame refresh time in ms
velocity = 1./frametime
counter = 0

def update():
    global z, velocity, plt_e, plt_h, counter, amplitude
    counter +=1
    time = float(counter)/frametime % 1
    x, y, z = efield(time,z,amplitude)
    pts_e = np.vstack([y,z,x]).transpose()
    plt_e.setData(pos=pts_e)
    pts_h = np.vstack([x,z,y]).transpose()
    plt_h.setData(pos=pts_h)
    
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
