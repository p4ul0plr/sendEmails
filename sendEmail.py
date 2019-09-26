from getpass import getpass
from emailWithAttachment import *
from jsonFile import JsonFile
from time import sleep
from sys import exit

def menuConfigs():
    clearScreen()
    option = input('\n\nEscolha uma das opções abaixo: \n1 - Configuração de diretórios\n2 - Serviços de E-Mail\n3 - Sair\nOpção: ')
    while option not in ['1', '2', '3']:
        option = input('\033[1;40;31m' + 'Opção INVÁLIDA!' + '\033[0;0m' + ' - Digite uma opção válida!\nOpção: ')

    if option == '1':
        setPaths()
    elif option =='2':
        menu()
    elif option == '3':
        exit

def setPaths():
    clearScreen()
    option = input('\n\nEscolha uma das opções abaixo: \n1 - Configurar\n2 - Exibir diretórios\n3 - Voltar\n4 - Sair\nOpção: ')
    while option not in ['1', '2', '3', '4']:
        option = input('\033[1;40;31m' + 'Opção INVÁLIDA!' + '\033[0;0m' + ' - Digite uma opção válida!\nOpção: ')

    if option =='1':
        print('\n\nConfiguração dos diretórios:\n')
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
        setPaths()

    elif option == '2':
        clearScreen()
        jsonFile.read()
        print('\n\nDiretórios: \n')
        print('Arquivo de relatórios (.csv): ' + '\'' + jsonFile.config['csvFilePath'] + '\'')
        print('Boletos em PDF: ' + '\'' + jsonFile.config['attachmentsPath'] + '\'')
        print('Modelo de menssagem (.html): ' + '\'' + jsonFile.config['messagePath'] + '\'')

        option = input('\n\nEscolha uma das opções abaixo: \n1 - Voltar\n2 - Sair\nOpção: ')
        while option not in ['1', '2']:
            option = input('\033[1;40;31m' + 'Opção INVÁLIDA!' + '\033[0;0m' + ' - Digite uma opção válida!\nOpção: ')

        if option == '1':
            setPaths()
        elif option == '2':
            exit

    elif option =='3':
        menuConfigs()
        
    elif option =='4':
        exit
    
def menu():
    clearScreen()
    flag = True

    option = input('\n\nEscolha uma das opções abaixo: \n1 - Enviar E-Mail\n2 - Verificar arquivos\n3 - Voltar\n4 - Sair\nOpção: ')
    while option not in ['1', '2', '3', '4']:
        option = input('\033[1;40;31m' + 'Opção INVÁLIDA!' + '\033[0;0m' + ' - Digite uma opção válida!\nOpção: ')

    if option == '1':
        clearScreen()
        print('\n\n')
        flag = False

        while True:
            sourceEmail = input('Digite o E-Mail de origem: ')
            password = getpass('Digite sua senha: ')
            if verifyEmailPassword(sourceEmail, password):
                break

        emailSubject = input('Assunto do E-Mail: ')
        messageText = input('Texto da messagem: ')

        jsonFile.read()
        emailWithAttachment = EmailWithAttachment(
            sourceEmail, 
            password, 
            emailSubject, 
            messageText, 
            jsonFile.config['csvFilePath'], 
            jsonFile.config['attachmentsPath'], 
            jsonFile.config['messagePath']
        )

        emailWithAttachment.verify()

        option = input('\n\nEscolha uma das opções abaixo: \n1 - Confirmar e enviar para os emails marcados como corretos\n2 - Voltar\n3 - Sair\nOpção: ')
        while option not in ['1', '2', '3']:
            option = input('\033[1;40;31m' + 'Opção INVÁLIDA!' + '\033[0;0m' + ' - Digite uma opção válida!\nOpção: ')

        if option == '1':
            print('\n\n')
            for associate in emailWithAttachment.csvFile.associates:
                if associate.method == 'Boleto' and associate.bankSlip != None:
                    emailWithAttachment.sendEmail(
                        associate, 
                        emailWithAttachment.attachmentsPath + str(associate.bankSlip)
                    )

            print('-=' * 50)
            print('\n\n' + '\033[1;40;32m' + 'Envio de E-mails concluido' + '\033[0;0m')
            option = input('\n\nEscolha uma das opções abaixo: \n1 - Voltar\n2 - Sair\nOpção: ')
            while option not in ['1', '2', '3']:
                option = input('\033[1;40;31m' + 'Opção INVÁLIDA!' + '\033[0;0m' + ' - Digite uma opção válida!\nOpção: ')
            
            if option =='1':
                menu()
            elif option =='2':
                exit

        elif option == '2':
            menu()

        elif option == '3':
            exit
        
    elif option == '2':
        clearScreen()

        jsonFile.read()
        if flag:
            verifyEmail = EmailWithAttachment(
                '',
                '',
                '',
                '',
                jsonFile.config['csvFilePath'], 
                jsonFile.config['attachmentsPath'],
                jsonFile.config['messagePath']
            )
            verifyEmail.verify()
        else:
            print('\033[1;40;32m' + '\nE-Mail e Senha CORRETOS!\n' + '\033[0;0m \n')
            print('Assunto do E-Mail:', emailSubject)
            print('Texto da messagem:', messageText)
            emailWithAttachment.verify()

        option = input('\n\nEscolha uma das opções abaixo: \n1 - Voltar\n2 - Sair\nOpção: ')
        while option not in ['1', '2']:
            option = input('\033[1;40;31m' + 'Opção INVÁLIDA!' + '\033[0;0m' + ' - Digite uma opção válida!\nOpção: ')

        if option == '1':
            menu()
        elif option == '2':
            exit
        
    elif option == '3':
        menuConfigs()

    elif option == '4':
        clearScreen()
        exit

jsonFile = JsonFile()
jsonFile.read()
menuConfigs()