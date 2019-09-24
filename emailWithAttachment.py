# -*- coding: utf-8 -*-

import mimetypes
import os
import smtplib
from email import encoders
from email.mime.audio import MIMEAudio
from email.mime.base import MIMEBase
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from csvFile import *
import os
from platform import system

class EmailWithAttachment:
    def __init__(self, sourceEmail='', password='', emailSubject='', messageText='', csvFilePath='', attachmentsPath='', messagePath=''):
        self.smtp = ''
        self.sourceEmail = sourceEmail
        self.password = password
        self.emailSubject = emailSubject
        self.messageText = messageText
        self.csvFilePath = csvFilePath
        self.csvFile = CsvFile(self.csvFilePath)
        #self.csvFile = CsvFile('./Relatorios/relatorio.csv')
        self.attachmentsPath = attachmentsPath
        self.attachmentsInPdf = self.openAttachmentsPath()
        #self.attachmentsInPdf = os.listdir('./Anexos')
        self.messagePath = messagePath

        self.csvFile.readCsvFile()
        self.messageText = self.createHtmlMessage()
        self.associatedWithSlips()

    def openAttachmentsPath(self):
        try:
            return os.listdir(self.attachmentsPath)
        except:
            print('\033[1;40;31m' + '\nErro ao abrir o arquivo!: ' + '\033[0;0m' + self.attachmentsPath + '\n')

    def createHtmlMessage(self):
        #htmlFile = open('./Modelo de Mensagem/messageTemplate.html', 'r')
        try:
            htmlFile = open(self.messagePath, 'r')
            msgTexto = htmlFile.read().replace('\n', '').replace('#!MESSAGE!#', self.messageText)
            htmlFile.close()
            return msgTexto
        except:
            print('\033[1;40;31m' + '\nErro ao abrir o arquivo!: ' + '\033[0;0m' + self.messagePath + '\n')
        

    def addAttachment(self, msg, filename):
        if not os.path.isfile(filename):
            return
        ctype, encoding = mimetypes.guess_type(filename)
        if ctype is None or encoding is not None:
            ctype = 'application/octet-stream'
        maintype, subtype = ctype.split('/', 1)
        if maintype == 'text':
            with open(filename) as f:
                mime = MIMEText(f.read(), _subtype=subtype)
        elif maintype == 'image':
            with open(filename, 'rb') as f:
                mime = MIMEImage(f.read(), _subtype=subtype)
        elif maintype == 'audio':
            with open(filename, 'rb') as f:
                mime = MIMEAudio(f.read(), _subtype=subtype)
        else:
            with open(filename, 'rb') as f:
                mime = MIMEBase(maintype, subtype)
                mime.set_payload(f.read())
            encoders.encode_base64(mime)
        mime.add_header('Content-Disposition', 'attachment', filename=filename.replace(self.attachmentsPath, ''))
        msg.attach(mime)

    def sendEmail(self, associate, attachment):    
        #para = ['pauloroberto_nobrega@hotmail.com']
        destinationEmail = [associate.email]
            
        #Estrutura da messagem
        msg = MIMEMultipart()
        msg['From'] = self.sourceEmail
        msg['To'] = ', '.join(destinationEmail)
        msg['Subject'] = self.emailSubject

        # Corpo da messagem

        #msgTexto = '<img src="https://docs.google.com/uc?id=1-e0dFB5xH_5R42Spv06MbzpXGXoUFL_M"alt=""><p id="rodape" style="color: #51a7f9; font-weight: bold; font-size: 8px; line-height: 1.5;">ASSUNIVASF  - Associação dos Servidores da Fundação - UNIVASF<br>Av. Souza Filho, 553/201 - Galeria Imperial Center - Centro<br>CEP 56304-000  PETROLINA-PE<br>Telefones (87) 3861-4244<br>Site: www.assunivasf.com.br - Visite a página da ASSUNIVASF no Facebook e Instagram.</p>'
        msg.attach(MIMEText(self.messageText, 'html', 'utf-8'))
            
        # Arquivos anexos.
        self.addAttachment(msg, attachment)
        raw = msg.as_string()
            
        if '@hotmail.com' in self.sourceEmail or '@live.com' in self.sourceEmail or '@outlook.com' in self.sourceEmail:
            smtp = smtplib.SMTP('smtp-mail.outlook.com', '587')  # para envio pelo Hotmail
            smtp.ehlo()  # Só usa para o envio pelo Hotmail
            smtp.starttls()  # Só usa para o envio pelo Hotmail
            smtp.login(self.sourceEmail, self.password)

            try:
                smtp.sendmail(self.sourceEmail, destinationEmail, raw)
                smtp.close()  # Só usa para o envio pelo Hotmail
                print('-=' * 50)
                print('\033[1;40;32m' + 'Enviado com SUCESSO' + '\033[0;0m:')
                print('Nome:', associate.name, '\nE-Mail:', associate.email, '\nArquivo:', '\033[1;0;32m' + str(associate.bankSlip) + '\033[0;0m')
            except:
                print('-=' * 50)
                print('\033[1;40;31m' + 'ERRO ao enviar email' + '\033[0;0m')
                print('Nome:', associate.name, '\nE-Mail:', associate.email, '\nArquivo:', '\033[1;0;32m' + str(associate.bankSlip) + '\033[0;0m')

        elif '@gmail.com' in self.sourceEmail:
            smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # para envio pelo Gmail
            smtp.login(self.sourceEmail, self.password)

            try:
                smtp.sendmail(self.sourceEmail, destinationEmail, raw)
                smtp.quit()
                print('-=' * 50)
                print('\033[1;40;32m' + 'Enviado com SUCESSO' + '\033[0;0m:')
                print('Nome:', associate.name, '\nE-Mail:', associate.email, '\nArquivo:', '\033[1;0;32m' + str(associate.bankSlip) + '\033[0;0m')
            except:
                print('-=' * 50)
                print('\033[1;40;31m' + 'ERRO ao enviar email' + '\033[0;0m')
                print('Nome:', associate.name, '\nE-Mail:', associate.email, '\nArquivo:', '\033[1;0;32m' + str(associate.bankSlip) + '\033[0;0m')


    def associatedWithSlips(self):
            for associate in self.csvFile.associates:
                if associate.method == 'Boleto':
                    for attachment in self.attachmentsInPdf:
                        if removeAaccent(associate.name).upper() in removeAaccent(attachment).upper():
                            associate.bankSlip = attachment
        
    def verify(self):
        self.attachmentsInPdf = self.openAttachmentsPath()
        self.csvFile = CsvFile(self.csvFilePath)
        self.csvFile.readCsvFile()
        self.associatedWithSlips()


        print('\n\nAssociados com boleto em PDF \033[1;40;32m' + 'CORRETOS!' + '\033[0;0m\n\n')
        i = 0

        for associate in self.csvFile.associates:
            if associate.method == 'Boleto': 
                if associate.bankSlip != None:
                    print('-=' * 50)        
                    print('Nome:', associate.name, '\nE-Mail:', associate.email, '\nArquivo:', '\033[1;0;32m' + str(associate.bankSlip) + '\033[0;0m')                      
                    i += 1

        print('-=' * 50) 
        print('Total: ' + str(i))

        print('\n\nAssociados com boleto em PDF \033[1;40;31m' + 'INCORRETOS!' + '\033[0;0m\n\n')
        i = 0  

        for associate in self.csvFile.associates:
            if associate.method == 'Boleto': 
                if associate.bankSlip == None:
                    print('-=' * 50)
                    print('Nome:', associate.name, '\nE-Mail:', associate.email, '\nArquivo:', '\033[1;0;31m' + str(associate.bankSlip) + '\033[0;0m')
                    i += 1

        print('-=' * 50) 
        print('Total: ' + str(i))

