arquivo = open('./Modelo de Mensagem/messageTemplate.html', 'r')
texto = arquivo.read()
print(texto.replace('\n', ''))
arquivo.close()