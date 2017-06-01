from PySide2 import QtCore, QtGui, QtWidgets
Signal = QtCore.Signal

class GradientWindow(QtWidgets.QMainWindow):
    grabSelectionButtonClicked = Signal()
    setPoint1ButtonClicked = Signal()
    setPoint2ButtonClicked = Signal()
    distanceGradientButtonClicked = Signal()
    radialGradientButtonClicked = Signal()
    vectorGradientButtonClicked = Signal()


def create_window(parent = None):
    window = GradientWindow(parent)
    window.setWindowTitle('Coles Vertex Color Gradient Tool')

    mainContainer = QtWidgets.QWidget(window)
    buttonContainer = QtWidgets.QGroupBox('test', mainContainer)



    grabSelectionButton = QtWidgets.QPushButton('Grab Selection', buttonContainer)
    setPoint1Button = QtWidgets.QPushButton('Set Point 1', buttonContainer)
    setPoint2Button = QtWidgets.QPushButton('Set Point 2', buttonContainer)
    distanceGradientButton = QtWidgets.QPushButton('Paint Distance Gradient', buttonContainer)
    radialGradientButton = QtWidgets.QPushButton('Paint Radial Gradient', buttonContainer)
    vectorGradientButton = QtWidgets.QPushButton('Paint Vector Gradient', buttonContainer)

    painter = QtGui.QPainter(mainContainer)
    brush = QtGui.QLinearGradient(50,50,50,50)
    painter.setBrush(brush)
    painter.begin(mainContainer)

    colorDialogTest = QtWidgets.QColorDialog()
    #colorDialogTest.getColor()

    def onGrabSelectionButtonClicked():
        grabSelectionButton.setFlat(True)
        window.grabSelectionButtonClicked.emit()
    grabSelectionButton.clicked.connect(onGrabSelectionButtonClicked)

    def onSetPoint1ButtonClicked():
        setPoint1Button.setFlat(True)
        window.setPoint1ButtonClicked.emit()
    setPoint1Button.clicked.connect(onSetPoint1ButtonClicked)

    def onSetPoint2ButtonClicked():
        setPoint2Button.setFlat(True)
        window.setPoint2ButtonClicked.emit()
    setPoint2Button.clicked.connect(onSetPoint2ButtonClicked)

    def onDirectionGradientButtonClicked():
        window.distanceGradientButtonClicked.emit()
    distanceGradientButton.clicked.connect(onDirectionGradientButtonClicked)

    def onRadialGradientButtonClicked():
        window.radialGradientButtonClicked.emit()
    radialGradientButton.clicked.connect(onRadialGradientButtonClicked)

    def onVectorGradientButtonClicked():
        window.vectorGradientButtonClicked.emit()
    vectorGradientButton.clicked.connect(onVectorGradientButtonClicked)

    mainLayout = QtWidgets.QVBoxLayout(mainContainer)
    buttonLayout = QtWidgets.QVBoxLayout(buttonContainer)

    mainContainer.setLayout(mainLayout)
    buttonContainer.setLayout(buttonLayout)

    mainLayout.addWidget(buttonContainer)

    buttonLayout.addWidget(grabSelectionButton)
    buttonLayout.addWidget(setPoint1Button)
    buttonLayout.addWidget(setPoint2Button)
    buttonLayout.addWidget(distanceGradientButton)
    buttonLayout.addWidget(radialGradientButton)
    buttonLayout.addWidget(vectorGradientButton)

    window.setCentralWidget(mainContainer)

    return window

if __name__ == '__main__':
    def onGrabSelection():
        print ('Selection Grabbed!')
    def onSetPoint1():
        print ('Point 2 Set!')
    def onSetPoint2():
        print ('Point 1 Set!')
    def onPaintGradient():
        print ('Gradient Painted!')
    app = QtWidgets.QApplication([])
    win = create_window()
    win.grabSelectionButtonClicked.connect(onGrabSelection)
    win.setPoint1ButtonClicked.connect(onSetPoint1)
    win.setPoint2ButtonClicked.connect(onSetPoint2)
    win.distanceGradientButtonClicked.connect(onPaintGradient)
    win.radialGradientButtonClicked.connect(onPaintGradient)
    win.vectorGradientButtonClicked.connect(onPaintGradient)
    win.show()
    app.exec_()