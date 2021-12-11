
from PyQt5 import QtCore, QtGui, QtWidgets


class airEvacWindow(QtWidgets.QDialog):
    #Created a signal to send selections back to main window
    selectionSignal = QtCore.pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
		
        self.title = "Kabin Seçin"
        self.left = 500
        self.top = 200
        self.width = 800
        self.height = 480
        self.iconName = "mouseicon.png"
		
        self.initUI()
        
    def initUI(self):
        
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        
        self.cabinChoiceGroupBox = QtWidgets.QGroupBox()
        self.cabinChoiceGroupBox.setObjectName("cabinChoiceGroupBox")
        self.cabinChoiceGroupBox.setTitle("Hangi bölmelerdeki havanın boşaltılmasını istiyorsunuz ?")

        self.horizontalLayout = QtWidgets.QHBoxLayout(self.cabinChoiceGroupBox)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.mouseCabinCheckBox = QtWidgets.QCheckBox(self.cabinChoiceGroupBox)
        self.mouseCabinCheckBox.setObjectName("mouseCabinCheckBox")
        self.mouseCabinCheckBox.setText("Fare Kabini")
        self.horizontalLayout.addWidget(self.mouseCabinCheckBox)
        
        self.cigaretteCabinCheckBox = QtWidgets.QCheckBox(self.cabinChoiceGroupBox)
        self.cigaretteCabinCheckBox.setObjectName("cigaretteCabinCheckBox")
        self.cigaretteCabinCheckBox.setText("Sigara Kabini")
        self.horizontalLayout.addWidget(self.cigaretteCabinCheckBox)
        
        self.gridLayout.addWidget(self.cabinChoiceGroupBox, 0, 0, 1, 2)
        
        spacerItem = QtWidgets.QSpacerItem(362, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 1, 0, 1, 1)
        
        self.returnPushButton = QtWidgets.QPushButton()
        self.returnPushButton.setObjectName("returnPushButton")
        self.returnPushButton.setText("Tamam")
        self.returnPushButton.clicked.connect(self.saveAndReturn)
        self.gridLayout.addWidget(self.returnPushButton, 1, 1, 1, 1)
        
        self.setLayout(self.gridLayout)
        
        self.show()
        
    def saveAndReturn(self):
        #.emit method of pyqtSignal sends a message to main window
        if self.mouseCabinCheckBox.isChecked() and self.cigaretteCabinCheckBox.isChecked():
            self.selectionSignal.emit('both')
        elif self.mouseCabinCheckBox.isChecked():
            self.selectionSignal.emit('mouseCabin')
        elif self.cigaretteCabinCheckBox.isChecked():
            self.selectionSignal.emit('cigaretteCabin')
        
        self.close()
        