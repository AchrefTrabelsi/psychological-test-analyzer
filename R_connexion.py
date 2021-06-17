from rpy2.robjects.packages import importr
from rpy2.rinterface import RRuntimeWarning
import rpy2.robjects as robjects
from rpy2.robjects.packages import PackageNotInstalledError
import os
class R_connexion: 
    def __init__(self,path,name):
        self.name=name
        self.path=path
    def Charger_données(self):
        robjects.r("data <- read.table('"+self.path+"', sep=';',header=TRUE)")
    def GRM(self):
        robjects.r("{} = grm(data)".format(self.name))
    def AnalyserQuestionnaire(self):
        robjects.r("""
        data_grm_coef= coef("""+self.name+""")
        pas=0.1
        intervalle = seq(from = -4,to = 4,by = pas)
        InfoTest=c(0)
        if(mode(data_grm_coef)!='list'){
            data_grm_coef=split(t(data_grm_coef), rep(1:nrow(data_grm_coef), each = ncol(data_grm_coef)))
        }
        i=1
        for(x in data_grm_coef){
            d=c()
            for(e in x){
                d=c(d,e)
            }
            item=item(model= "GRM",a=d[length(d)],b=d[1:(length(d)-1)])
            information=info(item,intervalle)
            p=0.95
            IC=qnorm(c(1/2+p/2), mean = 0, sd = 1)/sqrt(information)
            InfoTest=InfoTest+information
            png(filename = paste("ic/IC",i-1,".png",sep=""))
            plot(x=intervalle,y=IC,type="l",main = "Intervalle de confiance",xlab="Trouble psychologique",ylab="Intervalle de confiance")
            minor.tick(ny=10)
            dev.off()
            png(filename = paste("icc/ICC",i-1,".png",sep=""))
            plot("""+self.name+""",items = i, lwd = 2, cex = 0.8,
            legend = TRUE, cx = "topright",
            xlab = "Trouble Psychologique", cex.main = 1,ylab = "Probabilité")
            dev.off()
            i=i+1
        }
        ICTest=qnorm(c(1/2+p/2), mean = 0, sd = 1)/sqrt(InfoTest)
        png(filename ="ic/IC.png")
        plot(x=intervalle,y=ICTest,type="l",main = "Intervalle de confiance du Test",xlab="Trouble psychologique",ylab="Intervalle de confiance")
        minor.tick(ny=10)
        dev.off()

        """)
    def Tendance(self,name):
        robjects.r("""
        factor<-ltm::factor.scores("""+self.name+""",method="EB")
        png(filename = paste("tendance/"""+name+"""",1,".png",sep=""))
        plot(factor,main = "Tendance",xlab="Trouble psychologique",ylab="Densité",xaxt="n")
        axis(1, at=c(-4,0,4), labels=c('faible','moyenne','sévère'))
        dev.off()
        png(filename = paste("tendance/"""+name+"""",2,".png",sep=""))
        hist(factor[["score.dat"]][["z1"]],prob=TRUE,main = "Tendance",xlab="Trouble psychologique",ylab="Densité",xaxt="n",xlim = c(-4,4))
        axis(1, at=c(-4,0,4), labels=c('faible','moyenne','sévère'))
        dev.off()
        """)
def setupR():
    utils = importr('utils')
    utils.chooseCRANmirror(ind=1)
    packnames = ("psych","ltm","irt","Hmisc")
    for packname in packnames:
        try:
            importr(packname)
        except PackageNotInstalledError:
            utils.install_packages(packname)
            importr(packname)
