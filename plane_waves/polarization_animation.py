"""

Animation of plane wave polarization.
Feb. 28, 2015
G. Nordin

"""

from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import pyqtgraph as pg
import numpy as np
import sys

app = QtGui.QApplication([])
w = gl.GLViewWidget()
w.opts['distance'] = 5
w.resize(800,600)
w.show()
w.setWindowTitle('Propagating plane wave')

g = gl.GLGridItem()
#g.rotate(90,1,0,0)
w.addItem(g)

degtorad = np.pi/180.0

# Function to create new array from old where new array is formatted to prepare to
# draw lines perpendicular from z-axis to curve defined by input array
def preptomakelines(pts):
    pts2 = np.zeros(shape=(2*pts.shape[0], pts.shape[1]))
    for i in range(pts.shape[0]):
        pts2[2*i,2] = pts[i,2]
        pts2[2*i + 1,:] = pts[i,:]
    return pts2

psi_deg = 45.0
delta_deg = 90.0
# Calculate sinusoidal electric field for arbitrary polarization
def efield_arbpol(t,z,amplitude,psi_rad,delta_rad):
    x = amplitude * np.cos(psi_rad) * np.cos(2*np.pi*(t-z))
    y = amplitude * np.sin(psi_rad) * np.cos(2*np.pi*(t-z) + delta_rad)
    z = z
    return x, y, z

# Prep coordinate rotations for electric & magnetic fields to go from calculation
# coordinates to pyqtgraph plotting coordinates
temp2Darray = [[-1, 0, 0],
               [0, 0, 1],
               [0, 1, 0]]
rot_efield_coord = np.array(temp2Darray)

# Calculate electric & magnetic field arrays. Also make arrays to define lines.
amplitude = 1.0
z = np.linspace(-10, 10, 500)
x, y, z = efield_arbpol(0.0,z,amplitude,psi_deg*degtorad,delta_deg*degtorad)
pts_e = np.vstack([x,y,z]).transpose()
pts_e_lines = preptomakelines(pts_e)
pts_e = np.dot(pts_e, rot_efield_coord)
pts_e_lines = np.dot(pts_e_lines, rot_efield_coord)
z0 = np.zeros(len(z))
pts_e_z0 = np.vstack([x,y,z0]).transpose()
pts_e_z0 = np.dot(pts_e_z0, rot_efield_coord)
pts_arrow = np.array( [[0.0, 0.0, 0.0], pts_e_z0[0]] )

# Get ready to make plots
efield_color = (255, 0, 0, 255)
efield_color_z0 = (255, 255, 255, 255)
linewidth = 2.0
linewidth2Dpol = 4.0

# Make plots
plt_e = gl.GLLinePlotItem(pos=pts_e, mode='line_strip', color=efield_color, width=linewidth, antialias=True)
w.addItem(plt_e)
#plt_e_lines = gl.GLLinePlotItem(pos=pts_e_lines, mode='lines', color=efield_color, width=linewidth, antialias=True)
#w.addItem(plt_e_lines)
plt_e_z0 = gl.GLLinePlotItem(pos=pts_e_z0, mode='line_strip', color=efield_color_z0, width=linewidth2Dpol, antialias=True)
w.addItem(plt_e_z0)
plt_arrow = gl.GLLinePlotItem(pos=pts_arrow, mode='line_strip', color=efield_color_z0, width=linewidth2Dpol, antialias=True)
w.addItem(plt_arrow)


# Add lines to visually define axes
x_length = 1.1
y_length = 1.1
z_length = 10
axis_color = (255, 0, 255, 255)
## make z-axis
zaxis = np.linspace(-z_length,z_length,10)
x_zaxis = np.zeros(10)
y_zaxis = np.zeros(10)
pts_zaxis = np.vstack([x_zaxis,zaxis,y_zaxis]).transpose()
plt_zaxis = gl.GLLinePlotItem(pos=pts_zaxis, color=axis_color, width=linewidth, antialias=True)
w.addItem(plt_zaxis)
## make y-axis
yaxis = np.linspace(-y_length,y_length,10)
x_yaxis = np.zeros(10)
z_yaxis = np.zeros(10)
pts_yaxis = np.vstack([yaxis,z_yaxis,x_yaxis]).transpose()
plt_yaxis = gl.GLLinePlotItem(pos=pts_yaxis, color=axis_color, width=linewidth, antialias=True)
w.addItem(plt_yaxis)
## make x-axis
xaxis = np.linspace(-x_length,x_length,10)
y_xaxis = np.zeros(10)
z_xaxis = np.zeros(10)
pts_xaxis = np.vstack([y_xaxis,z_xaxis,xaxis]).transpose()
plt_xaxis = gl.GLLinePlotItem(pos=pts_xaxis, color=axis_color, width=linewidth, antialias=True)
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

# Set up some animation parameters
frametime = 50 # frame refresh time in ms
velocity = 1./frametime
counter = 0

# Function to update scene for each frame
def update():
    global z, z0, velocity, counter, amplitude
    global plt_e, rot_efield_coord, plt_e_z0, plt_arrow #, plt_e_lines
    global psi_deg, delta_deg, degtorad
    counter +=1
    time = float(counter)/frametime % 1
    x, y, z = efield_arbpol(time,z,amplitude,psi_deg*degtorad,delta_deg*degtorad)
    pts_e = np.vstack([x,y,z]).transpose()
    pts_e_lines = preptomakelines(pts_e)
    pts_e = np.dot(pts_e, rot_efield_coord)
    #pts_e_lines = np.dot(pts_e_lines, rot_efield_coord)
    plt_e.setData(pos=pts_e)
    #plt_e_lines.setData(pos=pts_e_lines)
    pts_e_z0 = np.vstack([x,y,z0]).transpose()
    pts_e_z0 = np.dot(pts_e_z0, rot_efield_coord)
    plt_e_z0.setData(pos=pts_e_z0)
    pts_e_arrow = np.array( [[0.0, 0.0, 0.0], pts_e_z0[len(pts_e_z0)/2.0]] )
    plt_arrow.setData(pos=pts_e_arrow)

    
# Set up timer for animation
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)

## Start Qt event loop unless running in interactive mode.
if __name__ == '__main__':
    import sys
    if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
        QtGui.QApplication.instance().exec_()
