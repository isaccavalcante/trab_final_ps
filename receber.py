#!/usr/bin/env python
#-*-coding: utf-8-*-
#Autor: Isac Cavalcante <isaccavalcante@alu.ufc.br>
import pygtk, gtk
pygtk.require("2.0")
import subprocess

class JanelaReceber:
    def __init__(self):
        self.janela = gtk.Window()
        self.janela.set_position(gtk.WIN_POS_CENTER)
        self.janela.set_size_request(480, 480)
        self.janela.set_title("share - Receber um arquivo")
        self.janela.set_resizable(False)
        try:
            self.janela.set_icon_from_file("icone.png")
        except Exception:
            self.icone = self.janela.render_icon(gtk.STOCK_MISSING_IMAGE, gtk.ICON_SIZE_MENU)
            self.janela.set_icon(self.icone)
       

        self.label_instrucao = gtk.Label("Digite o IP de quem está compartilhando:")
        self.label_ip = gtk.Label("Nenhum IP escolhido.")
        self.label_instrucao2 = gtk.Label("Escolha uma porta entre 1025 e 65535:")
        self.label_porta =  gtk.Label("Nenhuma porta escolhida.")
        self.label_conexao = gtk.Label("")
        
        self.botao_voltar = gtk.Button("<Voltar".center(30))
        self.botao_voltar.connect("clicked", self.voltar)
        
        self.texto_ip = gtk.Entry(15)
        self.texto_ip.connect("changed", self.escolher_ip)

        self.botao_receber = gtk.Button('Receber'.center(50))
        self.botao_receber.connect('clicked', self.receber_arquivo)

        self.texto_porta = gtk.Entry(5)
        self.texto_porta.connect("changed", self.escolher_porta)

        self.fixo = gtk.Fixed()
        self.fixo.put(self.label_instrucao, 30, 100)
        self.fixo.put(self.label_instrucao2, 30, 150)
        self.fixo.put(self.label_ip, 30, 200)
        self.fixo.put(self.label_porta, 30, 250)
        self.fixo.put(self.label_conexao, 30, 350)

        self.fixo.put(self.texto_ip, 310, 95)
        self.fixo.put(self.texto_porta, 310, 145)
        self.fixo.put(self.botao_receber, 120, 300)
        self.fixo.put(self.botao_voltar, 310, 420)

        self.janela.add(self.fixo)
        self.janela.show_all()

        self.nome_arquivo = ""
        self.ip = ""
        self.porta = ""

        self.IP_OK =  False
        

    def voltar(self, widget, data = None):
	from share import JanelaPrincipal
        self.janela.destroy()
	j = JanelaPrincipal()
        j.janela.show()
	
    def escolher_ip(self, widget, data=None):
        self.ip = self.texto_ip.get_text()        
        if self.ip == "":
            self.IP_OK = False
            self.label_ip.set_text("Nenhum IP escolhido.")
        elif self.ip == "localhost":
            self.IP_OK = True
            self.label_ip.set_text("Localhost escolhido.")
        elif '.' not in self.ip:
            self.IP_OK = False
            self.label_ip.set_text("Endereço IP inválido.") # Porque não tem pontos.
        elif '.' in self.ip:
            octetos = self.ip.split('.')
            if  len(octetos) < 4:
                self.IP_OK = False
                self.label_ip.set_text("Endereço IP inválido.") # Não tem 4 octetos
            else:
                for byte in octetos:
                    if not byte.isdigit():
                        self.IP_OK = False
                        self.label_ip.set_text("Endereço IP inválido.") # Algum octeto não é numero
                        break
                    elif byte.isdigit():
                        if int(byte) > 255 or '' in octetos:
                            self.IP_OK = False
                            self.label_ip.set_text("Endereço IP inválido.")
                            break
                        else:
                            self.IP_OK = True
                            self.label_ip.set_text("Endereço " + self.ip + " escolhido.")
    
    def escolher_porta(self, widget):
        "Valida a porta a ser escolhida."
        self.porta = str(self.texto_porta.get_text())
        if (self.porta== ""):
            self.label_porta.set_text("Nenhuma porta escolhida.")
        elif (not self.porta.isdigit()):
            self.label_porta.set_text("A porta deve conter somente números.")
        elif (self.porta.isdigit()):
            if (int(self.porta) <= 1024):
                self.label_porta.set_text("Número da porta muito baixo.")
            elif (int(self.porta) > 65535):
                self.label_porta.set_text("Número da porta muito alto.")
            else:
                self.label_porta.set_text("Porta "+ str(self.porta) +" escolhida.")

    def sair(self, widget, data=None):
	gtk.main_quit()

    def erro(self, mensagem):
        e = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, mensagem)
        e.run()
        e.destroy()

    def receber_arquivo(self, widget, data=None):
        if not self.IP_OK:
            self.erro("Endereço IP inválido.")
        else:
            self.porta = str(self.texto_porta.get_text())
            if (self.porta== ""):
                self.erro("Nenhuma porta escolhida.")
            elif (not self.porta.isdigit()):
                self.erro("A porta deve conter somente números.")
            elif (self.porta.isdigit()):
                if (int(self.porta) <= 1024):
                    self.erro("Número da porta muito baixo.")
                elif (int(self.porta) > 65535):
                    self.erro("Número da porta muito alto.")
                else:   
                    # Cria um File Chooser
                    self.fc = gtk.FileChooserDialog("Salvar...", None, gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
                    self.fc.set_default_response(gtk.RESPONSE_OK)
                    resposta = self.fc.run()
                    if resposta == gtk.RESPONSE_OK:
                        self.nome_arquivo = self.fc.get_filename()
                        self.fc.destroy()
                        aspas = '"'
                        self.nome_arquivo = aspas + self.nome_arquivo + aspas

                    ######
                    cmd = "nc %s %s > %s" %(self.ip, self.porta, self.nome_arquivo)
                    netcat = subprocess.Popen([cmd], stderr=subprocess.PIPE, shell=True)
                    saida, erro = netcat.communicate()
                    #####

                    if erro:
                        self.erro(erro)
                    else:
                        nome = self.nome_arquivo.split('/')[::-1][0].replace('"', '')
                        self.label_conexao.set_text("Arquivo " + nome + " salvo!")
                    
                    if resposta == gtk.RESPONSE_CANCEL:
                        # Destrói o File Chooser
                        self.fc.destroy()

