from QuestionsTextuelles import *

class QuestionsTextuellesImp(Ui_Dialog):
    def __init__(self):
        super().__init__()
    def setupUi(self, Dialog):
        super().setupUi(Dialog)
        Dialog.setWindowTitle("Questions Textuelles")
    def setData(self,data):
        self.tableWidget.setRowCount(len(data))
        self.tableWidget.setColumnCount(len(data[0]))
        self.tableWidget.setHorizontalHeaderLabels(data[0])
        for i in range(len(data)):
            for j in range(len(data[i])):
                self.tableWidget.setItem(i,j, QtWidgets.QTableWidgetItem(data[i][j]))
