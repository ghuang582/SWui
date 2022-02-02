import sys
from PyQt5.QtWidgets import QMainWindow, QApplication
from PyQt5 import uic

import RecordScreen
import BoxDetection
import OCR
import RuneEfficiency

Ui_MainWindow, QtBaseClass = uic.loadUiType("app\dependencies\SWtemplate_v3.ui")

class MyApp(QMainWindow):
    def __init__(self):
        super(MyApp, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        self.ui.CallUpdate.clicked.connect(self.callUpdate)

    def updateRune(self, rune = [], efficiency = []):
        if rune[1] == []:
            print('err1')
            print(rune)
            self.ui.MainStat.setText("hi")
        else:
            print('state2')
            print(rune)
            MainStat = ' '.join(map(str, rune[1][0]))
            self.ui.MainStat.setText(MainStat)

            hasInnate = rune[0][2]

            if hasInnate == 1:
                Innate = ' '.join(map(str, rune[1][1]))
                self.ui.Innate.setText(Innate)
            else:
                self.ui.Innate.setText(" - ")
                
            print('err2')

            Slot1 = ' '.join(map(str, rune[1][1 + hasInnate]))
            self.ui.Slot1.setText(Slot1)

            Slot2 = ' '.join(map(str, rune[1][2 + hasInnate]))
            self.ui.Slot2.setText(Slot2)

            Slot3 = ' '.join(map(str, rune[1][3 + hasInnate]))
            self.ui.Slot3.setText(Slot3)

            Slot4 = ' '.join(map(str, rune[1][4 + hasInnate]))
            self.ui.Slot4.setText(Slot4)          
            print('err3')
            self.ui.Rarity.setText(rune[0][1])
            self.ui.CurrEff.setText("{0:.2%}".format(efficiency[0]))
            self.ui.MaxEff.setText("{0:.2%}".format(efficiency[1]))      
    
    def callUpdate(self):
        print("update")

        # snapshot = RecordScreen.screenGrab()
        snapshot = RecordScreen.screenshot('NoxPlayer2')
        # if snapshot:
        #     snapshot.show()
        cropped = BoxDetection.crop_boxes(snapshot)
        print('mid')
        # Exit update call if cropped did not get find any boxes to OCR
        if cropped == []:
            return
        print('test')
        rune = OCR.do_ocr(cropped[0])
        eff = RuneEfficiency.CalcEff(rune)
        
        print('call')
        
        self.updateRune(rune, eff)

def run():        
    app = QApplication(sys.argv)
    window = MyApp()
    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    run()