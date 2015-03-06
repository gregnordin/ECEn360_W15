from PyQt4 import QtGui, QtCore
import pyqtgraph as pg
import pyqtgraph.opengl as gl
import numpy as np
import sys
from MyMeshData import MyMeshData

def vectorlength(vec):
    sum = 0.0
    for i in range(vec.shape[0]):
        sum += vec[i]**2
    return np.sqrt(sum)

## Always start by initializing Qt (only once per application)
app = QtGui.QApplication([])

## Define a top-level widget to hold everything
w = QtGui.QWidget()
w.resize(1000,600)
w.setWindowTitle('Polarization Visualization')

## Create widgets to be placed inside
heading_text = QtGui.QLabel('Polarization Angles ' + u"\u03C8" + ' and ' + u"\u03B4")

# Box with sliders
sliderbox = QtGui.QGroupBox()
hBoxLayout = QtGui.QHBoxLayout()
psi_slider_layout = QtGui.QVBoxLayout()
delta_slider_layout = QtGui.QVBoxLayout()

# psi slider
psi_label = QtGui.QLabel(u"\u03C8")
psi_slider = QtGui.QSlider()
psi_slider.setOrientation(QtCore.Qt.Vertical)
psi_slider.setMinimum(0)
psi_slider.setMaximum(90)
psi_slider.setValue(0)
psi_value = QtGui.QLabel(str(psi_slider.value()) + u"\u00b0")
psi_slider_layout.addWidget(psi_label)
psi_slider_layout.addWidget(psi_slider)
psi_slider_layout.addWidget(psi_value)
def set_psi_value(value):
    psi_value.setText(str(value) + u"\u00b0")
    global psi_deg
    psi_deg = value
psi_slider.valueChanged.connect(set_psi_value)

# delta slider
delta_label = QtGui.QLabel(u"\u03B4")
delta_slider = QtGui.QSlider()
delta_slider.setOrientation(QtCore.Qt.Vertical)
delta_slider.setMinimum(-180)
delta_slider.setMaximum(180)
delta_slider.setValue(0)
delta_value = QtGui.QLabel(str(delta_slider.value()) + u"\u00b0")
delta_slider_layout.addWidget(delta_label)
delta_slider_layout.addWidget(delta_slider)
delta_slider_layout.addWidget(delta_value)
def set_delta_value(value):
    delta_value.setText(str(value) + u"\u00b0")
    global delta_deg
    delta_deg = value
delta_slider.valueChanged.connect(set_delta_value)

# Set layout of box containing sliders
hBoxLayout.addItem(psi_slider_layout)
hBoxLayout.addItem(delta_slider_layout)
sliderbox.setLayout(hBoxLayout)

# Create openGL view widget & add a grid
wGL = gl.GLViewWidget()
wGL.setSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Expanding)
wGL.opts['distance'] = 5
g = gl.GLGridItem()
wGL.addItem(g)

## Create a grid layout to manage the widgets size and position
layout = QtGui.QGridLayout()
w.setLayout(layout)
layout.setColumnStretch (1, 2)

## Add widgets to the layout in their proper positions
layout.addWidget(heading_text, 0, 0)   # heading text goes in upper-left
layout.addWidget(sliderbox, 1, 0)   # slider box goes underneath heading text
layout.addWidget(wGL, 0, 1, 3, 1)  # wGL goes on right side, spanning 3 rows

## Display the widget as a new window
w.show()

##------------ Set up polarization animation ------------##
degtorad = np.pi/180.0

# Function to create new array from old where new array is formatted to prepare to
# draw lines perpendicular from z-axis to curve defined by input array
def preptomakelines(pts):
    pts2 = np.zeros(shape=(2*pts.shape[0], pts.shape[1]))
    for i in range(pts.shape[0]):
        pts2[2*i,2] = pts[i,2]
        pts2[2*i + 1,:] = pts[i,:]
    return pts2

psi_deg = float(psi_slider.value())
delta_deg = float(delta_slider.value())

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
pts_arrow = np.array( [[0.0, 0.0, 0.0], pts_e_z0[len(pts_e_z0)/2.0]] )

