"""

Animation of propagating plane wave wavefronts.
March 2, 2015
G. Nordin

"""

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np

app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.opts['distance'] = 20
w.resize(800,600)
w.show()
w.setWindowTitle('Propagating plane wave')

g = gl.GLGridItem()
#g.rotate(90,1,0,0)
w.addItem(g)

linewidth = 2.0

# Add lines to visually define axes
x_length = 1.1
y_length = 1.1
z_length = 10
## make z-axis
zaxis = np.linspace(-z_length,z_length,10)
x_zaxis = np.zeros(10)
y_zaxis = np.zeros(10)
pts_zaxis = np.vstack([x_zaxis,zaxis,y_zaxis]).transpose()
plt_zaxis = gl.GLLinePlotItem(pos=pts_zaxis, width=linewidth, antialias=True)
w.addItem(plt_zaxis)
## make y-axis
yaxis = np.linspace(-y_length,y_length,10)
x_yaxis = np.zeros(10)
z_yaxis = np.zeros(10)
pts_yaxis = np.vstack([yaxis,z_yaxis,x_yaxis]).transpose()
plt_yaxis = gl.GLLinePlotItem(pos=pts_yaxis, width=linewidth, antialias=True)
w.addItem(plt_yaxis)
## make x-axis
xaxis = np.linspace(-x_length,x_length,10)
y_xaxis = np.zeros(10)
z_xaxis = np.zeros(10)
pts_xaxis = np.vstack([y_xaxis,z_xaxis,xaxis]).transpose()
plt_xaxis = gl.GLLinePlotItem(pos=pts_xaxis, width=linewidth, antialias=True)
w.addItem(plt_xaxis)

## make images
image_shape = (8,8)
uniform_values = np.ones(image_shape) * 255
uniform_image_transparent = pg.makeARGB(uniform_values)[0]
uniform_image_transparent[:,:,3] = 65
v1 = gl.GLImageItem(uniform_image_transparent)
v1.translate(-image_shape[0]/2, -image_shape[1]/2, 0)
v1.rotate(90, 1,0,0)
#w.addItem(v1)
v = []
for i in range(0,20):
    vtemp = gl.GLImageItem(uniform_image_transparent)
    vtemp.translate(-image_shape[0]/2, -image_shape[1]/2, 0)
    vtemp.rotate(90, 1,0,0)
    dz = float(i - 10)
    vtemp.translate(0, dz, 0)
    v.append(vtemp)
    w.addItem(v[i])

# Set up some animation parameters
frametime = 50 # frame refresh time in ms
inv_frametime = 1./frametime
counter = 0

# Function to update scene for each frame
def update():
    global inv_frametime, counter, amplitude
    counter +=1
    time = float(counter)/frametime % 1
    if counter != 1:
        if time != 0:
            dz = inv_frametime
        else:
            dz = -1.0
    else:
        dz = inv_frametime
    #v1.translate(0, dz, 0)
    for vtemp in v:
        vtemp.translate(0, dz, 0)
    
# Set up timer for animation
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
