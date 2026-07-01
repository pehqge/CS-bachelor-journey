import PySimpleGUI as sg
from calculadora import CalculadoraIMC

class Interface:
    def __init__(self):
        sg.theme('Topanga')
        self.__programa = [
            [sg.Text('       Calculadora de IMC', font=('Futura', 24))],
            [sg.Text('', size=(15, 1))],
            [sg.Text('Peso (kg)  '), sg.InputText(key="peso")],
            [sg.Text('Altura (cm)'), sg.InputText(key="altura")],
            [sg.Text('', size=(15, 1))],
            [sg.Button('Calcular', size=(55, 1))],
        ]
        
        self.__janela = sg.Window('Calculadora de IMC', self.__programa)
        
    def main(self):
        while True:
            event, values = self.__janela.read()

            if event == sg.WIN_CLOSED:
                break
            elif event == "Calcular":
                try:
                    peso = float(values["peso"])
                    altura = float(values["altura"])/100
                    calculadora = CalculadoraIMC(peso, altura)
                    
                    imc = calculadora.calcular()
                    imc_tipo = calculadora.tipoIMC(imc)
                        
                    sg.popup(f"Seu IMC é {imc:.2f} e você está {imc_tipo}", title="Resultado")
                except ValueError:
                    sg.popup_error("O input está errado. Coloque valores corretos")
                    
        self.__janela.close()