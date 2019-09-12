# -*- coding: utf-8 -*-
import csv
from associate import *
from unicodedata import normalize

def removeAaccent(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
 
if __name__ == '__main__':
    from doctest import testmod
    testmod()

class CsvFile:
    def __init__(self, path):
        self.associates = []
        self.path = path
    
    def createCsvFile(self, columnNames):
        try:
            #O 'w' cria o arquivo e apaga os dados existentes. O 'a+' adiciona uma nova linha e não apaga o arquivo
            with open(self.path, 'w',  newline='') as csvfile:
                self.spamwriter = csv.writer(csvfile)
                self.spamwriter.writerow(columnNames)
        except:
            print("Erro ao criar arquivo: \'" + self.path + "\'")

    def readCsvFile(self):
        try:
            with open(self.path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        self.associates.append(Associate(row["\ufeff\ufeffNOME"], row["MÉTODO"], row["EMAIL"]))
                    except:
                        try:
                            self.associates.append(Associate(row["\ufeffNOME"], row["MÉTODO"], row["EMAIL"]))
                        except:
                            self.associates.append(Associate(row["NOME"], row["MÉTODO"], row["EMAIL"]))  
        except:
            print("Erro ao ler do arquivo: \'" + self.path + "\'")

    def readCsvFileNoEmail(self):
        try:
            with open(self.path, newline='') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    try:
                        self.associates.append(Associate(row["\ufeff\ufeffNOME"]))
                    except:
                        self.associates.append(Associate(row["\ufeffNOME"]))
                    
        except:
            print("Erro ao ler do arquivo: \'" + self.path + "\'")

    def checkEmailByName(self, nameAss):
        for associate in self.associates:
            if nameAss == associate.name:
                return associate.email
            else:
                return "Associado não está presente no arquivo: \'" + self.path + "\'"

    def writeRowCsvFile(self, row):
        with open(self.path, 'a+',  newline='') as csvfile:
            self.spamwriter = csv.writer(csvfile)
            self.spamwriter.writerow(row)

""" csvFile = CsvFile('./Relatorios/associadosBoletoComEmail.csv')
csvFile.createCsvFile(['NOME', 'EMAIL'])
csvFile.writeRowCsvFile(['Paulo', 'bla@gmail.com'])
csvFile.writeRowCsvFile(['João', 'ola@hotmail.com'])

csvFile1 = CsvFile('./Relatorios/associadosBoletoComEmail.csv')
csvFile1.readCsvFile()
print(csvFile1.checkEmailByName('Paulo')) """

""" Ciar um novo CSV com a intersecção de associadosBoletoComEmail.csv com relatorio.csv e criar
Um novo CSV com o resultado """

""" csvFileRel = CsvFile('./Relatorios/relatorio.csv')
csvFileRel.readCsvFile()
csvFileRelFin = CsvFile('./Relatorios/relatoriofinanceiro.csv')
csvFileRelFin.readCsvFileNoEmail()
csvFileRes = CsvFile('./Relatorios/associadosBoletoComEmail.csv')
csvFileRes.createCsvFile(['NOME', 'EMAIL'])

for assRel in csvFileRel.associates:
    for assRelFin in csvFileRelFin.associates:
        if removeAaccent(assRelFin.name) == removeAaccent(assRel.name):
            csvFileRes.writeRowCsvFile([assRel.name, assRel.email]) """



