import json

class JsonFile:
    def __init__(self, filePath='./sendEmail_Files/Configuracoes/config.json'):
       self.config = {}
       self.jsonFile = ''
       self.filePath = filePath
       
    def __str__(self):
        return str(self.config)

    def read(self, filePath='./sendEmail_Files/Configuracoes/config.json'):
        try:
            self.jsonFile = json.load(open(self.filePath, encoding='utf8'))
            self.config.update(self.jsonFile)
            return True
        except:
           print('\033[1;40;31m' + '\nErro ao abrir arquivo de configurações!: ' +'\033[0;0m' + str(self.filePath) + '\n')
           return False      

    def write(self, config):
        with open(self.filePath, 'w') as jsonFile:
            jsonFile = json.dump(config, jsonFile)
            self.config.update(self.jsonFile)
