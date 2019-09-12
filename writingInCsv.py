import csv
from associate import *

class WritingInCsv:
    def __init__(self):
        with open('./Relatorios/associadosBoletoComEmail.csv', 'w',  newline='') as csvfile:
            spamwriter = csv.writer(csvfile)
            spamwriter.writerow(['NOME', 'EMAIL'])
            spamwriter.writerow(['paulo', 'bla@gmail.com'])
        
writingInCsv = WritingInCsv()