from R_connexion import R_connexion
import csv
from rpy2.rinterface_lib.embedded import RRuntimeError
from analyse import analyse

class Dataset:
    def __init__(self,path):
        self.grm=False
        self.filtered=False
        self.path=path
        self.dataset=[]
        self.nbquestion=0
        self.options_d=[]
        self.questions_d=[]
        self.header_questions_d=[]
        self.header_questions_t=[]
        self.questions_t=[]
        self.header=[]
        self.header_questions_non_d=[]
        self.analyse_t=[]
        self.filtereddata=[]
        self.analyse = analyse()
        
        name=path.split("/")
        self.name=name[len(name)-1]
        csv_reader = csv.reader(open(path,"r",encoding='utf-8'), delimiter=";")
        for row in csv_reader:
            self.dataset.append(row)
        self.nbquestion=len(self.dataset[0])
        self.header=self.dataset[0]
        self.header_questions_non_d=self.dataset[0]
        self.dataset=self.dataset[1:]

        l=self.name.split(".")
        self.output="temp/temp.csv"

    def setQuestions_d(self,questions_d):
        self.questions_d=questions_d
        self.header_questions_non_d=[]
        self.header_questions_d=[]
        for i in range(len(self.header)):
            if not i in self.questions_d:
                self.header_questions_non_d.append(self.header[i])

        for i in self.questions_d:
            ops=[row[i] for row in self.dataset]
            ops=list(set(ops))
            ops.sort()
            self.options_d.append(ops)
            self.header_questions_d.append(self.header[i])
    def setQuestions_t(self,question_t):
        self.questions_t=question_t
        self.header_questions_t=[]
        for i in range(len(self.header)):
            if i in self.questions_t:
                self.header_questions_t.append(self.header[i])
    def filtre(self,checked_options):
        filtereddata=[]
        self.analyse_t=[]
        for row in self.dataset:
            valide=True
            for i in range(len(self.questions_d)):
                if not row[self.questions_d[i]] in checked_options[i]:
                    valide=False
            filteredrow=[]
            row_t=[]
            if valide:
                for i in range(len(row)):
                    if i in self.questions_d:
                        continue
                    elif i in self.questions_t:
                        text=row[i]
                        x=self.analyse.analyser(text)
                        row_t.append(str(x))
                        filteredrow.append(str(round(x*10)))
                    else:
                        filteredrow.append(row[i])
                filtereddata.append(filteredrow)
                self.analyse_t.append(row_t)
        with open(self.output, mode='w',newline='',encoding='utf-8') as output:
            csv_writer = csv.writer(output, delimiter=';', quotechar='"',quoting=csv.QUOTE_ALL)
            csv_writer.writerow(self.header_questions_non_d)
            csv_writer.writerows(filtereddata)
        output.close()
        self.filtereddata=filtereddata
        self.filtered=True
        self.grm=False
    def GRM(self):
        if self.grm:
            return True
        try:
            if self.filtered:
                self.R= R_connexion(self.output,"dataset"+self.name.split(".")[0])
            else:
                self.R=R_connexion(self.path,"dataset"+self.name.split(".")[0])
            self.R.Charger_données()
            self.R.GRM()
        except RRuntimeError:
            return False
        self.grm=True
        return True
    def analyserQuestionnaire(self):
        self.R.AnalyserQuestionnaire()
    def tendance(self,name):
        self.R.Tendance(name)
    def save(self,path):
        with open(path, mode='w',newline='',encoding='utf-8') as output:
            csv_writer = csv.writer(output, delimiter=';', quotechar='"',quoting=csv.QUOTE_ALL)
            csv_writer.writerow(self.header_questions_non_d)
            csv_writer.writerows(self.filtereddata)
        output.close()







