from Participant import *
import rpy2.robjects as robjects
from rpy2.rinterface_lib.embedded import RRuntimeError
from re import match
from os import path
from pathlib import Path
from PyQt5.QtWebEngineWidgets import QWebEngineView
from bokeh.models.annotations import Legend, Title
from bokeh.plotting import Figure,output_file,show,save
from bokeh.plotting.figure import figure
from bokeh.plotting import ColumnDataSource
from bokeh.models import tools



class ParticipantImp(Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.datasets=[]
    def setupUi(self, MainWindow):
        super().setupUi(MainWindow)
        self.canvas = QWebEngineView(self.centralwidget)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.canvas.sizePolicy().hasHeightForWidth())
        self.canvas.setSizePolicy(sizePolicy)
        self.canvas.setMinimumSize(QtCore.QSize(480, 480))
        self.canvas.setMaximumSize(QtCore.QSize(480, 480))
        self.canvas.setObjectName("canvas")
        self.gridLayout.addWidget(self.canvas, 1, 0, 1, 1)

        self.m=MainWindow
        MainWindow.setWindowTitle("Participant")
        MainWindow.setWindowIcon(QtGui.QIcon("icon.png"))
        self.pushButton.clicked.connect(self.resultat)
        print("test")
    def resultat(self):
        Path("temp").mkdir(parents=True, exist_ok=True)
        self.label_3.setText("")
        self.label_4.setText("")
        self.label_5.setText("")
        verification=True
        datasetexiste=True
        if(bool(match("\d+$", self.lineEdit.text()))==False):
            verification=False
            self.label_4.setText("ID Participant n'est pas valide")
        if(bool(match("\d+$", self.lineEdit_2.text()))==False):
            verification=False
            self.label_5.setText("ID Dataset n'est pas valide")
        if verification==False:
            return
        if path.exists("dataset/"+self.lineEdit_2.text()+".csv")==False:
            self.label_5.setText("Dataset n'existe pas")
            verification=False
        if verification==False:
            return
        dataset=self.lineEdit_2.text()
        robjects.r("data<- read.table('dataset/"+dataset+".csv', sep=';',header=TRUE)")
        nbparticipant = robjects.r("dim(data)[1]")
        id=int(self.lineEdit.text())
        if id==0 or id>nbparticipant[0]:
            verification=False
            self.label_4.setText("ID Participant n'existe pas")
        if verification==False:
            return        
        robjects.r("dataidp<- data["+self.lineEdit.text()+",]")
        if (dataset in self.datasets) == False:
            try:
                self.statusbar.showMessage("Analyse du dataset")
                robjects.r("fit<- grm(data)")
            except RRuntimeError:
                msg = QtWidgets.QMessageBox(self.m)
                msg.setIcon(QtWidgets.QMessageBox.Critical)
                msg.setText("Erreur lors de l'application de la méthode grm au dataset")
                msg.setWindowTitle("Erreur")
                msg.exec_()
                self.statusbar.clearMessage()
                return
            self.statusbar.showMessage("Estimation des scores")
            robjects.r("factor"+dataset+"<-ltm::factor.scores(fit,method='EB')")
            self.datasets.append(dataset)
        robjects.r("factor<-factor"+dataset)
        self.statusbar.showMessage("Détermination de votre score")
        robjects.r("datasc<-factor[['score.dat']]")
        filtre="datasc["
        dim=robjects.r("dim(dataidp)[2]")
        for i in range(1,dim[0]+1):
            filtre=filtre+"datasc[,"+str(i)+"] %in% c(dataidp[,"+str(i)+"])"
            if(i==(dim[0])):
                filtre=filtre+",]"
            else:
                filtre=filtre+' & '
        robjects.r("score<-"+filtre)
        score=robjects.r("score[['z1']]")
        nrows=robjects.r("dim(factor[['score.dat']])[1]")
        nobst=0
        scores=robjects.r("factor[['score.dat']][['z1']]")
        for i in range(1,nrows[0]+1):
            scorei=robjects.r("factor[['score.dat']]["+str(i)+","+str(dim[0]+3)+"]")
            if(scorei[0]>score[0]):
                nobsl=robjects.r("factor[['score.dat']]["+str(i)+","+str(dim[0]+1)+"]")
                nobst=nobst+nobsl[0]
            if(scorei[0]==score[0]):
                id=i
        self.label_3.setText("Votre score est : "+str(round(score[0]*50/4+50,2))+".\nvotre état psychologique est mieux que "+str(round(nobst/nbparticipant[0]*100,2))+"% de la population.")
        robjects.r("png(filename ='temp/participant.png')")
        robjects.r("plot(factor[['score.dat']][['z1']]*50/4+50,ylab='Score')")
        robjects.r("points(x="+str(id)+",y="+str(score[0]*50/4+50)+",pch=19,col='red',cex=1)")
        robjects.r("legend(1,120, legend=c('Votre position', 'Les positions des autres participants'),col=c('red', 'black'),pch=c(19,1),cex=0.8)")
        robjects.r("dev.off()")
        y=robjects.r("factor[['score.dat']][['z1']]*50/4+50")
        occ=robjects.r("factor$score$Obs")
        output_file('temp/participant.html')
        x=range(len(y))
        p=figure(
            x_axis_label='Index',
            y_axis_label='Score',
            plot_width=450, 
            plot_height=450,
            tools="pan,wheel_zoom,reset"
        )
        source = ColumnDataSource(data=dict(
            index=x,
            score=y,
            occ=occ
        ))
        s = ColumnDataSource(data=dict(
            index=[x[id-1]],
            score=[score[0]*50/4+50],
            occ=[occ[id-1]]
        ))
        p.circle(x="index",y="score",size=7,legend_label="Positions des autres participants",source=source)
        p.circle(x="index",y="score",legend_label="Votre position",size=7,color="red",source=s)
        hover = tools.HoverTool()
        hover.tooltips="""
        <div>
            <div><strong>Score : </Strong>@score</div>
            <div><strong>Occurence : </Strong>@occ</div>
        </div>
        """
        p.legend.click_policy="hide"
        p.add_tools(hover)
        save(p)
        f=open("temp/participant.html",'r')
        self.canvas.setHtml(f.read())
        self.statusbar.clearMessage()



