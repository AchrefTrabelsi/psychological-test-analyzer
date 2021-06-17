from PyQt5.QtCore import Qt
from Chercheur import *
from re import findall
import csv
from R_connexion import setupR
from Dataset import Dataset
from pathlib import Path
from QuestionsTextuellesImp import QuestionsTextuellesImp
import sys

class ChercheurImp(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.checkboxs = []
        self.dataset=None
        self.dataset_secondaire=None 
        self.pointeur_question=0
        Path("ic").mkdir(parents=True, exist_ok=True)
        Path("icc").mkdir(parents=True, exist_ok=True)
        Path("tendance").mkdir(parents=True, exist_ok=True)
        Path("temp").mkdir(parents=True, exist_ok=True)



    def setupUi(self, MainWindow):
        self.mainWindow=MainWindow
        MainWindow.setWindowIcon(QtGui.QIcon("icon.png"))
        super().setupUi(MainWindow)
        MainWindow.setWindowTitle("Chercheur")
        self.pushButton_4.clicked.connect(self.ajouter_Question_Demographique)
        self.pushButton_13.clicked.connect(self.supprimer_Question_Demographique)
        self.pushButton.clicked.connect(self.ajouter_Question_Textuelle)
        self.pushButton_8.clicked.connect(self.supprimer_Question_Textuelle)
        self.pushButton_7.clicked.connect(self.parcourir)
        self.pushButton_2.clicked.connect(self.pre_filtre)
        self.pushButton_3.clicked.connect(self.filtre)
        self.pushButton_5.clicked.connect(self.previous)
        self.pushButton_6.clicked.connect(self.next)
        self.pushButton_9.clicked.connect(self.parcourir_secondaire)
        self.pushButton_10.clicked.connect(self.correlation)
        self.pushButton_11.clicked.connect(self.analyser)
        self.pushButton_16.clicked.connect(self.analyseTextuelle)
        self.pushButton_12.clicked.connect(lambda: self.selectionnerTout(True))
        self.pushButton_14.clicked.connect(lambda: self.selectionnerTout(False))
        self.pushButton_15.clicked.connect(self.save)
        
    def pre_filtre(self) :
        questions_d=[]
        self.clearLayout(self.verticalLayout_2)
        for x in range(self.list_Questions_Demographiques.count()):
            questions_d.append(int(self.list_Questions_Demographiques.item(x).text())-1)
        self.dataset.setQuestions_d(questions_d)
        self.checkboxs=[]
        for i in range(len(self.dataset.questions_d)) :
            horizontalLayout_4 = QtWidgets.QHBoxLayout()
            horizontalLayout_4.setObjectName(str(self.dataset.questions_d[i]))
            label = QtWidgets.QLabel(self.scrollAreaWidgetContents)
            label.setObjectName("label"+str(self.dataset.questions_d[i]))
            horizontalLayout_4.addWidget(label)
            label.setText(str(self.dataset.header_questions_d[i]))
            self.verticalLayout_2.addLayout(horizontalLayout_4)
            option=[]
            for j in range(len(self.dataset.options_d[i])):
                checkBox = QtWidgets.QCheckBox(self.scrollAreaWidgetContents)
                checkBox.setObjectName(str(self.dataset.questions_d[i])+str(self.dataset.options_d[i][j]))
                checkBox.setText(str(self.dataset.options_d[i][j]))
                horizontalLayout_4.addWidget(checkBox)
                option.append(checkBox)
            spacerItem6 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
            horizontalLayout_4.addItem(spacerItem6)
            self.checkboxs.append(option)
        spacerItem6 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem6)
        self.activerdemarrer()
        
    def ajouter_Question_Demographique(self) :
        question=findall('\d+',self.Question_demographique.text())
        l=[]
        if not question:
            return
        for num in question:
            if int(num)==0:
                continue
            if int(num)>self.dataset.nbquestion:
                l.append(num)
                continue
            unique=True
            for x in range(self.list_Questions_Demographiques.count()):
                if self.list_Questions_Demographiques.item(x).text()==num:
                    unique=False
                    break
            if unique==False:
                continue
            self.list_Questions_Demographiques.addItem(num) 
        if len(l)>0:
            m=l[0]
            for i in range(1,len(l)):
                m+=","+l[i]
            msg = QtWidgets.QMessageBox(self.mainWindow)
            msg.setWindowIcon(QtGui.QIcon("icon.png"))
            if len(l)==1:
                msg.setText("La question "+m+" n'existe pas")
            else:
                msg.setText("Les questions "+m+" n'existent pas")
            msg.setWindowTitle("Erreur")
            msg.exec_()


    
    def supprimer_Question_Demographique(self) :
        items=self.list_Questions_Demographiques.selectedItems()
        for item in items:
            self.list_Questions_Demographiques.takeItem(self.list_Questions_Demographiques.row(item))
    
    def ajouter_Question_Textuelle(self) :
        question=findall('\d+',self.lineEdit.text())
        if not question:
            return
        l=[]
        for num in question:
            if int(num)==0:
                continue
            if int(num)>self.dataset.nbquestion :
                l.append(num)
                continue
            n=int(num)-1
            if n in self.dataset.questions_d:
                continue
            unique=True
            for x in range(self.list_Questions_Textuelles.count()):
                if self.list_Questions_Textuelles.item(x).text()==num:
                    unique=False
                    break
            if unique==False:
                continue
            self.list_Questions_Textuelles.addItem(num) 
        if len(l)>0:
            m=l[0]
            for i in range(1,len(l)):
                m+=","+l[i]
            msg = QtWidgets.QMessageBox(self.mainWindow)
            msg.setWindowIcon(QtGui.QIcon("icon.png"))
            if len(l)==1:
                msg.setText("La question "+m+" n'existe pas")
            else:
                msg.setText("Les questions "+m+" n'existent pas")
            msg.setWindowTitle("Erreur")
            msg.exec_()
   
    
    def supprimer_Question_Textuelle(self) :
        items=self.list_Questions_Textuelles.selectedItems()
        for item in items:
            self.list_Questions_Textuelles.takeItem(self.list_Questions_Textuelles.row(item))

    def parcourir(self):
        filebrowser = QtWidgets.QFileDialog(self.mainWindow)
        filebrowser.setModal(True)
        filebrowser.show()
        if filebrowser.exec_():
            path = filebrowser.selectedFiles()
        else:
            return
        path=path[0]
        self.dataset= Dataset(path)
        self.label_3.setText(self.dataset.name)
        self.label_4.setText(self.dataset.name)
        self.activerparcourir()

    def draw(self,label,image_path):
        img = QtGui.QPixmap.fromImage(QtGui.QImage(image_path))
        label.setPixmap(img)

    def filtre(self):
        questions_t=[]
        for x in range(self.list_Questions_Textuelles.count()):
            questions_t.append(int(self.list_Questions_Textuelles.item(x).text())-1)
        self.dataset.setQuestions_t(questions_t)
        checked_options=[]
        for i in range(len(self.checkboxs)):
            checked=[]
            for j in range(len(self.checkboxs[i])):
                if(self.checkboxs[i][j].isChecked()):
                    checked.append(self.dataset.options_d[i][j])
            checked_options.append(checked)
        valide=True
        if len(questions_t)>0:
            valide =self.confirmer()
        if valide==False:
            return
        print("filtre")
        self.statusbar.showMessage("filtration des données et analyse des données textuelles")
        self.dataset.filtre(checked_options)
        self.statusbar.clearMessage()
        msg = QtWidgets.QMessageBox(self.mainWindow)
        msg.setWindowIcon(QtGui.QIcon("icon.png"))
        msg.setText("Dataset filtrée et données textuelles analysées avec succès")
        msg.setWindowTitle("Succées")
        msg.exec_()
        self.pushButton_16.setEnabled(True)

    def confirmer(self):
        textdata=[]
        textdata.append(self.dataset.header_questions_t)
        for i in range(1,6): #changer 6 par len(self.dataset.dataset) pour afficher tout
            txtlist=[]
            for j in self.dataset.questions_t:
                txtlist.append(self.dataset.dataset[i][j])
            textdata.append(txtlist)
        ui = QuestionsTextuellesImp()
        Dialog = QtWidgets.QDialog()
        ui.setupUi(Dialog)
        ui.setData(textdata)
        if Dialog.exec():
            return True
        else:
            return False



    def analyser(self):
        self.statusbar.showMessage("Analyse du dataset")
        if self.dataset.GRM()==False:
            msg = QtWidgets.QMessageBox(self.mainWindow)
            msg.setIcon(QtWidgets.QMessageBox.Critical)
            msg.setText("Erreur lors de l'application de la méthode grm au dataset")
            msg.setWindowTitle("Erreur")
            msg.exec_()
            self.statusbar.clearMessage()
            return
        self.dataset.analyserQuestionnaire()
        self.draw(self.canvas,"ic/IC0")
        self.draw(self.canvas_3,"icc/ICC0")
        self.label_2.setText(self.dataset.header_questions_non_d[0])
        self.pointeur_question=0
        self.draw(self.canvas_2,"ic/IC")
        self.pushButton_5.setEnabled(True)
        self.pushButton_6.setEnabled(True)
        self.statusbar.clearMessage()


    def next(self):
        if(self.dataset==None):
            return
        self.pointeur_question=(self.pointeur_question+1)%len(self.dataset.header_questions_non_d)
        self.label_2.setText(self.dataset.header_questions_non_d[self.pointeur_question])
        self.draw(self.canvas,"ic/IC"+str(self.pointeur_question))
        self.draw(self.canvas_3,"icc/ICC"+str(self.pointeur_question))

    def previous(self):
        if(self.dataset==None):
            return
        self.pointeur_question=(self.pointeur_question-1+len(self.dataset.header_questions_non_d))%len(self.dataset.header_questions_non_d)
        self.label_2.setText(self.dataset.header_questions_non_d[self.pointeur_question])
        self.draw(self.canvas,"ic/IC"+str(self.pointeur_question))
        self.draw(self.canvas_3,"icc/ICC"+str(self.pointeur_question))

    def parcourir_secondaire(self):
        filebrowser = QtWidgets.QFileDialog(self.mainWindow)
        filebrowser.setModal(True)
        filebrowser.show()
        if filebrowser.exec_():
            path = filebrowser.selectedFiles()
        else:
            return
        path=path[0]
        self.dataset_secondaire= Dataset(path)
        self.label_5.setText(self.dataset_secondaire.name)
        self.label.setText(self.dataset_secondaire.name)

    def correlation(self):
        if self.dataset!=None:
            self.statusbar.showMessage("Analyse du premier dataset")
            if self.dataset.GRM()==False:
                msg = QtWidgets.QMessageBox(self.mainWindow)
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Erreur lors de l'application de la méthode  grm au dataset")
                msg.setWindowTitle("Erreur")
                msg.exec_()
                self.statusbar.clearMessage()
                return
            self.statusbar.showMessage("Analyse des tendances du premier dataset")
            self.dataset.tendance("1")
            self.draw(self.canvas_4,"tendance/11")
            self.draw(self.canvas_6,"tendance/12")
            self.statusbar.clearMessage()

        if self.dataset_secondaire!=None:
            self.statusbar.showMessage("Analyse du second dataset")
            if self.dataset_secondaire.GRM()==False:
                msg = QtWidgets.QMessageBox(self.mainWindow)
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Erreur lors de l'application de la méthode grm au second dataset")
                msg.setWindowTitle("Erreur")
                msg.exec_()
                self.statusbar.clearMessage()
                return
            self.statusbar.showMessage("Analyse des tendances du second dataset")
            self.dataset_secondaire.tendance("2")
            self.draw(self.canvas_7,"tendance/21")
            self.draw(self.canvas_5,"tendance/22")
            self.statusbar.clearMessage()

    def analyseTextuelle(self):
        self.tableWidget.setRowCount(len(self.dataset.analyse_t))
        self.tableWidget.setColumnCount(len(self.dataset.header_questions_t))
        header = ["Evaluation-"+ x for x in self.dataset.header_questions_t]
        self.tableWidget.setHorizontalHeaderLabels(header)
        for i in range(len(self.dataset.analyse_t)):
            for j in range(len(self.dataset.analyse_t[i])):
                x=float(self.dataset.analyse_t[i][j])
                x=round(x,3)
                if x>=0.5:
                    x= str(x)+" - Pas de trouble psychologique"
                else:
                    x= str(x)+" - Trouble Psychologique sévère"
                self.tableWidget.setItem(i,j, QtWidgets.QTableWidgetItem(str(x)))

    def selectionnerTout(self,selectionner):
        for row in self.checkboxs:
            for item in row:
                item.setChecked(selectionner)

    def save(self):        
        path = QtWidgets.QFileDialog.getSaveFileName(self.mainWindow)
        if not path[0]:
            return
        self.dataset.save(path[0])
    
    def activerparcourir(self):
        self.pushButton_4.setEnabled(True)
        self.pushButton_13.setEnabled(True)
        self.pushButton_2.setEnabled(True)
        self.pushButton_11.setEnabled(True)
        self.pushButton_10.setEnabled(True)

        self.pushButton_12.setEnabled(False)
        self.pushButton_14.setEnabled(False)
        self.pushButton.setEnabled(False)
        self.pushButton_8.setEnabled(False)
        self.pushButton_3.setEnabled(False)
        self.pushButton_15.setEnabled(False)
        self.list_Questions_Demographiques.clear()
        self.clearLayout(self.verticalLayout_2)
        self.pushButton_5.setEnabled(False)
        self.pushButton_6.setEnabled(False)
    
    def activerdemarrer(self):
        self.pushButton_12.setEnabled(True)
        self.pushButton_14.setEnabled(True)
        self.pushButton.setEnabled(True)
        self.pushButton_8.setEnabled(True)
        self.pushButton_3.setEnabled(True)
        self.pushButton_15.setEnabled(True)
        self.list_Questions_Textuelles.clear()




#--------------------utility func ---------------------------

    def clearLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.clearLayout(item.layout())

