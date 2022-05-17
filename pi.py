import PySimpleGUI as sg
from zeep import Client
from requests import Session
from requests.auth import HTTPBasicAuth
from zeep.transports import Transport
from zeep.exceptions import Fault

#Testa o link da API dos Correios
try:
  wsdl = 'https://cws.correios.com.br/pedidoInformacaoWS/pedidoInformacaoService/pedidoInformacaoWS?wsdl'
  session = Session()
  session.auth = HTTPBasicAuth('usuarioIDCorreios', 'senhaIDCorreios')
  client = Client(wsdl=wsdl, transport=Transport(session=session))
except Fault as fault:
  parsed_fault_detail = client.wsdl.types.deserialize(fault.detail[0])


#O trecho comentando a seguir mostra outra forma de retornar o valor do PI usando uma função
#Altere NUM_CONTRATO para seu contrato dos Correios
#def func_princ(num): 
#   teste = client.service.consultarAcompanharRegistrarOcorreciaComContrato('NUM_CONTRATO', num, 'C')
#   print(teste['mensagemUltimaResposta'])


sg.theme('DarkAmber')   # Tema pré-configurado da lib PySimpleGUI.

# Define os elementos do layout da janela.
layout = [  [sg.Text('Insira o numero do PI')],
            [sg.Text('PI'), sg.InputText(do_not_clear=False)],
            [sg.Button('Pesquisar'), sg.Button('Cancel')],
            [sg.Multiline(size=(50, 10), key='-TEXT-')] ]

# Cria a janela
window = sg.Window('Consultar PI', layout)

# Loop para processar os eventos e receber os valores do input
while True:
    event, values = window.read()
    if event == sg.WIN_CLOSED or event == 'Cancel': # Finaliza o programa se o usuário clicar em cancelar ou fechar a janela.
        break

    #print('Mensagem: ', func_princ(values[0])) #Trecho comentado | Caso você queira chamar uma função.
    
    resposta = client.service.consultarAcompanharRegistrarOcorreciaComContrato('NUM_CONTRATO', values[0], 'C')
    retorno = resposta['mensagemUltimaResposta']

    #A condicional abaixo testa se a resposta do Webservice é valida ou não. 
    if (retorno != None):
      window['-TEXT-'].update(retorno)
    else:
      window['-TEXT-'].update("Ainda não há resposta dos Correios ou o número é invalido")

window.close()