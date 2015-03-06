# -*- coding: utf-8 -*-
"""
Created on Fri Jul 04 10:45:53 2014

@author: moynesy
"""


import pyqtgraph.opengl as gl

import numpy as np      

from pyqtgraph import functions as fn
from pyqtgraph import Vector
from pyqtgraph import Transform3D

class MyMeshData(gl.MeshData):
    """
    Add the cone object and the arrow object in the MeshData Class
    """
    
    def __init__(self, vertexes=None, faces=None, edges=None, vertexColors=None, faceColors=None):
        gl.MeshData.__init__(vertexes=None, faces=None, edges=None, vertexColors=None, faceColors=None)



    @staticmethod
    def cone(cols, radius=3.0, length=10.0):
        """
        Return a MeshData instance with vertexes and faces computed
        for a cone surface.
        """
        verts = np.empty((cols+1, 3), dtype=float)
        ## compute vertexes
        th = np.linspace(2 * np.pi, 0, cols+1).reshape(1, cols+1)
        verts[:-1,2] = 0.0
        verts[:-1,0] = radius * np.cos(th[0,:-1]) # x = r cos(th)
        verts[:-1,1] = radius * np.sin(th[0,:-1]) # y = r sin(th)
        # Add the extremity
        verts[-1,0] = 0.0
        verts[-1,1] = 0.0
        verts[-1,2] = length
        verts = verts.reshape((cols+1), 3) # just reshape: no redundant vertices...
        ## compute faces
        faces = np.empty((cols, 3), dtype=np.uint)
        template = np.array([[0, 1]])
        for pos in range(cols):
            faces[pos,:-1] = template + pos
        faces[:,2] = cols
        faces[-1,1] = 0
        
        return gl.MeshData(vertexes=verts, faces=faces)


    @staticmethod
    def arrow(rows, cols, radius=0.1, length=1.0, fRC=2.0, fLC=0.3):
        """
        Return a MeshData instance with vertexes and faces computed
        for an arrow surface.
        it's a cylinder + a cone
        
        IN :
            - length : Arrow length
            - radius = Cylinder Radius
            - fCR = factor Cone Radius : Cone radius = fCR*radius 
            - fLC = factor Cone length of arrow length : Cone length = fLC*length
                                                         Cylinder length = length - fLC*length if fLC < 1.0 else = 0.0
                0 < flc < 1.0
            - rows : number of vertexes on radius
        
        OUT: a MeshData object.        
        
        
        TODO: add the colors for the head and cylinder
        """
        # create the cylinder
        mdCyl = None
        conL = length * fLC
        if abs(fLC) < 1.0:
            cylL = length * (1.0 - fLC)             
            mdCyl = gl.MeshData.cylinder(rows, cols, radius=[radius, radius], length=cylL)
        # create the cone
        mdCon = MyMeshData.cone(cols, radius=radius*fRC, length=conL)
        verts = mdCon.vertexes()
        nbrVertsCon = verts.size/3
        faces = mdCon.faces()
        if mdCyl is not None:
            trans = np.array([[0.0, 0.0, cylL]])
            verts = np.vstack((verts+trans, mdCyl.vertexes()))
            faces = np.vstack((faces, mdCyl.faces()+nbrVertsCon))
            print mdCyl.faceCount(), mdCon.faceCount(), faces.shape
        
        return gl.MeshData(vertexes=verts, faces=faces)
        
    @staticmethod 
    def triad(rows, cols, lx=1.0, ly=1.0, lz=1.0):  

        mdX = MyMeshData.arrow(rows, cols, length=lx, radius=0.1*lx)
        mdY = MyMeshData.arrow(rows, cols, length=ly, radius=0.1*ly)
        mdZ = MyMeshData.arrow(rows, cols, length=lz, radius=0.1*lz)       
        # Orientation
        trX = Transform3D()
        trX.rotate(90., 0.0, 1.0, 0.0)
        vertX = fn.transformCoordinates(trX, mdX.vertexes(),transpose=True)
        nbrVerts = vertX.size/3
        trY = Transform3D()
        trY.rotate(90., 1.0, 0.0, 0.0)
        vertY = fn.transformCoordinates(trY, mdY.vertexes(),transpose=True)        
        verts = np.vstack((vertX, vertY, mdZ.vertexes()))
        faces = np.vstack((mdX.faces(), mdY.faces()+nbrVerts, mdZ.faces()+2*nbrVerts))
        nbrFaces = faces.shape[0]
        #Colors x: red, y: green and z: blue
        colors = np.zeros((nbrFaces, 4))
        colors[0:nbrFaces/3] = np.array([1.0, 0.0, 0.0, 0.6])
        colors[nbrFaces/3:nbrFaces*2/3] = np.array([0.0, 1.0, 0.0, 0.6])
        colors[nbrFaces*2/3:nbrFaces] = np.array([0.0, 0.0, 1.0, 0.6])       

        return gl.MeshData(vertexes=verts, faces=faces, faceColors=colors)

