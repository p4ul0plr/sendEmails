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
import getpass
from csvFile import *
import os

de = input('Digite o E-Mail de origem: ')
senha = getpass.getpass('Digite sua senha: ')
assunto = input('Assunto do E-Mail: ')
msgTexto = input('Texto da mensagem:')

def adiciona_anexo(msg, filename):
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
    mime.add_header('Content-Disposition', 'attachment', filename=filename)
    msg.attach(mime)

def sendEmail(email, attachment):
    try:
        print('\033[1;40;32m' + 'Enviado com SUCESSO' + '\033[0;0m: ' + 'Email: ' + email + 'Boleto: ' +  attachment)
        
        #para = ['pauloroberto_nobrega@hotmail.com']
        para = [email]
        
        #Estrutura da mensagem
        msg = MIMEMultipart()
        msg['From'] = de
        msg['To'] = ', '.join(para)
        msg['Subject'] = assunto

        # Corpo da mensagem
        msg.attach(MIMEText(msgTexto, 'html', 'utf-8'))
        
        # Arquivos anexos.
        adiciona_anexo(msg, attachment)
        raw = msg.as_string()
        
        if '@hotmail.com' in de or '@live.com' in de or '@outlook.com' in de:
            smtp = smtplib.SMTP('smtp-mail.outlook.com', '587')  # para envio pelo Hotmail
            smtp.ehlo()  # Só usa para o envio pelo Hotmail
            smtp.starttls()  # Só usa para o envio pelo Hotmail
            smtp.login(de, senha)
            smtp.sendmail(de, para, raw)
            smtp.close()  # Só usa para o envio pelo Hotmail
            smtp.quit()
        elif '@gmail.com' in de:
            smtp = smtplib.SMTP_SSL('smtp.gmail.com', 465)  # para envio pelo Gmail
            smtp.login(de, senha)
            smtp.sendmail(de, para, raw)
            smtp.quit()
    except:
        print('\033[1;40;31m' + 'ERRO ao enviar email: \033[0;0m' + 'Email: ' + email + 'Boleto: ' +  attachment)
        
        

csvFileRel = CsvFile('./Relatorios/relatorio.csv')
csvFileRel.readCsvFile()
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

attachmentsInPdf = os.listdir('./Anexos')
#print(attachmentsInPdf)

def associatesWithAttachments(associateName):
    for attachment in attachmentsInPdf:
        return associateName in attachment



''' def associateHasBankSlip(csvFileRel):
    for associate in csvFileRel.associates:
        for attachment in attachmentsInPdf:
            if associate.name in attachment:
                associate.haveBankSlip = True
        
associateHasBankSlip(csvFileRel) '''

i = 0
print('\n\nAssociados com boleto em PDF \033[1;40;32m' + 'CORRETOS!' + '\033[0;0m\n\n')
for associate in csvFileRel.associates:
    if associate.method == 'Boleto':
        for attachment in attachmentsInPdf:
            if associate.name in attachment:
                i += 1
                associate.bankSlip = attachment
                print(i, '- Nome:', associate.name, ', E-Mail:', associate.email, ', Método:', associate.method, ', Arquivo:', '\033[1;0;32m' + associate.bankSlip + '\033[0;0m')

i = 0
print('\n\nAssociados com boleto em PDF \033[1;40;31m' + 'INCORRETOS!' + '\033[0;0m\n\n')
for associate in csvFileRel.associates:
    if associate.method == 'Boleto' and associate.bankSlip == None:
        i += 1
        print(i, '- Nome:', associate.name, ', E-Mail:', associate.email, ', Método:', associate.method, ', Arquivo:', '\033[1;0;31m' + str(associate.bankSlip) + '\033[0;0m')

option = input('\n\nDeseja enviar email para destinatários marcados como CORRETOS?\n1 - Enviar\n2 - Tentar novamente\n3 - Cancelar\nOpção: ')
while option not in ['1', '2', '3']:
    option = input('Digite uma opção válida!\nOpção: ')

print('\n\n')

if option == '1':
    for associate in csvFileRel.associates:
        if associate.method == 'Boleto' and associate.bankSlip != None:
            sendEmail(associate.email, './Anexos/' + str(associate.bankSlip))
elif option == '1':
    pass
elif option == '3':
    exit()
