import sys
# Импортируем наш интерфейс из файла
from automarryUI import *
from PyQt5 import QtCore, QtGui, QtWidgets
# from analog_plot import AnalogPlot
from time import sleep
import serial
from serial_test import serial_ports
import threading
from PyQt5.QtCore import QTimer ,QThreadPool
import time


def threaded(fn):
    def wrapper(*args, **kwargs):
        thread = threading.Thread(target=fn, args=args, kwargs=kwargs)
        thread.start()
        return thread

    return wrapper

class MyWin(QtWidgets.QMainWindow):

    def __init__(self, parent=None):
        QtWidgets.QWidget.__init__(self, parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.upTimer = QTimer()

        # # Здесь прописываем событие нажатия на кнопку
        self.ui.REFRESHpushButton.clicked.connect(self.Refresh)
        self.ui.CONNECTpushButton.clicked.connect(self.Connect)
        self.ui.TESTpushButton.clicked.connect(self.Test)
        self.ui.PH_PLUScheckBox.stateChanged.connect(self.PHPpump)
        self.ui.PH_MINUScheckBox.stateChanged.connect(self.PHMpump)
        self.ui.FERT_WTRcheckBox.stateChanged.connect(self.FERTpump)
        self.ui.CLR_WTRcheckBox.stateChanged.connect(self.CLEARpump)

        self.upTimer.timeout.connect(self.Update)
        self.ph = ''
        self.hum= ''
        self.lvB= ''
        self.lvT= ''
        self.tank= ''
        self.time= ''
        self.period= ''

        self.pre_delay= ''
        self.lvlH= ''
        self.lvlL= ''
        self.ph_min= ''
        self.ph_max= ''
        self.ph_plus_doze= ''
        self.ph_minus_doze= ''
        self.fert_doze= ''
        self.subst_hum= ''
        self.ph_delay= ''




        

    def Refresh(self):

        self.ui.PORTlistWidget.clear()

        com_list = serial_ports()

        for key in com_list:
            self.ui.PORTlistWidget.addItem(key)

    def Connect(self):
        if(len(self.ui.RATElistWidget.selectedItems()) > 0):
            port = self.ui.PORTlistWidget.selectedItems()[0].text()
            rate = self.ui.RATElistWidget.selectedItems()[0].text()
            try:

                self.ser = serial.Serial(port, rate)
                print('connected')


                self.SerialRead()
                self.upTimer.start(2000)

            except Exception as e:
                print (e)
                print ('connection exeption')

    @threaded
    def SerialRead(self):
        while True:
            if self.ser.inWaiting():
                msg=str(self.ser.readline())
                msg = msg.replace("b'", '')
                msg = msg.replace("\\r\\n", '')
                msg = msg.replace("'", '')
                msg = msg.split(':')
                if msg[0] == 'ph':
                    self.ph=msg[1]
                if msg[0] == 'hum':
                    self.hum = msg[1]
                if msg[0] == 'lvl_l':
                    self.lvB=msg[1]
                if msg[0] == 'lvl_h':
                    self.lvT =msg[1]
                if msg[0] == 'tank':
                    self.tank=msg[1]
                if msg[0] == 'time':
                    self.time = msg[1]
                if msg[0] == 'period':
                    self.period = msg[1]

                if msg[0] == 'pre_delay':
                    self.pre_delay=msg[1]
                if msg[0] == 'lvl_hTR':
                    self.lvlH = msg[1]
                if msg[0] == 'lvl_lTR':
                    self.lvlL=msg[1]
                if msg[0] == 'phMax':
                    self.ph_max =msg[1]
                if msg[0] == 'phMin':
                    self.ph_min=msg[1]
                if msg[0] == 'ph_plus_doze':
                    self.ph_plus_doze = msg[1]
                if msg[0] == 'ph_minus_doze':
                    self.ph_minus_doze = msg[1]

                if msg[0] == 'fertilizer_doze':
                    self.fert_doze = msg[1]
                if msg[0] == 'ph_delay':
                    self.ph_delay = msg[1]
                if msg[0] == 'substrat_hum':
                    self.subst_hum = msg[1]




    def Update(self):
            self.ser.write('com:9\n'.encode('utf-8'))
            # print("get data")
            self.ui.PHtextBrowser.setText(self.ph)
            self.ui.SUBSTRATtextBrowser.setText(self.hum)
            self.ui.LEVEL_BOTtextBrowser.setText(self.lvB)
            self.ui.LEVEL_TOPtextBrowser.setText(self.lvT)
            self.ui.TANK_STATEtextBrowser.setText(self.tank)
            self.ui.TIMEtextBrowser.setText(self.time)
            self.ui.PERIODtextBrowser.setText(self.period)

            self.ui.PRE_DELAYlabel.setText(self.pre_delay)
            self.ui.LVL_Hlabel.setText(self.lvlH)
            self.ui.LVL_Llabel.setText(self.lvlL)
            self.ui.PH_MAXlabel.setText(self.ph_max)
            self.ui.PH_MINlabel.setText(self.ph_min)
            self.ui.PH_PLUS_DOZElabel.setText(self.ph_plus_doze)
            self.ui.PH_MINUS_DOZElabel.setText(self.ph_minus_doze)
            self.ui.FERT_DOZElabel.setText(self.fert_doze)
            self.ui.SUBST_HUMlabel.setText(self.subst_hum)
            self.ui.PH_DELAYlabel.setText(self.ph_delay)

    def Test(self):
        self.ser.write('\n'.encode('utf-8'))
        print("get data")

    def PHPpump(self):
        if self.ui.PH_PLUScheckBox.isChecked():
            self.ser.write('com:1\n'.encode('utf-8'))
        else:
            self.ser.write('com:2\n'.encode('utf-8'))
    def PHMpump(self):
        if self.ui.PH_MINUScheckBox.isChecked():
            self.ser.write('com:3\n'.encode('utf-8'))
        else:
            self.ser.write('com:4\n'.encode('utf-8'))

    def FERTpump(self):
        if self.ui.FERT_WTRcheckBox.isChecked():
            self.ser.write('com:5\n'.encode('utf-8'))
        else:
            self.ser.write('com:6\n'.encode('utf-8'))
    def CLEARpump(self):
        if self.ui.CLR_WTRcheckBox.isChecked():
            self.ser.write('com:7\n'.encode('utf-8'))
        else:
            self.ser.write('com:8\n'.encode('utf-8'))


            
            

if __name__=="__main__":
    app = QtWidgets.QApplication(sys.argv)
    myapp = MyWin()
    myapp.show()
    sys.exit(app.exec_())