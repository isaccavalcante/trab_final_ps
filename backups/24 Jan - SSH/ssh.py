#!/usr/bin/env python
#-*-coding: utf-8-*-
#Autor: Isac Cavalcante <isaccavalcante@alu.ufc.br>
import pygtk, gtk
pygtk.require("2.0")
import paramiko
import socket

class JanelaSSH:
    def __init__(self):
        self.janela = gtk.Window()
        self.janela.set_position(gtk.WIN_POS_CENTER)
        self.janela.set_size_request(480, 480)
        self.janela.set_title("share - ssh")
        self.janela.set_resizable(False)
        try:
            self.janela.set_icon_from_file("icone.png")
        except Exception:
            self.icone = self.janela.render_icon(gtk.STOCK_MISSING_IMAGE, gtk.ICON_SIZE_MENU)
            self.janela.set_icon(self.icone)
        self.ip = ""
        self.login = ""
        self.senha = ""

        # INICIO FIXO 1
        self.label_ip = gtk.Label("Digite o endereço do host remoto: ")
        self.label_login = gtk.Label("Login: ")
        self.label_senha = gtk.Label("Senha: ")

        self.texto_ip = gtk.Entry()
        self.texto_login = gtk.Entry()
        self.texto_senha = gtk.Entry()
        self.texto_senha.set_visibility(False)
        
        self.botao_conectar = gtk.Button('Conectar'.center(50))
        self.botao_conectar.connect('clicked', self.conectar)
        self.botao_voltar = gtk.Button('<Voltar'.center(30))
        self.botao_voltar.connect('clicked', self.voltar)

        self.fixo = gtk.Fixed()
        self.fixo.put(self.label_ip, 30, 100)
        self.fixo.put(self.label_login, 30, 150)
        self.fixo.put(self.label_senha, 30, 200)
        self.fixo.put(self.texto_ip, 270, 95)
        self.fixo.put(self.texto_login, 270, 145)
        self.fixo.put(self.texto_senha, 270, 195)
        self.fixo.put(self.botao_conectar, 120, 300)
        self.fixo.put(self.botao_voltar, 300, 420)
        # FIM FIXO 1

        self.janela.add(self.fixo)
        self.janela.show_all()


    def main(self):
        gtk.main()
    
    def executar(self, widget, data=None):
        return 

    def voltar(self, widget, data=None):
        from share import JanelaPrincipal
        self.janela.destroy()
        j = JanelaPrincipal()
        j.janela.show()

    def erro(self, mensagem):
        e = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_ERROR, gtk.BUTTONS_CLOSE, mensagem)
        e.run()
        e.destroy()

    def info(self, mensagem):
        i = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, mensagem)
        i.run()
        i.destroy()

    def conectar(self, widget, data=None):
        self.ip = self.texto_ip.get_text()
        self.login = self.texto_login.get_text()
        self.senha = self.texto_senha.get_text()
        if self.ip == "":
            self.erro("Nenhum host escolhido.")
        elif self.login == "":
            self.erro("Login não informado.")
        elif self.senha == "":
            self.erro("Senha não informada.")
        else:
            try:
                self.ssh = paramiko.SSHClient()
                self.ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
                self.ssh.connect(self.ip, username=self.login, password=self.senha)
                self.logar()
                self.info("Login realizado com sucesso!")
            except paramiko.AuthenticationException, msg:
                self.erro(msg[0])
            except socket.gaierror, msg:
                self.erro(msg[1])
            except socket.error, msg:
                self.erro(msg[1])

    def logar(self):
        self.janela.set_title("share - %s@%s" % (self.login, self.ip))
        self.janela.remove(self.fixo)
        self.label_info = gtk.Label('Logado em "%s" como usuário "%s". ' % (self.ip, self.login))
        self.label_comando = gtk.Label("Digite um comando: ")
        self.texto_comando = gtk.Entry()

        self.botao_executar = gtk.Button("Executar")
        self.botao_executar.connect("clicked", self.executar)

        self.texto = gtk.TextView()
        self.texto.set_editable(False)
        self.texto.set_cursor_visible(False)
        self.buffer_texto = self.texto.get_buffer()

        self.janela_scroll = gtk.ScrolledWindow()
        self.janela_scroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.janela_scroll.set_border_width(10)

        self.janela_scroll.add_with_viewport(self.texto)

        self.caixa1 = gtk.VBox()
        self.caixa1.pack_start(self.label_info)
        
        self.caixa2 = gtk.HBox()
        #self.caixa2.set_border_width(10)
        #self.caixa2.pack_start(self.caixa1)
        self.caixa3.pack_star(self.caixa1)
        self.caixa2.pack_start(self.label_comando)
        self.caixa2.pack_start(self.texto_comando, False, False, 0)
        self.caixa2.pack_start(self.botao_executar, False, False, 0)

        self.caixa3 = gtk.VBox(False, 10)
        self.caixa3.pack_start(self.caixa2)
        self.caixa3.pack_start(self.janela_scroll)

        #self.fixo2 = gtk.Fixed()
        #self.fixo2.put(self.label_info, 30, 35)
        #self.fixo2.put(self.label_comando, 30, 75)
        #self.fixo2.put(self.texto_comando, 305, 70)
        #self.fixo2.put(self.janela_scroll, 5, 200)
        #self.fixo2.put(self.botao_executar, 320, 100)

        self.janela.add(self.caixa3)
        self.janela.show_all()

    def executar(self, widget, data=None):
        comando = self.texto_comando.get_text()
        stdin, stdout, stderr = self.ssh.exec_command(comando)
        out, err  = stdout.readlines(), stderr.readlines()
        x = ""
        print "Saida: "
        print out
        print "Saída Formatada 1"
        for i in out:
            x += str(i)
        print x
        self.buffer_texto.set_text(x)




if __name__ == '__main__':
    try:
        j = JanelaSSH()
        j.main()
    except KeyboardInterrupt:
        print "Cancelado"
