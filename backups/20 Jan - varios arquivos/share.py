#!/usr/bin/env python
#-*-coding: utf-8-*-
#Autor: Isac Cavalcante <isaccavalcante@alu.ufc.br>
import pygtk, gtk
import subprocess
pygtk.require("2.0")

class JanelaPrincipal:
    def __init__(self):
        self.janela = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.janela.set_position(gtk.WIN_POS_CENTER)
        self.janela.set_size_request(480, 480)
        self.janela.set_title("share")
        self.janela.set_resizable(False)
        try:
            self.janela.set_icon_from_file("icone.png")
        except Exception:
            self.icone = self.janela.render_icon(gtk.STOCK_MISSING_IMAGE, gtk.ICON_SIZE_MENU)
            self.janela.set_icon(self.icone)


        self.botao_servir = gtk.Button("COMPARTILHAR UM ARQUIVO")
        self.botao_servir.connect("clicked", self.compartilhar)

        self.botao_receber = gtk.Button("RECEBER UM ARQUIVO")
        self.botao_receber.connect("clicked", self.receber)

        self.botao_ssh = gtk.Button("LOGIN COM SSH")
        self.botao_ssh.connect("clicked", self.ssh)
        
        self.botao_ajuda = gtk.Button("AJUDA")
        self.botao_ajuda.connect("clicked", self.ajuda )

        self.botao_sobre = gtk.Button("SOBRE")
        self.botao_sobre.connect("clicked", self.sobre)

        self.botao_sair = gtk.Button("SAIR")
        self.botao_sair.connect("clicked", self.sair)

        self.caixa = gtk.VBox()

        self.caixa.pack_start(self.botao_servir)
        self.caixa.pack_start(self.botao_receber)
        self.caixa.pack_start(self.botao_ajuda)
        self.caixa.pack_start(self.botao_sobre)
        self.caixa.pack_start(self.botao_sair)

        self.janela.add(self.caixa)
        self.janela.show_all()
        self.janela.connect("destroy", self.sair)

    def main(self):
        gtk.main()

    def sair(self, widget, data=None):
        gtk.main_quit()

    def compartilhar(self, widget, data=None):
        from compartilhar import JanelaCompartilhar
	self.janela.hide()
	j = JanelaCompartilhar()
	j.janela.show()

    def receber(self, widget, data=None):
        from receber import JanelaReceber
	self.janela.hide()        
	j = JanelaReceber()
	j.janela.show()

    def ssh(self, widget, data=None):
        self.janela.hidde()
        jssh = JanelaSSH
        jssh.janela.show()

    def ajuda(self, widget, data=None):
        a = gtk.Dialog("share - Ajuda", None, gtk.DIALOG_DESTROY_WITH_PARENT, (gtk.STOCK_OK, gtk.RESPONSE_ACCEPT))
        label = gtk.Label("\n\n\n" + "Nós quem precisamos de ajuda.".center(70) + "\n\n\n")
        a.vbox.pack_start(label)
        label.show()
        a.run()
        a.destroy()

    def sobre(self, widget):
        s = gtk.AboutDialog()
        s.set_program_name = "Share"
        s.set_version("v0.1")
        s.set_copyright("GPL v3 ou superior")
        s.set_comments("\nPrograma que usa a ferramenta netcat para o compartilhamento simples de arquivos em rede local.\n\nTrabalho para a disciplina de Programação de Scripts\n\n Universidade Federal do Ceará\nCurso: Redes de Computadores\n 4º Semestre\n\nAutores:\nIsac Cavalcante, Maria Micaele, Tiago Nascimento")
        s.set_website("www.algumsite.com")
        s.run()
        s.destroy()

if __name__== "__main__":
    try:
        j = JanelaPrincipal()
        j.main()
    except KeyboardInterrupt:
        print "\nCancelado pelo usuário."
