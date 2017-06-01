import gradientTool
import gradientTool_ui as ui
from Qt import QtCore, QtWidgets
import pymel.core as pmc
import pymel.core.datatypes as dt
Signal = QtCore.Signal

window = None

SELECTION = None
POINT1 = None
POINT2 = None

def show():
    global window

    if window is None:
        app = QtWidgets.QApplication.instance()
        mainWindow = {o.objectName(): o for o in app.topLevelWidgets()}["MayaWindow"]
        parent = mainWindow
        window = ui.create_window(parent)

        def set_selection():
            global SELECTION
            SELECTION = gradientTool.get_verts_from_selection()
        window.grabSelectionButtonClicked.connect(set_selection)

        def set_point1():
            global POINT1
            selection = pmc.selected()
            POINT1 = selection[0].getPosition()
        window.setPoint1ButtonClicked.connect(set_point1)

        def set_point2():
            global POINT2
            selection = pmc.selected()
            POINT2 = selection[0].getPosition()
        window.setPoint2ButtonClicked.connect(set_point2)

        def paint_distance_gradient():
            print SELECTION, POINT2
            gradientTool.apply_distance_gradient(SELECTION, POINT1, POINT2)
        window.distanceGradientButtonClicked.connect(paint_distance_gradient)

        def paint_radial_gradient():
            print SELECTION, POINT1
            gradientTool.apply_radial_gradient(SELECTION, POINT1)
        window.radialGradientButtonClicked.connect(paint_radial_gradient)

        def paint_vector_gradient():
            print SELECTION
            gradientTool.apply_vector_gradient(SELECTION, dt.Vector(0, 1, 0))
        window.vectorGradientButtonClicked.connect(paint_vector_gradient)



    window.show()

#from vertexcolortools import gradientTool_ui_maya, gradientTool, gradientTool_ui; reload(gradientTool); reload(gradientTool_ui); reload(gradientTool_ui_maya); gradientTool_ui_maya.show()
