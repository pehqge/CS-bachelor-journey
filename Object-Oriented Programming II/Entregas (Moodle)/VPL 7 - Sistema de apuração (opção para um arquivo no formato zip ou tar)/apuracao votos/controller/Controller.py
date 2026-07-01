from view.MenuView import MenuView
from view.GeradorView import GeradorView
from view.ComputaView import ComputaView
from model.Gerador import GeradorModel
from model.Apuracao import Apuracao
import PySimpleGUI as sg
import matplotlib.pyplot as plt

class Controller:
    def __init__(self):
        self.__tela_menu = MenuView()
        self.__tela_gerador = GeradorView()
        self.__tela_computa = ComputaView()

    def main(self):
        self.__tela_menu.tela_consulta()
        
        while True:
            evento, valores = self.__tela_menu.le_eventos()

            if evento == sg.WIN_CLOSED:
                break

            if evento == "Gerar Votos":
                self.__tela_menu.fim()
                self.mostrar_tela_gerador()
            
            if evento == "Computar Votos":
                self.__tela_menu.fim()
                self.mostrar_tela_computa()
        
        self.__tela_menu.fim()
                

    def mostrar_tela_gerador(self):
        self.__tela_gerador.tela_consulta()
        
        while True:
            evento, valores = self.__tela_gerador.le_eventos()

            if evento == sg.WIN_CLOSED:
                self.__tela_gerador.fim()
                self.__tela_menu.tela_consulta()
                break

            if evento == "Gerar Votos":
                try:
                    GeradorModel(valores["-FOLDER-"], valores["-REGIOES-"], valores["-CANDIDATOS-"])
                    sg.popup("Votos gerados com sucesso!")
                except ValueError:
                    sg.PopupError("Por favor, escreva números inteiros positivos nos campos de candidatos e regiões.")
                except FileNotFoundError:
                    sg.PopupError("Por favor, selecione uma pasta válida.")

            if evento == "Voltar":
                self.__tela_gerador.fim()
                self.__tela_menu.tela_consulta()

        
    def mostrar_tela_computa(self):
        self.__tela_computa.tela_consulta()
        
        while True:
            evento, valores = self.__tela_computa.le_eventos()

            if evento == sg.WIN_CLOSED:
                self.__tela_computa.fim()
                self.__tela_menu.tela_consulta()
                break

            if evento == "Computa Região":
                try:
                    if valores["-COMBO-"] == "bar":
                        apuracao = Apuracao()
                        apuracao.computa_regioes(valores["-FOLDER-"])
                        apuracao.plotar_grafico_bar_regioes()
                    elif valores["-COMBO-"] == "pie":
                        apuracao = Apuracao()
                        apuracao.computa_regioes(valores["-FOLDER-"])
                        apuracao.plotar_grafico_pie_regioes()
                    else:
                        sg.PopupError("Por favor, selecione um tipo de gráfico.")
                except FileNotFoundError:
                    sg.PopupError("Por favor, selecione uma pasta válida.")
            

            if evento == "Computa Candidatos":
                try:
                    if valores["-COMBO-"] == "bar":
                        apuracao = Apuracao()
                        apuracao.computa_regioes(valores["-FOLDER-"])
                        apuracao.plotar_grafico_bar_candidatos()
                    elif valores["-COMBO-"] == "pie":
                        apuracao = Apuracao()
                        apuracao.computa_regioes(valores["-FOLDER-"])
                        apuracao.plotar_grafico_pie_candidatos()
                    else:
                        sg.PopupError("Por favor, selecione um tipo de gráfico.")
                except FileNotFoundError:
                    sg.PopupError("Por favor, selecione uma pasta válida.")
                

            if evento == "Voltar":
                self.__tela_computa.fim()
                self.__tela_menu.tela_consulta()