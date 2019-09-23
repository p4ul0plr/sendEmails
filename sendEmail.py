from getpass import getpass
from emailWithAttachment import *
from jsonFile import JsonFile
from time import sleep

def setPaths():
    if jsonFile.config['csvFilePath'] == '' and jsonFile.config['attachmentsPath'] == '' and jsonFile.config['messagePath'] == '':
        print('Configuração dos diretórios:\n')
        csvFilePath = input('Digite o caminho do arquivo de relatórios (.csv): ')
        attachmentsPath = input('Digite o camino da pasta com os boletos em PDF: ')
        messagePath = input('Digite o caminho do arquivo do modelo de menssagem (.html): ')
        config = {
            "csvFilePath": csvFilePath,
            "attachmentsPath": attachmentsPath,
            "messagePath": messagePath
        }
        jsonFile.write(config)
        print('\033[1;40;32m' + '\nDiretórios Configurados' + '\033[0;0m \n')
        sleep(3)
        clearScreen()
 
def menu():
    option = input('\n\nDeseja enviar email para destinatários marcados como CORRETOS?\n1 - Enviar\n2 - Verificar\n3 - Configurações\n4 - Cancelar\nOpção: ')
    while option not in ['1', '2', '3', '4']:
        option = input('Digite uma opção válida!\nOpção: ')

    if option == '1':
        print('\n\n')
        for associate in emailWithAttachment.csvFile.associates:
            if associate.method == 'Boleto' and associate.bankSlip != None:
                emailWithAttachment.sendEmail(associate.email, emailWithAttachment.attachmentsPath + str(associate.bankSlip))
    elif option == '2':
        clearScreen()
        print('\033[1;40;32m' + '\nE-Mail e Senha CORRETOS!\n' + '\033[0;0m \n')
        print('Assunto do E-Mail:', emailSubject)
        print('Texto da messagem:', messageText)
        emailWithAttachment.verify()
        menu()
    elif option == '3':
        csvFilePath = input('\n\nDigite o caminho do arquivo de relatórios (.csv): ')
        attachmentsPath = input('Digite o camino da pasta com os boletos em PDF: ')
        messagePath = input('Digite o caminho do arquivo do modelo de menssagem (.html): ')
        config = {
            "csvFilePath": csvFilePath,
            "attachmentsPath": attachmentsPath,
            "messagePath": messagePath
        }
        jsonFile.write(config)
        print(jsonFile.config)
        clearScreen()
        print('\033[1;40;32m' + '\nE-Mail e Senha CORRETOS!\n' + '\033[0;0m \n')
        print('Assunto do E-Mail:', emailSubject)
        print('Texto da messagem:', messageText)
        menu()
    elif option == '4':
        clearScreen()
        exit()

jsonFile = JsonFile()
setPaths()

while True:
    sourceEmail = input('Digite o E-Mail de origem: ')
    password = getpass('Digite sua senha: ')
    if verifyEmailPassword(sourceEmail, password):
        break

emailSubject = input('Assunto do E-Mail: ')
messageText = input('Texto da messagem: ')


emailWithAttachment = EmailWithAttachment(sourceEmail, password, emailSubject, messageText, jsonFile.config['csvFilePath'], jsonFile.config['attachmentsPath'], jsonFile.config['messagePath'])

menu()