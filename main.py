import numpy as np
from pyqtgraph.Qt import QtCore, QtGui
import pyqtgraph.opengl as gl
import sys
from opensimplex import OpenSimplex

#FOR MAC BIG SUR, RUN THIS COMMAND TO INSTALL OPENGL#
'''try:
    import OpenGL as ogl
    try:
        import OpenGL.GL   # this fails in <=2020 versions of Python on OS X 11.x
    except ImportError:
        print('Drat, patching for Big Sur')
        from ctypes import util
        orig_util_find_library = util.find_library
        def new_util_find_library( name ):
            res = orig_util_find_library( name )
            if res: return res
            return '/System/Library/Frameworks/'+name+'.framework/'+name
        util.find_library = new_util_find_library
except ImportError:
    pass'''
class Terrain(object):
    def __init__(self):
        self.app = QtGui.QApplication(sys.argv)
        self.w = gl.GLViewWidget()
        self.w.setGeometry(0, 110, 1920, 1080)
        self.w.show()
        self.w.setWindowTitle('Terrain Generation')
        self.w.setCameraPosition(distance=35, elevation=3)

        
        self.nsteps = 1
        self.ypoints = range(-20, 22, self.nsteps)
        self.xpoints = range(-20, 22, self.nsteps)
        self.nfaces = len(self.ypoints)
        self.offset = 0


        self.tmp = OpenSimplex()


        verts = np.array([
            [
                x, y, 1.5 * self.tmp.noise2d(x=n / 5, y=m / 5)
            ] for n, x in enumerate(self.xpoints) for m, y in enumerate(self.ypoints)
        ], dtype=np.float32)


        faces = []
        colors = []
        for m in range(self.nfaces - 1):
            yoff = m * self.nfaces
            for n in range(self.nfaces - 1):
                faces.append([n + yoff, yoff + n + self.nfaces, yoff + n + self.nfaces + 1])
                faces.append([n + yoff, yoff + n + 1, yoff + n + self.nfaces + 1])
                colors.append([0, 0, 0, 0])
                colors.append([0, 0, 0, 0])

        faces = np.array(faces)
        colors = np.array(colors)


        self.m1 = gl.GLMeshItem(vertexes=verts,faces=faces, faceColors=colors,smooth=False, drawEdges=True,)
        self.m1.setGLOptions('additive')
        self.w.addItem(self.m1)

    def update(self):
        verts = np.array([
            [
                x, y, 2.5 * self.tmp.noise2d(x=n / 5 + self.offset, y=m / 5 + self.offset)
            ] for n, x in enumerate(self.xpoints) for m, y in enumerate(self.ypoints)
        ], dtype=np.float32)

        faces = []
        colors = []
        for m in range(self.nfaces - 1):
            yoff = m * self.nfaces
            for n in range(self.nfaces - 1):
                faces.append([n + yoff, yoff + n + self.nfaces, yoff + n + self.nfaces + 1])
                faces.append([n + yoff, yoff + n + 1, yoff + n + self.nfaces + 1])
                #CHANGE THE COLORS HERE#
                colors.append([n / self.nfaces, 1 - n / self.nfaces, m / self.nfaces, 0.7])
                colors.append([n / self.nfaces, 1 - n / self.nfaces, m / self.nfaces, 0.8])

        faces = np.array(faces, dtype=np.uint32)
        colors = np.array(colors, dtype=np.float32)

        self.m1.setMeshData(
            vertexes=verts, faces=faces, faceColors=colors
        )
        #CHANGE THE SPEED HERE#
        self.offset -= 0.08

    def start(self):
        if (sys.flags.interactive != 1) or not hasattr(QtCore, 'PYQT_VERSION'):
            QtGui.QApplication.instance().exec_()

    def animation(self):
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(10)
        self.start()
        self.update()


if __name__ == '__main__':
    terrain = Terrain()
    terrain.animation()