def clearScreen():
    if system() == 'Linux':
        os.system('clear')
    else:
        os.system('cls')

def verifyEmailPassword(sourceEmail, password):
    if '@hotmail.com' in sourceEmail or '@live.com' in sourceEmail or '@outlook.com' in sourceEmail:
        smtp = smtplib.SMTP('smtp-mail.outlook.com', '587')
        smtp.ehlo()  # Só usa para o envio pelo Hotmail
        smtp.starttls()  # Só usa para o envio pelo Hotmail
    elif '@gmail.com' in sourceEmail:
        smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)


    try:
        smtp.login(sourceEmail, password)
        smtp.quit()
        clearScreen()
        print('\033[1;40;32m' + '\nE-Mail e Senha CORRETOS!\n' + '\033[0;0m \n')
        return True
    except:
        clearScreen()
        print('\033[1;40;31m' + '\nE-Mail e/ou Senha INCORRETOS!\nDigite Novamente: ' + '\033[0;0m \n')
        return False  


def removeAaccent(txt):
    return normalize('NFKD', txt).encode('ASCII', 'ignore').decode('ASCII')
 
if __name__ == '__main__':
    from doctest import testmod
    testmod()

''' csvFileRelFin = CsvFile('./Relatorios/relatoriofinanceiro.csv')
csvFileRelFin.readCsvFileNoEmail()
csvFileRes = CsvFile('./Relatorios/associadosBoletoComEmail.csv')
csvFileRes.createCsvFile(['NOME', 'EMAIL']) '''

#Criando o arquivo associadosBoletoComEmail.csv com nome e emails dos associados que pagam com boleto
''' for assRel in csvFileRel.associates:
    for assRelFin in csvFileRelFin.associates:
        if removeAaccent(assRelFin.name) == removeAaccent(assRel.name):
            csvFileRes.writeRowCsvFile([assRel.name, assRel.email]) '''

''' attachmentStrList = []
for attachment in attachmentsInPdf:
    attachmentStr = attachment.split() #Quebra string transformando-a em uma lista
    attachmentStr.pop() #remove o ultimo elemento da lista
    attachmentStr = ' '.join(attachmentStr) #transforma a lista em string
    attachmentStrList.append(attachmentStr) '''
             
''' for associate in csvFileRel.associates:
    sendEmail(associate.email, associate.name + ' ' + diaMesAno)
    print(associate.email, ' - ', associate.name + ' 05.09.19.pdf')
#print(openCsvFile.checkEmailByName('MARCELO FORTE BEZERRA')) '''

''' def associateHasBankSlip(csvFileRel):
    for associate in csvFileRel.associates:
        for attachment in attachmentsInPdf:
            if associate.name in attachment:
                associate.haveBankSlip = True
        
associateHasBankSlip(csvFileRel) '''