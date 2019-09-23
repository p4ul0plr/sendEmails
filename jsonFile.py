import json

class JsonFile:
    def __init__(self, filePath='./Configuracoes/config.json'):
       self.config = {}
       self.jsonFile = ''
       self.filePath = filePath

       try:
            self.jsonFile = json.load(open(self.filePath))
            self.config.update(self.jsonFile)
       except:
           print('\033[1;40;31m' + '\nErro ao abrir arquivo de configurações!: ' +'\033[0;0m' + str(self.filePath) + '\n')    

    def __str__(self):
        return str(self.config)

    def write(self, config):
        with open(self.filePath, 'w') as jsonFile:
            jsonFile = json.dump(config, jsonFile)
            self.config.update(self.jsonFile)
