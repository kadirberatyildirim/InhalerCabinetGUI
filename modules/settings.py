
from PyQt5 import QtCore, QtGui, QtWidgets
import sys, json
import modules.keyboard

class SettingsWindow(QtWidgets.QDialog):
    
    cigaretteTypeSignal = QtCore.pyqtSignal(str)
    resetHolderSignal = QtCore.pyqtSignal(str)
    ExpTimeSignal = QtCore.pyqtSignal(str)
    
    def __init__(self):
        super().__init__()
		
        self.title = "Ayarlar"
        self.left = 500
        self.top = 200
        self.width = 800
        self.height = 480
        self.iconName = "mouseicon.png"
		
        self.selected_button = ''
		
        self.InitWindow()
		
        self.LoadPreviousSettings()
		
    def InitWindow(self):
        self.setWindowTitle(self.title)
        self.setWindowIcon(QtGui.QIcon(self.iconName))
		#self.setGeometry(self.left, self.top, self.width, self.height)
		
		#We define a central grid layout to set QDialog windows layout
        self.CentralGridLayout = QtWidgets.QGridLayout(self)
        self.CentralGridLayout.setObjectName("CentralGridLayout")
		
		#We define a main grid layout to add objects into
        self.MainGridLayout = QtWidgets.QGridLayout()
        self.MainGridLayout.setObjectName("MainGridLayout")
		
		#We call out methods to form our other layouts
        self.SettingsUI()
		
        self.MainInputAreaUI()
		
        self.BottomUI()
		
		#Next we add our MainGridLayout to CentralGridLayout as only standing item
        self.CentralGridLayout.addLayout(self.MainGridLayout, 0, 0, 1, 1)
		
		#At last we set Central grid layout as QDialog's layout
        self.setLayout(self.CentralGridLayout)
		
        self.show()
		
    def SettingsUI(self):
		#Items that are at the top of MainGridLayout are created here
        settingsLabel = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(settingsLabel.sizePolicy().hasHeightForWidth())
        settingsLabel.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Myriad CAD")
        font.setPointSize(15)
        font.setBold(True)
        font.setUnderline(False)
        font.setWeight(75)
        settingsLabel.setFont(font)
        settingsLabel.setFrameShape(QtWidgets.QFrame.Box)
        settingsLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        settingsLabel.setLineWidth(2)
        settingsLabel.setObjectName("settingsLabel")
        settingsLabel.setText("Ayarlar")
        self.MainGridLayout.addWidget(settingsLabel, 0, 0, 1, 1)
		
		#ExperimentInfoLabel will be dynamically changed with inputs from MainInputArea
        self.ExperimentInfoLabel = QtWidgets.QLabel(self)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.ExperimentInfoLabel.sizePolicy().hasHeightForWidth())
        self.ExperimentInfoLabel.setSizePolicy(sizePolicy)
        self.ExperimentInfoLabel.setText("")
        self.ExperimentInfoLabel.setObjectName("ExperimentInfoLabel")
        self.MainGridLayout.addWidget(self.ExperimentInfoLabel, 0, 1, 1, 1)
		
    def MainInputAreaUI(self):
		#QFontLayout can help us create our input area
        MainInputArea = QtWidgets.QFormLayout()
        MainInputArea.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        MainInputArea.setLabelAlignment(QtCore.Qt.AlignCenter)
        MainInputArea.setFormAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        MainInputArea.setObjectName("MainInputArea")
		
		#Items here are objects inside MainInputArea top to bottom/left to right
		
		#First line with index 0 starts here
        self.ExperimentNameLabel = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.ExperimentNameLabel.setFont(font)
        self.ExperimentNameLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.ExperimentNameLabel.setObjectName("ExperimentNameLabel")
        self.ExperimentNameLabel.setText("Deney İsmi : ")
        MainInputArea.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.ExperimentNameLabel)
        
        firstHLayout = QtWidgets.QHBoxLayout()
        firstHLayout.setObjectName("firstHLabout")
		
        self.ExperimentNameLineEdit = QtWidgets.QLineEdit(self)
        self.ExperimentNameLineEdit.setObjectName("ExperimentNameLineEdit")
        self.ExperimentNameLineEdit.setPlaceholderText("*Tarih-Deney İsmi")
        self.ExperimentNameLineEdit.textChanged.connect(self.ExperimentInfoUpdate)
        firstHLayout.addWidget(self.ExperimentNameLineEdit)
        
        self.keyboardButton = QtWidgets.QPushButton(self)
        self.keyboardButton.setObjectName("keyboardButton")
        self.keyboardButton.setText("")
        self.keyboardButton.setIcon(QtGui.QIcon("./icons/keyboardicon.png"))
        self.keyboardButton.clicked.connect(self.showMehKeyboard)
        firstHLayout.addWidget(self.keyboardButton)
        
        MainInputArea.setLayout(0, QtWidgets.QFormLayout.FieldRole, firstHLayout)
		
		#Second line with index 1 starts here
        self.CigaretteTypeLabel = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.CigaretteTypeLabel.setFont(font)
        self.CigaretteTypeLabel.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.CigaretteTypeLabel.setObjectName("CigaretteTypeLabel")
        self.CigaretteTypeLabel.setText("Sigara Tipi :")
        MainInputArea.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.CigaretteTypeLabel)
		
		#QHBoxLayout created to insert multiple objects inside QFormLayout's FieldRole =========================
        self.ButtonsHLayout = QtWidgets.QHBoxLayout()
        self.ButtonsHLayout.setObjectName("ButtonsHLayout")

        self.NormalTypeButton = QtWidgets.QRadioButton(self)
        self.NormalTypeButton.setObjectName("NormalTypeButton")
        self.NormalTypeButton.setText("Normal")
        self.NormalTypeButton.toggled.connect(self.ExperimentInfoUpdate)
        self.ButtonsHLayout.addWidget(self.NormalTypeButton)
		
        self.IQOSButton = QtWidgets.QRadioButton(self)
        self.IQOSButton.setObjectName("IQOSButton")
        self.IQOSButton.setText("IQOS")
        self.IQOSButton.toggled.connect(self.ExperimentInfoUpdate)
        self.ButtonsHLayout.addWidget(self.IQOSButton)
		
        MainInputArea.setLayout(1, QtWidgets.QFormLayout.FieldRole, self.ButtonsHLayout)
		#ButtonsHLayout End ===========================================
		
		#Third line with index 2 starts here
        self.StayTimeLabel = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.StayTimeLabel.setFont(font)
        self.StayTimeLabel.setObjectName("StayTimeLabel")
        self.StayTimeLabel.setText("Dumanın Kabinde Kalış Zamanı : ")
        MainInputArea.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.StayTimeLabel)
		
		#QHBoxLayout created to insert multiple objects inside QFormLayout's FieldRole ===============
        self.StayTimeHLayout = QtWidgets.QHBoxLayout()
        self.StayTimeHLayout.setObjectName("StayTimeHLayout")
		
        self.StayTimeLineEdit = QtWidgets.QLineEdit(self)
        validator = QtGui.QIntValidator(0, 360, self)
        self.StayTimeLineEdit.setValidator(validator)
        self.StayTimeLineEdit.setInputMethodHints(QtCore.Qt.ImhNone)
        self.StayTimeLineEdit.setObjectName("StayTimeLineEdit")
        self.StayTimeLineEdit.setPlaceholderText("*Lütfen tam sayı olarak girin")
		#self.StayTimeLineEdit.setValidator(self, QtGui.QIntValidator)
        self.StayTimeHLayout.addWidget(self.StayTimeLineEdit)
		
        self.StayTimeUnitLabel = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.StayTimeUnitLabel.setFont(font)
        self.StayTimeUnitLabel.setObjectName("StayTimeUnitLabel")
        self.StayTimeUnitLabel.setText("dakika")
        self.StayTimeHLayout.addWidget(self.StayTimeUnitLabel)
        
        self.keyboardButton2 = QtWidgets.QPushButton(self)
        self.keyboardButton2.setObjectName("keyboardButton2")
        self.keyboardButton2.setText("")
        self.keyboardButton2.setIcon(QtGui.QIcon("./icons/keyboardicon.png"))
        self.keyboardButton2.clicked.connect(self.showMehKeyboard2)
        self.StayTimeHLayout.addWidget(self.keyboardButton2)
		
        StayTimeSpacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.StayTimeHLayout.addItem(StayTimeSpacer)
		
        MainInputArea.setLayout(3, QtWidgets.QFormLayout.FieldRole, self.StayTimeHLayout)
		#StayTimeHLayout End ===================
        
        #Sixth line with index 5 starts here
        self.resetHolderLabel = QtWidgets.QLabel(self)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        font.setBold(False)
        font.setWeight(50)
        font.setKerning(True)
        self.resetHolderLabel.setFont(font)
        self.resetHolderLabel.setObjectName("resetHolderLabel")
        self.resetHolderLabel.setText("Sigara Tutucu Konumu : ")
        MainInputArea.setWidget(5, QtWidgets.QFormLayout.LabelRole, self.resetHolderLabel)
		
		#QHBoxLayout created to insert multiple objects inside QFormLayout's FieldRole ------------------
        resetHolderHLayout = QtWidgets.QHBoxLayout()
        resetHolderHLayout.setObjectName("resetHolderHLayout")
		
        self.resetHolderButton = QtWidgets.QPushButton(self)
        self.resetHolderButton.setObjectName("resetHolderButton")
        self.resetHolderButton.setText("Sıfırla")
        self.resetHolderButton.clicked.connect(self.resetHolder)
        resetHolderHLayout.addWidget(self.resetHolderButton)
		
        resetHolderSpacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        resetHolderHLayout.addItem(resetHolderSpacer)

        MainInputArea.setLayout(5, QtWidgets.QFormLayout.FieldRole, resetHolderHLayout)
		#resetHolderHLayout End -------------------------
		
		#At last, we add this MainInputArea to our MainGridLayout
        self.MainGridLayout.addLayout(MainInputArea, 1, 0, 1, 4)
		
    def BottomUI(self):
		#Items that are at the bottom of this window are created here
        BottomSpacer = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.MainGridLayout.addItem(BottomSpacer, 2, 1, 1, 1)
		
        HelpButton = QtWidgets.QPushButton(self)
        HelpButton.setObjectName("HelpButton")
        HelpButton.setText("Yardım")
        HelpButton.clicked.connect(self.HelpWindow)
        self.MainGridLayout.addWidget(HelpButton, 2, 2, 1, 1)
		
        self.SaveButton = QtWidgets.QPushButton(self)
        self.SaveButton.setObjectName("SaveButton")
        self.SaveButton.setText("Kaydet")
        self.SaveButton.clicked.connect(self.SaveAndReturn)
        self.MainGridLayout.addWidget(self.SaveButton, 2, 3, 1, 1)
        
    def resetHolder(self):
        self.resetHolderSignal.emit('reset')
		
    def LoadPreviousSettings(self):
		#Upon pressing settings button on main window, we want the current settings to be loaded inside our objects
		#Try/Except used incase there is no settings file
        try :
            with open("settings.json", "r") as Settings_File:
                user_settings = json.load(Settings_File)
            self.ExperimentNameLineEdit.setText(user_settings['Experiment_Name'])
            self.StayTimeLineEdit.setText(user_settings['Stay_Time'])
            if user_settings['Cigarette_Type'] == 'Normal':
                self.NormalTypeButton.setChecked(True)
                self.selected_button = 'Normal'
            if user_settings['Cigarette_Type'] == 'IQOS':
                self.IQOSButton.setChecked(True)
                self.selected_button = 'IQOS'
			
        except FileNotFoundError :
            pass
		
    def ExperimentInfoUpdate(self):
		#We update the empty label (ExperimentInfoLabel) to show what data info will look like
        fixedText = 'Deney Künyesi : '
        sender = self.sender()
        if (sender.objectName() == 'NormalTypeButton'):
            self.ExperimentInfoLabel.setText(fixedText + self.ExperimentNameLineEdit.text() + ' - ' + sender.text())
            self.selected_button = sender.text()
        elif (sender.objectName() == 'IQOSButton'):
            self.ExperimentInfoLabel.setText(fixedText + self.ExperimentNameLineEdit.text() + ' - ' + sender.text())
            self.selected_button = sender.text()
        elif (sender.objectName() == 'ExperimentNameLineEdit'):
            self.ExperimentInfoLabel.setText(fixedText + self.ExperimentNameLineEdit.text() + ' - ' + self.selected_button)
		
    def SaveAndReturn(self):
		#To save settings, we open a JSON file and write our settings in there
        with open("settings.json", "w") as Settings_File:
            data = { 'Experiment_Name' : self.ExperimentNameLineEdit.text(), 'Cigarette_Type' : self.selected_button, 'Stay_Time' : self.StayTimeLineEdit.text()}
            json.dump(data, Settings_File, indent = 4)
            
        if self.selected_button == 'IQOS':
            self.cigaretteTypeSignal.emit('iqos')
        elif self.selected_button == 'Normal':
            self.cigaretteTypeSignal.emit('normal')
        
        self.ExpTimeSignal.emit(self.StayTimeLineEdit.text())
        
        self.close()
		
    def HelpWindow(self):
        message = "Deney ismi girdisinin Tarih-Deney İsmi-Sigara Tipi şeklinde olması beklenmektedir. \
                    Diğer girdilerin sayı olması beklenmektedir. "
        QtWidgets.QMessageBox.about(self, "Yardım", message)
        
    def showMehKeyboard(self):
        self.keyboard = modules.keyboard.keyboardWindow()
        self.keyboard.textToReturn.connect(self.textReturned)
        self.keyboard.showFullScreen()
        
    def showMehKeyboard2(self):
        self.keyboard = modules.keyboard.keyboardWindow()
        self.keyboard.textToReturn.connect(self.textReturned2)
        self.keyboard.showFullScreen()
        
    def textReturned(self, text):
        self.ExperimentNameLineEdit.setText(text)
        
    def textReturned2(self, text):
        try:
            int(text)
            self.StayTimeLineEdit.setText(text)
        except:
            QtWidgets.QMessageBox.about(self, "Dikkat!", 'Lütfen tam sayı giriniz!')
            self.showMehKeyboard2()
    
if __name__ == "__main__":
    App = QApplication(sys.argv)
    window = Window()
    sys.exit(App.exec())
    
