import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
import GEOparse
import numpy as np
from scipy.stats.stats import ks_2samp
import pandas as pd

# загружаем оболочку тула
form_class = uic.loadUiType("./gsea1/mainwindow.ui")[0]

class Window(QMainWindow, form_class):
    
    def __init__(self):
#        вызываем конструктор суперкласса
        super(Window, self).__init__()
        self.setupUi(self)

        self.home() 
# по клику на кнопку вызываем функцию и соответственный ответ
    def home(self):

        self.pushButton.clicked.connect(self.pushButton_clicked)

        self.show()
# что реализуется по клику:
    def pushButton_clicked(self):
#        считываем текст, введенный в ячейку имени файла и ячейку генов
        gse_acc = self.lineEdit.text()
        mytext = self.textEdit.toPlainText()
#        делаем из генов список
        genes = mytext.split()
#        загружаем файл по имени
        gse = GEOparse.get_GEO(geo=gse_acc, destdir="./")
#        получаем матрицу экспрессии по генам и образцам
        expression = gse.pivot_samples('VALUE').T

#        получаем список из фенотипов: если в описании присутствует слово 
#        "control", считаем это контролем и присваиваем 1
        experiments = {}
        for i, (idx, row) in enumerate(gse.phenotype_data.iterrows()):
            tmp = {}
            tmp["Type"] = 1 if "control" in row["description"] else 0
            experiments[i] = tmp
        experiments = pd.DataFrame(experiments).T
        phen=list(experiments['Type'])
#        строим матрицы корреляций (как в классе)
        counter = 0
        all_genes_set = [] 
        all_corr_set = [] 
        genes_corr_set = []
        for column in expression:
                    counter += 1
                    if counter <= 3:
                        continue
                    
                    expressions = list(expression[column])
                    gene = column
                    all_genes_set.append(column)
                    
                    corr_matrix = np.corrcoef([phen, expressions])
                    all_corr_set.append(corr_matrix[0,1])
                    if gene in genes:
                        genes_corr_set.append(corr_matrix[0,1])
                        
#        получаем p-value по тесту Колмогорова-Смирнова
        p_value = ks_2samp(genes_corr_set, all_corr_set)[1]
#        выводим его в окошко 
        self.label_3.setText('{:.3f}'.format(p_value))

        
def run():
    app = QApplication(sys.argv)
    
    GUI = Window()
    app.exec_()

if __name__ == "__main__":
    run()
        