# Get ready to make plots
efield_color = (255, 0, 0, 255)
efield_color_z0 = (255, 255, 255, 255)
efield_color_arrow = (255, 255, 255, 255)
linewidth = 2.0
linewidth2Dpol = 2.0
linewidth2Defieldvector = 7.0

# Make plots
plt_e = gl.GLLinePlotItem(pos=pts_e, mode='line_strip', color=efield_color, width=linewidth, antialias=True)
wGL.addItem(plt_e)
#plt_e_lines = gl.GLLinePlotItem(pos=pts_e_lines, mode='lines', color=efield_color, width=linewidth, antialias=True)
#wGL.addItem(plt_e_lines)
plt_e_z0 = gl.GLLinePlotItem(pos=pts_e_z0, mode='line_strip', color=efield_color_z0, width=linewidth2Dpol, antialias=True)
#wGL.addItem(plt_e_z0)
## Create arrow
arrow_length = vectorlength(pts_e_z0[len(pts_e_z0)/2.0])
arrow_md = MyMeshData.arrow(rows=10, cols=20, radius = 0.05, length=arrow_length)
psi = np.arctan2(pts_arrow[1][2], pts_arrow[1][1])
print pts_arrow, arrow_length, psi
arrow_color = np.zeros((arrow_md.faceCount(), 4), dtype=float)
arrow_color[:,0] = 1.0
arrow_color[:,3] = 1.0
arrow_md.setFaceColors(arrow_color)
arrow = gl.GLMeshItem(meshdata=arrow_md, smooth=True, drawEdges=True, edgeColor=(1,0,0,1), shader='balloon')
arrow.rotate(-90., 0, 1, 0)
wGL.addItem(arrow)

# Add lines to visually define axes
x_length = 1.1
y_length = 1.1
z_length = 10
linewidthaxis = 1.0
axis_color = (32, 32, 32, 40)
## make z-axis
zaxis = np.linspace(-z_length,z_length,10)
x_zaxis = np.zeros(10)
y_zaxis = np.zeros(10)
pts_zaxis = np.vstack([x_zaxis,zaxis,y_zaxis]).transpose()
plt_zaxis = gl.GLLinePlotItem(pos=pts_zaxis, color=axis_color, width=linewidthaxis, antialias=True)
#wGL.addItem(plt_zaxis)
## make y-axis
yaxis = np.linspace(-y_length,y_length,10)
x_yaxis = np.zeros(10)
z_yaxis = np.zeros(10)
pts_yaxis = np.vstack([yaxis,z_yaxis,x_yaxis]).transpose()
plt_yaxis = gl.GLLinePlotItem(pos=pts_yaxis, color=axis_color, width=linewidthaxis, antialias=True)
wGL.addItem(plt_yaxis)
## make x-axis
xaxis = np.linspace(-x_length,x_length,10)
y_xaxis = np.zeros(10)
z_xaxis = np.zeros(10)
pts_xaxis = np.vstack([y_xaxis,z_xaxis,xaxis]).transpose()
plt_xaxis = gl.GLLinePlotItem(pos=pts_xaxis, color=axis_color, width=linewidthaxis, antialias=True)
wGL.addItem(plt_xaxis)

## make image for x-y plane
image_shape = (2,2)
uniform_values = np.ones(image_shape) * 255
uniform_image_transparent = pg.makeARGB(uniform_values)[0]
uniform_image_transparent[:,:,3] = 100
v1 = gl.GLImageItem(uniform_image_transparent)
v1.translate(-image_shape[0]/2., -image_shape[1]/2., 0)
v1.rotate(90, 1,0,0)
wGL.addItem(v1)

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
    pts_arrow = np.array( [[0.0, 0.0, 0.0], pts_e_z0[len(pts_e_z0)/2.0]] )
    arrow_length = vectorlength(pts_e_z0[len(pts_e_z0)/2.0])
    arrow_md = MyMeshData.arrow(rows=10, cols=20, radius = 0.05, length=arrow_length)
    arrow_md.setFaceColors(arrow_color)
    arrow.setMeshData(arrow_md)
    psi = np.arctan2(pts_arrow[1][2], pts_arrow[1][1])
    arrow.rotate(psi, 0, 1, 0)

# Set up timer for animation
timer = QtCore.QTimer()
timer.timeout.connect(update)
timer.start(50)


## Start the Qt event loop
app.exec_()
