import sys
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
import GEOparse
import numpy as np
from scipy.stats.stats import ks_2samp
import pandas as pd
import argparse

def parse_inputs():
     parser = argparse.ArgumentParser(description='GSEA')
     parser.add_argument('-i', '--input' , help='Input file' , metavar='Str',
                    type=str, required=True)
     args = parser.parse_args()
     return args.input


class Window(QMainWindow, uic.loadUiType(parse_inputs())[0]):
    
    def __init__(self):
#        вызываем конструктор суперкласса
#        call super class constructor
        super(Window, self).__init__()
        self.setupUi(self)

        self.home() 
# по клику на кнопку вызываем функцию и соответственный ответ
# by clicking the button call the function and the corresponding reaction
    def home(self):

        self.pushButton.clicked.connect(self.pushButton_clicked)

        self.show()
# что реализуется по клику:
# what is implemented by clicking: 
    def pushButton_clicked(self):
#        считываем текст, введенный в ячейку имени файла и ячейку генов
#        read the text entered into filename and genes cells
        gse_acc = self.lineEdit.text()
        mytext = self.textEdit.toPlainText()
#        делаем из генов список
#        make list from genes
        genes = mytext.split()
#        загружаем файл по имени
#        upload file by filename
        gse = GEOparse.get_GEO(geo=gse_acc, destdir="./")
#        получаем матрицу экспрессии по генам и образцам
#        get expression matrix by genes and samples
        expression = gse.pivot_samples('VALUE').T

#        получаем список из фенотипов: если в описании присутствует слово 
#        "control", считаем это контролем и присваиваем 1
#         retrieve phenotype list: if the "control" word is in the description,
#         we consider it control group and assign 1 to it
"        experiments = {}
        for i, (idx, row) in enumerate(gse.phenotype_data.iterrows()):
            tmp = {}
            tmp["Type"] = 1 if "control" in row["description"] else 0
            experiments[i] = tmp
        experiments = pd.DataFrame(experiments).T
        phen=list(experiments['Type'])
#        строим матрицы корреляций (как в классе)
#        build correlation matrices
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
#        get p-value using the Kolmogorov-Smirnov test
        p_value = ks_2samp(genes_corr_set, all_corr_set)[1]
#        выводим его в окошко 
#        print p-value
        self.label_3.setText('{:.3f}'.format(p_value))

        
def run():
    app = QApplication(sys.argv)
    
    GUI = Window()
    app.exec_()

if __name__ == "__main__":
    run()
        
