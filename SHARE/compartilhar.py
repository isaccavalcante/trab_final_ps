#!/usr/bin/env python
#-*-coding: utf-8-*-
#Autor: Isac Cavalcante <isaccavalcante@alu.ufc.br>
import pygtk, gtk
import subprocess
from threading import Thread
import os
pygtk.require("2.0")

class JanelaCompartilhar:
    def __init__(self):
        self.janela = gtk.Window()
        self.janela.set_position(gtk.WIN_POS_CENTER)
        self.janela.set_size_request(480, 480)
        self.janela.set_title("share - Compartilhar um arquivo")
        self.janela.set_resizable(False)
        try:
            self.janela.set_icon_from_file("icon.png")
        except Exception:
            self.icone = self.janela.render_icon(gtk.STOCK_MISSING_IMAGE, gtk.ICON_SIZE_MENU)
            self.janela.set_icon(self.icone)

        
        def obter_ip():
            comando = subprocess.Popen(["ifconfig wlan0 | grep 'inet addr' | awk -F: '{print $2}' | awk '{print $1}' "], stdout=subprocess.PIPE, shell=True)
            ip, erro = comando.communicate()
            return ip
        msg = obter_ip()
        self.label_ip = gtk.Label("Seu IP na interface wlan0 é %s" % msg)
        
        self.label_instrucao = gtk.Label("Escolha um arquivo para compartilhar.")
        self.label_arquivo = gtk.Label("Nenhum arquivo escolhido.")
        self.label_instrucao2 = gtk.Label("Escolha uma porta entre 1025 e 65535:")
        self.label_porta =  gtk.Label("Nenhuma porta escolhida.")
        self.label_conexao = gtk.Label("")

        self.botao_cancelar = gtk.Button("Cancelar".center(30))
        self.botao_cancelar.connect("clicked", self.cancelar)
        
        self.botao_voltar = gtk.Button("<Voltar".center(30))
        self.botao_voltar.connect("clicked", self.voltar)
        
        self.botao_arquivo = gtk.Button('Escolher'.center(30))
        self.botao_arquivo.connect("clicked", self.escolher_arquivo)

        self.botao_compartilhar = gtk.Button('Compartilhar'.center(50))
        self.botao_compartilhar.connect('clicked', self.compartilhar)

        self.texto_porta = gtk.Entry(5)
        self.texto_porta.connect("changed", self.escolher_porta)

        self.fixo = gtk.Fixed()
        self.fixo.put(self.label_ip, 30, 50)
        self.fixo.put(self.label_instrucao, 30, 100)
        self.fixo.put(self.label_instrucao2, 30, 150)
        self.fixo.put(self.label_arquivo, 30, 200)
        self.fixo.put(self.label_porta, 30, 250)
        self.fixo.put(self.label_conexao, 30, 350)

        self.fixo.put(self.botao_arquivo, 300, 95)
        self.fixo.put(self.texto_porta, 300, 150)
        self.fixo.put(self.botao_compartilhar, 120, 300)
        self.fixo.put(self.botao_cancelar, 30, 420)
        self.fixo.put(self.botao_voltar, 300, 420)

        self.janela.add(self.fixo)
        self.janela.show_all()

        self.caminho = ""
        self.porta = ""
        self.nome_arquivo = ""
        self.lista_portas = []

    def passe(self, widget, data=None):
        resposta = 42

    def escolher_arquivo(self, widget):
        "Valida a escolha do arquivo."
        # Cria um File Chooser
        self.fc = gtk.FileChooserDialog("Escolher...", None, gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        self.fc.set_default_response(gtk.RESPONSE_OK)
        resposta = self.fc.run()
        if resposta == gtk.RESPONSE_OK:
            self.caminho =  self.fc.get_filename()
            # Nome do arquivo é o último índice do caminho quando dividido pelas barras presentes
            nome = self.caminho.split('/')[len(self.caminho.split('/'))-1]
            self.nome_arquivo = nome
            if len(nome) > 40:
                nome_curto = nome[:10]+ ' [...] ' + nome[len(nome)-20:]
                self.nome_arquivo = nome_curto
                self.label_arquivo.set_text('Arquivo "' + nome_curto +'" escolhido')
            else:
                self.label_arquivo.set_text('Arquivo "'+ nome + '" escolhido.')
            # Se caminho contiver espaços, é preciso fazer com que o shell o reconheça
            # Solução 1: adicionando barra invertida antes dos espaços
            '''
            if " " in self.caminho:
                caminho_espacos = self.caminho.split(" ")
                caminho = ''
                i = 0
                while i < len(caminho_espacos):
                    # Para terminar no penultimo, não adicionando depois do último indice.
                    if i == len(caminho_espacos)-1:
                        self.caminho += caminho_espacos[i]
                    else:
                        self.caminho += caminho_espacos[i] + "\ "
                    i+=1
            '''
            # Solução 2: adicionando aspas no início e fim do caminho
            if " " in self.caminho:
                aspas='"'
                self.caminho = aspas + self.caminho + aspas
        elif resposta == gtk.RESPONSE_CANCEL:
            self.caminho = ""
            self.label_arquivo.set_text('Nenhum arquivo escolhido.')
        # Destrói o File Chooser
        self.fc.destroy()

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
                self.label_porta.set_text("Porta "+ str(self.porta) +" escolhida. Clique em 'Compartilhar' para iniciar.")

    def cancelar(self, widget, data=None):
        if len(self.lista_portas) == 0:
            self.label_conexao.set_text("Não há compartilhamentos a serem cancelados.")
        else:
            for i in self.lista_portas:
                cmd = "fuser -k %s/tcp" % i
                os.system(cmd)
            self.lista_portas = []
            self.label_conexao.set_text("Compartilhamento cancelado.")

    def voltar(self, widget, data=None):
        from share import JanelaPrincipal
        self.janela.destroy()
	j = JanelaPrincipal()
        j.janela.show()

    def sair(self, widget, data=None):
        gtk.main_quit()

    def erro(self, mensagem):
        e = gtk.MessageDialog(None,  gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, mensagem)
        e.run()
        e.destroy()

    def compartilhar(self, widget, data=None):
        "Valida o arquivo e porta selecionados e fica escutando para enviar."
        if (self.caminho == ""):
            self.erro("Nenhum arquivo escolhido.")
        elif (self.porta == ""):
            self.erro("Nenhuma porta escolhida.")
        elif (not self.porta.isdigit()):
            self.erro("A porta deve conter somente números.")
        elif (self.porta.isdigit()):
            if (int(self.porta) <= 1024):
                self.erro("Número da porta muito baixo.")
            elif (int(self.porta) > 65535):
                self.erro("Número da porta muito alto.")
            else:
                # Libera a porta escolhida pelo usuário
                #cmd = "fuser -k %s/tcp 2> /dev/null > /dev/null" % self.porta
                #os.system(cmd)
                def thr():     
                    cmd = "nc -l -p %s < %s" % (self.porta, self.caminho)
                    #os.system(cmd)
                    netcat =  subprocess.Popen([cmd], stderr=subprocess.PIPE, shell=True)
                    saida, erro = netcat.communicate()

                t = Thread(target=thr)
                t.start()

                self.lista_portas.append(self.porta)

                # Mostra pro usuário que a conexão foi iniciada.
                texto = "Compartilhando arquivo '%s'\nna porta %s." % (self.nome_arquivo, self.porta)
                self.label_conexao.set_text(texto)
                
                
                #thread.start_new_thread(thr, ())
