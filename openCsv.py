# -*- coding: utf-8 -*-
import csv
from associate import *

class OpenCsv:
    def __init__(self, path):
        self.associated = []
        self.path = path
        #try:
        with open(self.path, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                print(row)
                self.associated.append(Associate(row["\ufeff\ufeffNOME"], None))
                    #print("Nome: ", row["\ufeff\ufeffNOME"], "E-Mail: ", row["EMAIL"])
        """ except:
            print("Erro - Arquivo invalido!") """ 
      
    def checkEmailByName(self, nameAss):
        for associate in self.associated:
            if nameAss == associate.name:
                return associate.email
            else:
                return "Associado não está presente no arquivo: " + self.path

#path = input("Informe o caminho do arquivo (.csv): ")
openCsvFile = OpenCsv('./Relatorios/relatoriofinanceiro.csv')
print(openCsvFile.checkEmailByName("CICERO BEZERRA DA SILVA JUNIOR"))