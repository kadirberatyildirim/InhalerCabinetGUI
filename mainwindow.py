# -*- coding: utf-8 -*-

from PyQt5 import QtCore, QtGui, QtWidgets
import sys, random, csv, json, os, serial
import modules.settings, modules.CreateGraph, modules.airEvacuation, modules.SaveData, modules.keyboard

class Window(QtWidgets.QMainWindow):

    def __init__(self):
        super().__init__()
		
        self.title = "Ana Ekran"
        self.top = 100
        self.left = 100
        self.width = 800
        self.height = 480
		
        self.TemperatureValues = []
        self.OxyValues = []
        self.COValues = []
        self.HumidityValues = []
        self.CO2Values = []
        
        os.system('sudo chmod 777 /dev/ttyUSB0')
        self.openArduinoPort()
        
        self.workPath = ''
        
        self.InitWindow()
        
        self.createDeneylerFolder()
		
		#Timers for data collection, label checking and auto save
        self.portTimer = QtCore.QTimer(self)
        self.portTimer.start(1000)
        self.portTimer.timeout.connect(self.readFromArduino)
		
        self.CheckForLabelTimer = QtCore.QTimer(self)
        self.CheckForLabelTimer.start(1000)
        self.CheckForLabelTimer.timeout.connect(self.FindExperimentName)
		
        self.AutoSaveTimer = QtCore.QTimer(self)
        self.AutoSaveTimer.start(300000)
        self.AutoSaveTimer.timeout.connect(self.AutoSave)
		
    def InitWindow(self):
        self.setWindowIcon(QtGui.QIcon("./icons/mouseicon.png"))
        self.setWindowTitle(self.title)
		#self.setGeometry(self.left, self.top, self.width, self.height)
		
		#Central Widget to add other widgets 
        self.centralwidget = QtWidgets.QWidget()
        self.centralwidget.setObjectName("CentralWidget")
		
		#We need to determine a layout for central widget
        self.CentralGridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.CentralGridLayout.setObjectName("CentralGridLayout")
		
		#Other layouts will be created and added to main vertical layout, which will then be added to central grid layout
        self.MainVerticalLayout = QtWidgets.QVBoxLayout()
        self.MainVerticalLayout.setObjectName("MainVerticalLayout")
		
		#We call our UI methods to fill our window
        self.DataInfoLabelUI()
		
        self.SensorOutputUI()
		
        self.ExteriorButtonsUI()
		
		#We add MainVerticalLayout into our CentralGridLayout
        self.CentralGridLayout.addLayout(self.MainVerticalLayout, 0, 0, 1, 1)
		
		#We set our central widget
        self.setCentralWidget(self.centralwidget)
		
        self.show()
		
    def DataInfoLabelUI(self):
        #Top items are created here
        
        #We create QHBoxLayout which holds top items of main window
        hboxDataInfo = QtWidgets.QHBoxLayout()
        
        #ExperimentLabel will stay at minimum size to make room for ExperimentLineEdit
        self.ExperimentLabel = QtWidgets.QLabel(self)
        self.ExperimentLabel.setGeometry(QtCore.QRect(10, 20, 169, 31))
        fontExpLabel = QtGui.QFont()
        fontExpLabel.setPointSize(15)
        fontExpLabel.setBold(True)
        fontExpLabel.setWeight(75)
        self.ExperimentLabel.setFont(fontExpLabel)
        self.ExperimentLabel.setFrameShape(QtWidgets.QFrame.NoFrame)
        self.ExperimentLabel.setFrameShadow(QtWidgets.QFrame.Raised)
        self.ExperimentLabel.setObjectName("ExperimentLabel")
        self.ExperimentLabel.setText("Deney Künyesi : ")
        hboxDataInfo.addWidget(self.ExperimentLabel)
        
        #ExperimentLineEdit will show experiment information entered by user
        self.ExperimentLineEdit = QtWidgets.QLineEdit(self)
        self.ExperimentLineEdit.setGeometry(QtCore.QRect(200, 28, 201, 21))
        sizeAdjust = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Maximum)
        sizeAdjust.setHorizontalStretch(0)
        sizeAdjust.setVerticalStretch(0)
        sizeAdjust.setHeightForWidth(self.ExperimentLineEdit.sizePolicy().hasHeightForWidth())
        self.ExperimentLineEdit.setSizePolicy(sizeAdjust)
        self.ExperimentLineEdit.setMinimumSize(QtCore.QSize(201, 0))
        self.ExperimentLineEdit.setReadOnly(True)
        self.ExperimentLineEdit.setObjectName("ExperimentLineEdit")
        self.ExperimentLineEdit.setPlaceholderText("*Lütfen ayarlardan deney künyesi girin*")
        self.ExperimentLineEdit.setText(' ')
        hboxDataInfo.addWidget(self.ExperimentLineEdit)
        
        self.shutdownButton = QtWidgets.QPushButton(self)
        self.shutdownButton.setText("")
        self.shutdownButton.setFixedSize(50, 24)
        self.shutdownButton.setObjectName("shutdownButton")
        self.shutdownButton.setIcon(QtGui.QIcon("./icons/shutdownicon.png"))
        self.shutdownButton.clicked.connect(self.shutDown)
        hboxDataInfo.addWidget(self.shutdownButton)   
        
        self.MainVerticalLayout.addLayout(hboxDataInfo)
		
    def SensorOutputUI(self):
		#Main output box is created here
		
		#We create QGroupBox to add data/sensor related items into
        groupBox = QtWidgets.QGroupBox(self.centralwidget)
        groupboxfont = QtGui.QFont()
        groupboxfont.setPointSize(10)
        groupBox.setFont(groupboxfont)
        groupBox.setInputMethodHints(QtCore.Qt.ImhNone)
        groupBox.setFlat(False)
        groupBox.setCheckable(False)
        groupBox.setObjectName("groupBox")
        groupBox.setTitle("Sensör Değerleri")
		
		#We set QGroupBox's layout to QGridLayout as there will be multiple items added horizontally and vertically
        gridLayout = QtWidgets.QGridLayout(groupBox)
        gridLayout.setSizeConstraint(QtWidgets.QLayout.SetDefaultConstraint)
        gridLayout.setObjectName("gridLayout")
		
		#-------------------------Labels---------------------------
        self.TemperatureLabel = QtWidgets.QLabel(groupBox)
        temperaturelabelfont = QtGui.QFont()
        temperaturelabelfont.setBold(False)
        temperaturelabelfont.setItalic(False)
        temperaturelabelfont.setUnderline(False)
        temperaturelabelfont.setWeight(50)
        temperaturelabelfont.setStrikeOut(False)
        self.TemperatureLabel.setFont(temperaturelabelfont)
        self.TemperatureLabel.setWordWrap(True)
        self.TemperatureLabel.setObjectName("TemperatureLabel")
        self.TemperatureLabel.setText("Sıcaklık : ")
        gridLayout.addWidget(self.TemperatureLabel, 0, 0, 1, 1)
		
        self.HumidityLabel = QtWidgets.QLabel(groupBox)
        self.HumidityLabel.setWordWrap(True)
        self.HumidityLabel.setObjectName("HumidityLabel")
        self.HumidityLabel.setText("Nem :")
        gridLayout.addWidget(self.HumidityLabel, 0, 3, 1, 1)
		
        self.O2Label = QtWidgets.QLabel(groupBox)
        self.O2Label.setObjectName("O2Label")
        self.O2Label.setText("O<sub>2</sub> : ")
        gridLayout.addWidget(self.O2Label, 1, 0, 1, 1)
		
        self.COLabel = QtWidgets.QLabel(groupBox)
        self.COLabel.setObjectName("COLabel")
        self.COLabel.setText("CO :")
        gridLayout.addWidget(self.COLabel, 2, 0, 1, 1)
		
        self.CO2Label = QtWidgets.QLabel(groupBox)
        self.CO2Label.setWordWrap(True)
        self.CO2Label.setObjectName("CO2Label")
        self.CO2Label.setText("CO<sub>2</sub> :")
        gridLayout.addWidget(self.CO2Label, 1, 3, 1, 1)
		#-------------------------Labels End---------------------------
		#======================LCD Monitors============================        
        self.TemperatureLCD = QtWidgets.QLCDNumber(groupBox)
        self.TemperatureLCD.setAutoFillBackground(True)
        self.TemperatureLCD.setFrameShadow(QtWidgets.QFrame.Plain)
        self.TemperatureLCD.setObjectName("TemperatureLCD")
        gridLayout.addWidget(self.TemperatureLCD, 0, 1, 1, 1)
        
        self.HumidityLCD = QtWidgets.QLCDNumber(groupBox)
        self.HumidityLCD.setAutoFillBackground(True)
        self.HumidityLCD.setFrameShadow(QtWidgets.QFrame.Plain)
        self.HumidityLCD.setObjectName("HumidityLCD")
        gridLayout.addWidget(self.HumidityLCD, 0, 4, 1, 1)
		
        self.O2LCD = QtWidgets.QLCDNumber(groupBox)
        self.O2LCD.setAutoFillBackground(True)
        self.O2LCD.setFrameShadow(QtWidgets.QFrame.Plain)
        self.O2LCD.setObjectName("O2LCD")
        gridLayout.addWidget(self.O2LCD, 1, 1, 1, 1)
        
        self.COLCD = QtWidgets.QLCDNumber(groupBox)
        self.COLCD.setAutoFillBackground(True)
        self.COLCD.setFrameShadow(QtWidgets.QFrame.Plain)
        self.COLCD.setObjectName("COLCD")
        gridLayout.addWidget(self.COLCD, 2, 1, 1, 1)
        
        self.CO2LCD = QtWidgets.QLCDNumber(groupBox)
        self.CO2LCD.setAutoFillBackground(True)
        self.CO2LCD.setFrameShadow(QtWidgets.QFrame.Plain)
        self.CO2LCD.setObjectName("CO2LCD")
        gridLayout.addWidget(self.CO2LCD, 1, 4, 1, 1)
		#======================LCD Monitors End============================
		#----------------------Graph Buttons---------------------------
        self.TemperatureButton = QtWidgets.QPushButton(groupBox)
        self.TemperatureButton.setText("")
        self.TemperatureButton.setFixedSize(50,24)
        self.TemperatureButton.setObjectName("TemperatureButton")
        self.TemperatureButton.setIcon(QtGui.QIcon("./icons/charticon.png"))
        self.TemperatureButton.clicked.connect(self.CallTemperatureGraph)
        gridLayout.addWidget(self.TemperatureButton, 0, 2, 1, 1)
		
        self.HumidityButton = QtWidgets.QPushButton(groupBox)
        self.HumidityButton.setText("")
        self.HumidityButton.setFixedSize(50,24)
        self.HumidityButton.setObjectName("HumidityButton")
        self.HumidityButton.setIcon(QtGui.QIcon("./icons/charticon.png"))
        self.HumidityButton.clicked.connect(self.CallHumidityGraph)
        gridLayout.addWidget(self.HumidityButton, 0, 5, 1, 1)
		
        self.O2Button = QtWidgets.QPushButton(groupBox)
        self.O2Button.setText("")
        self.O2Button.setFixedSize(50,24)
        self.O2Button.setObjectName("O2Button")
        self.O2Button.setIcon(QtGui.QIcon("./icons/charticon.png"))
        self.O2Button.clicked.connect(self.CallOxyGraph)
        gridLayout.addWidget(self.O2Button, 1, 2, 1, 1)
		
        self.COButton = QtWidgets.QPushButton(groupBox)
        self.COButton.setText("")
        self.COButton.setFixedSize(50,24)
        self.COButton.setObjectName("COButton")
        self.COButton.setIcon(QtGui.QIcon("./icons/charticon.png"))
        self.COButton.clicked.connect(self.CallCOGraph)
        gridLayout.addWidget(self.COButton, 2, 2, 1, 1)

        self.CO2Button = QtWidgets.QPushButton(groupBox)
        self.CO2Button.setText("")
        self.CO2Button.setFixedSize(50, 24)
        self.CO2Button.setObjectName("CO2Button")
        self.CO2Button.setIcon(QtGui.QIcon("./icons/charticon.png"))
        self.CO2Button.clicked.connect(self.CallCO2Graph)
        gridLayout.addWidget(self.CO2Button, 1, 5, 1, 1)
		#----------------------Graph Buttons End---------------------------
		#======================Control Buttons============================
        self.startExpButton = QtWidgets.QPushButton(groupBox)
        self.startExpButton.setText("Deneyi Başlat")
        self.startExpButton.setFixedSize(150, 24)
        self.startExpButton.setObjectName("startExpButton")
        self.startExpButton.setIcon(QtGui.QIcon("./icons/starticon.png"))
        self.startExpButton.clicked.connect(self.startStopExp)
        gridLayout.addWidget(self.startExpButton, 0, 7, 1, 1)
        
        self.airEvacButton = QtWidgets.QPushButton(groupBox)
        self.airEvacButton.setText("Hava Tahliyesi")
        self.airEvacButton.setFixedSize(150, 24)
        self.airEvacButton.setObjectName("airEvacButton")
        #self.airEvacButton.setIcon(QtGui.QIcon("./icons/charticon.png"))
        self.airEvacButton.clicked.connect(self.airEvac)
        gridLayout.addWidget(self.airEvacButton, 1, 7, 1, 1)
        
        self.ejectHolderButton = QtWidgets.QPushButton(groupBox)
        self.ejectHolderButton.setText("Holder'ı çıkart")
        self.ejectHolderButton.setFixedSize(150, 24)
        self.ejectHolderButton.setObjectName("ejectHolderButton")
        #self.ejectHolderButton.setIcon(QtGui.QIcon("./icons/charticon.png"))
        self.ejectHolderButton.clicked.connect(self.ejectHolder)
        gridLayout.addWidget(self.ejectHolderButton, 2, 7, 1, 1)
		#======================Control Buttons End============================
		#----------------------Spacers#----------------------
        spacerOfHumidity = QtWidgets.QSpacerItem(232, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        gridLayout.addItem(spacerOfHumidity, 0, 6, 1, 1)
		
        spacerOfPressure = QtWidgets.QSpacerItem(232, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        gridLayout.addItem(spacerOfPressure, 1, 6, 1, 1)
		
        spacerOfCO = QtWidgets.QSpacerItem(232, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        gridLayout.addItem(spacerOfCO, 2, 6, 1, 1)
		#----------------------Spacers End#----------------------
		
        self.MainVerticalLayout.addWidget(groupBox)
		
    def ExteriorButtonsUI(self):
		#Bottom items are created here
        hboxExteriorButtons = QtWidgets.QHBoxLayout()
        hboxExteriorButtons.setObjectName("horizontalLayout")
		
        self.startSmokingButton = QtWidgets.QPushButton(self.centralwidget)
        self.startSmokingButton.setText("Sigara Yak")
        self.startSmokingButton.setFixedSize(150, 24)
        self.startSmokingButton.setObjectName("startSmokingButton")
        self.startSmokingButton.setIcon(QtGui.QIcon("./icons/litcigaretteicon.png"))
        self.startSmokingButton.clicked.connect(self.startStopSmoking)
        hboxExteriorButtons.addWidget(self.startSmokingButton)
        
        self.stopSmokingButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopSmokingButton.setText("Sigara Söndür")
        self.stopSmokingButton.setFixedSize(150, 24)
        self.stopSmokingButton.setObjectName("stopSmokingButton")
        self.stopSmokingButton.setIcon(QtGui.QIcon("./icons/extinguishedcigaretteicon.png"))
        self.stopSmokingButton.clicked.connect(self.startStopSmoking)
        hboxExteriorButtons.addWidget(self.stopSmokingButton)
        """
        self.stopAllButton = QtWidgets.QPushButton(self.centralwidget)
        self.stopAllButton.setText("Sistemi Durdur")
        self.stopAllButton.setFixedSize(150, 24)
        self.stopAllButton.setObjectName("stopAllButton")
        self.stopAllButton.setIcon(QtGui.QIcon("./icons/terminateicon.png"))
        self.stopAllButton.clicked.connect(self.startStopSmoking)
        hboxExteriorButtons.addWidget(self.stopAllButton)
        """
        spacerItem = QtWidgets.QSpacerItem(278, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        hboxExteriorButtons.addItem(spacerItem)
		
        self.SaveDataButton = QtWidgets.QPushButton(self.centralwidget)
        self.SaveDataButton.setObjectName("SaveDataButton")
        self.SaveDataButton.setText("Verileri Kaydet")
        self.SaveDataButton.clicked.connect(self.SaveData)
        hboxExteriorButtons.addWidget(self.SaveDataButton)
		
        self.SettingsButton = QtWidgets.QPushButton(self.centralwidget)
        self.SettingsButton.setObjectName("SettingsButton")
        self.SettingsButton.setText("Ayarlar")
        self.SettingsButton.clicked.connect(self.CallSettings)
        hboxExteriorButtons.addWidget(self.SettingsButton)
		
        self.MainVerticalLayout.addLayout(hboxExteriorButtons)
        
    def startStopSmoking(self):
        sender = self.sender()
        
        try:
            if sender.text() == 'Sigara Yak':
                self.ser.write(b'r \n')
            elif sender.text() == 'Sigara Söndür':
                self.ser.write(b'p \n')
            #elif sender.text() == 'Sistemi Durdur':
            #    self.ser.write(b'a \n')
        except:
            QtWidgets.QMessageBox.about(self, "Dikkat", 'Bağlı arduino bulunamadı. Lütfen sistemi kontrol ediniz.')
        
    def ejectHolder(self):
        try:
            self.ser.write(b'j \n')
        except:
            QtWidgets.QMessageBox.about(self, "Dikkat", 'Bağlı arduino bulunamadı. Lütfen sistemi kontrol ediniz.')
        
    def openArduinoPort(self):
        try:
            self.ser = serial.Serial()
            self.ser.baudrate = 9600
            self.ser.port = '/dev/ttyUSB0'
            self.ser.open()
        except:
            pass
        
    def readFromArduino(self):
        try:
            if self.ser.in_waiting != 0:
                sensorData = self.ser.readline().decode('ascii')[:-2].split('/')
                for i in range(0, len(sensorData)): 
                    sensorData[i] = float(sensorData[i])
                
                self.TemperatureValues.append(sensorData[0])
                self.TemperatureLCD.display(sensorData[0])
                
                self.OxyValues.append(sensorData[1])
                self.O2LCD.display(sensorData[1])
                
                self.COValues.append(sensorData[2])
                self.COLCD.display(sensorData[2])
                
                self.HumidityValues.append(sensorData[3])
                self.HumidityLCD.display(sensorData[3])
                
                self.CO2Values.append(sensorData[4])
                self.CO2LCD.display(sensorData[4])
            else:
                pass
        except:
            pass
        
    def createDeneylerFolder(self):
        if os.path.isdir('/home/pi/Desktop/Deneyler'):
            pass
        else:
            os.mkdir('/home/pi/Desktop/Deneyler')
        
    def startStopExp(self):
        sender1 = self.sender()
        if sender1.text() == 'Deneyi Başlat':
            if self.ser.isOpen() == True and os.path.isdir('/home/pi/Desktop/Deneyler' + self.ExperimentLineEdit.text()) == False:
                try:
                    self.ser.write(b'd \n')
                    
                    try:
                        self.workPath = '/home/pi/Desktop/Deneyler/' + self.ExperimentLineEdit.text()
                        os.mkdir(self.workPath)
                        
                        self.TemperatureValues = []
                        self.OxyValues = []
                        self.COValues = []
                        self.HumidityValues = []
                        self.CO2Values = []
                        
                        self.startExpButton.setText('Deneyi Bitir')
                        self.startExpButton.setIcon(QtGui.QIcon("./icons/terminateicon.png"))
                        
                    except FileExistsError:
                        QtWidgets.QMessageBox.about(self, "Dikkat", 'Yeni bir çalışma alanı yapın.')
                        
                except:
                    QtWidgets.QMessageBox.about(self, "Dikkat", 'Bağlı arduino bulunamadı. Lütfen sistemi kontrol ediniz.')
                    
            elif os.path.isdir('/home/pi/Desktop/Deneyler' + self.ExperimentLineEdit.text()) == True:
                QtWidgets.QMessageBox.about(self, "Dikkat", 'Yeni bir çalışma alanı yapın.')
                
            elif self.ser.isOpen() == False:
                QtWidgets.QMessageBox.about(self, "Dikkat", 'Bağlı arduino bulunamadı. Lütfen sistemi kontrol ediniz.')
                
        elif sender1.text() == 'Deneyi Bitir':
            self.workPath = ''
            try:
                self.ser.write(b'a \n')
                
                self.AutoSave()
                
                self.startExpButton.setText('Deneyi Başlat')
                self.startExpButton.setIcon(QtGui.QIcon("./icons/starticon.png"))
            except:
                QtWidgets.QMessageBox.about(self, "Dikkat", 'Bağlı arduino bulunamadı. Lütfen sistemi kontrol ediniz.')
        
    def airEvac(self):
        try:
            self.ser.write(b'z \n')
        except:
            QtWidgets.QMessageBox.about(self, "Dikkat", 'Bağlı arduino bulunamadı. Lütfen sistemi kontrol ediniz.')
        """
        #selectionSignal created in airEvacuation.py is connected to a method here
        #That method receives data and performs the given action
        self.airEvacwindow = modules.airEvacuation.airEvacWindow()
        self.airEvacwindow.selectionSignal.connect(self.receiveAirEvacSignal)
        self.airEvacwindow.show()
        
    def receiveAirEvacSignal(self, whichCabin):
        #whichCabin variable receives emitted signal from selectionSignal inside airEvacwindow
        #signal is emitted with the specific name of the cabin or as 'both'
        try:
            if whichCabin == 'both':
                self.ser.write(b'x \n')
                self.ser.write(b'z \n')
            elif whichCabin == 'mouseCabin':
                self.ser.write(b'z \n')
            elif whichCabin == 'cigaretteCabin':
                self.ser.write(b'x \n')
        except:
            pass
        """ #Only one cabin is left to be evacuated
    def CallTemperatureGraph(self):
        modules.CreateGraph.CreateTemperatureGraph(self.TemperatureValues)
		
    def CallOxyGraph(self):
        modules.CreateGraph.CreateOxyGraph(self.OxyValues)

    def CallCOGraph(self):
        modules.CreateGraph.CreateCOGraph(self.COValues)

    def CallHumidityGraph(self):
        modules.CreateGraph.CreateHumidityGraph(self.HumidityValues)

    def CallCO2Graph(self):
        modules.CreateGraph.CreateCO2Graph(self.CO2Values)

    def CallSettings(self):
		#As settings window, we create QDialog window contained inside settings.py
        self.settingswindow = modules.settings.SettingsWindow()
        self.settingswindow.cigaretteTypeSignal.connect(self.receiveTypeSignal)
        self.settingswindow.resetHolderSignal.connect(self.resetHolderPosition)
        self.settingswindow.ExpTimeSignal.connect(self.ExpTimeSignalReceiver)
        self.settingswindow.HowManyCigarettes.connect(self.HowManyCigs)
        self.settingswindow.showFullScreen()
        
    def HowManyCigs(self, number):
        try:
            self.ser.write(b''.join('y' + str(number) + '\n'))
        except:
            pass
        
    def ExpTimeSignalReceiver(self, time):
        try:
            self.ser.write(b''.join('h' + str(time) + '\n'))
        except:
            pass
        
    def resetHolderPosition(self, go):
        if go == 'reset':
            try:
                self.ser.write(b'f \n')
            except:
                pass
        
    def receiveTypeSignal(self, cigaretteType):
        try:
            if cigaretteType == 'iqos':
                self.ser.write(b'q \n')
            elif cigaretteType == 'normal':
                self.ser.write(b'c \n')
        except:
            pass
		
    def SaveData(self):
        """virtualKeyboard = QtGui.QInputMethod()
        virtualKeyboard.setVisible(True)"""
        name = QtWidgets.QInputDialog.getText(self, 'Kayıt ismi', 'Kaydedilecek dosya için isim girin.', QtWidgets.QLineEdit.Normal, "")
        temp_savePath = QtWidgets.QFileDialog.getExistingDirectory(self, 'Kaydetmek istediğiniz yeri seçin', '/home')
        save_path = temp_savePath + '/' + str(name[0])
        modules.SaveData.SaveasCSV(self.ExperimentLineEdit.text(), self.TemperatureValues, self.HumidityValues, self.OxyValues, self.COValues, self.CO2Values, save_path)
		
    def FindExperimentName(self):
        try :
            with open("settings.json", "r") as Settings_File:
                user_settings = json.load(Settings_File)
                self.ExperimentLineEdit.setText(user_settings['Experiment_Name'] + ' - ' + user_settings['Cigarette_Type'])
        except FileNotFoundError :
            pass
		
    def AutoSave(self):
        try:
            fieldnames = ['Sicaklik', 'Nem', 'Oksijen Yüzdesi', 'Karbonmonoksit Yüzdesi', 'Karbondioksit Yüzdesi']
            with open (self.workPath + '/Auto Save.csv', 'w', newline='') as myfile:
                wr = csv.writer(myfile)
                wr.writerow(fieldnames)
                for i in range(0, len(self.OxyValues)):
                    temporaryValuesList = [self.TemperatureValues[i], self.HumidityValues[i], self.OxyValues[i], self.COValues[i], self.CO2Values[i]]
                    wr.writerow(temporaryValuesList)
        except:
            pass
		
    def shutDown(self):
        buttonReply = QtWidgets.QMessageBox.question(self, 'Sistem kapama komutu verildi.', "Sistemin kapanmasını istediğinize emin misiniz?", QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No, QtWidgets.QMessageBox.No)
        if buttonReply == QtWidgets.QMessageBox.Yes:
            try:
                self.ser.write(b'e \n')
            except:
                pass
            self.AutoSave()
            self.close()
        else:
            pass
        
#os.environ["QT_IM_MODULE"] = "qtvirtualkeyboard"
App = QtWidgets.QApplication(sys.argv)
window = Window()
window.showFullScreen()
sys.exit(App.exec())
