from ParticipantImp import ParticipantImp
from ChercheurImp import ChercheurImp
from R_connexion import setupR
from Choix import *

class ChoixImp(Ui_MainWindow):
    def __init__(self):
        super().__init__()
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.w=MainWindow
        MainWindow.setWindowTitle("Choufli-PSY")
        MainWindow.setWindowIcon(QtGui.QIcon("icon.png"))
        self.pushButton.clicked.connect(self.echange)
    def echange(self):
        x=self.comboBox.currentIndex()
        self.Window = QtWidgets.QMainWindow()
        if(x==1):
            self.ui = ParticipantImp()
        else:
            self.ui = ChercheurImp()
        self.ui.setupUi(self.Window)
        self.Window.show()
        self.w.close()

if __name__ == "__main__":
    import sys
    setupR()
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = ChoixImp()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())
