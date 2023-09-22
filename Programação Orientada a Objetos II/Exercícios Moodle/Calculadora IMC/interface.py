import PySimpleGUI as sg

# Definindo o layout da janela
layout = [
    [sg.Text('Calculadora de IMC', justification='center', size=(20, 1), font=('Helvetica', 16))],
    [sg.Text('Peso (kg):'), sg.Input(key='peso')],
    [sg.Text('Altura (m):'), sg.Input(key='altura')],
    [sg.Button('Calcular IMC')],
    [sg.Text('', size=(20, 1), key='resultado', font=('Helvetica', 14))]
]

# Criando a janela
window = sg.Window('Calculadora de IMC', layout, resizable=True, finalize=True)

# Loop principal
while True:
    event, values = window.read()

    # Verifica se o usuário fechou a janela
    if event == sg.WINDOW_CLOSED:
        break

    # Se o botão 'Calcular IMC' foi pressionado
    if event == 'Calcular IMC':
        try:
            # Obtém os valores de peso e altura fornecidos pelo usuário
            peso = float(values['peso'])
            altura = float(values['altura'])

            # Calcula o IMC
            imc = peso / (altura ** 2)

            # Exibe o resultado na interface
            window['resultado'].update(f'Seu IMC é: {imc:.2f}')
        except ValueError:
            # Trata erros de entrada inválida
            window['resultado'].update('Por favor, insira valores válidos para peso e altura.')

# Fechando a janela
window.close()
