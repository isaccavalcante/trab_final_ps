#!/usr/bin/env python
#-*-coding: UTF-8-*-
import pygtk, gtk
import os
pygtk.require("2.0")

class JanelaArquivos:
    def __init__(self):
        self.janela = gtk.Window()
        self.janela.set_position(gtk.WIN_POS_CENTER)
        self.janela.set_size_request(480, 480)
        self.janela.set_title("share - Operações com arquivos")
        self.janela.set_resizable(False)
        try:
            self.janela.set_icon_from_file("icone.png")
        except:
            self.icone = self.janela.render_icon(gtk.STOCK_MISSING_IMAGE, gtk.ICON_SIZE_MENU)
            self.set_icon(self.icone)

        self.label_instrucao = gtk.Label("Escolha uma opção.")
        self.label_operacoes = gtk.Label("...")

        self.botao_cp = gtk.Button("Copiar".center(50))
        self.botao_cp.connect("clicked", self.cp)

        self.botao_mv = gtk.Button("Mover".center(50))
        self.botao_mv.connect("clicked", self.mv)


        self.botao_rm = gtk.Button("Remover".center(50))
        self.botao_rm.connect("clicked", self.rm)

        self.botao_voltar = gtk.Button("<Voltar".center(30))
        self.botao_voltar.connect("clicked", self.voltar)
        
        self.fixo = gtk.Fixed()
        self.fixo.put(self.label_instrucao, 30, 50)
        self.fixo.put(self.botao_cp, 120, 100)
        self.fixo.put(self.botao_mv, 120, 200)
        self.fixo.put(self.botao_rm, 120, 300)
        self.fixo.put(self.label_operacoes, 30, 370)
        self.fixo.put(self.botao_voltar, 300, 420)
       
        self.janela.add(self.fixo)
        self.janela.show_all()
    
    def voltar(self, widget, data=None):
        from share import JanelaPrincipal
        self.janela.hide()
        j = JanelaPrincipal()
        j.janela.show()


    def info(self, mensagem):
        info = gtk.MessageDialog(None, gtk.DIALOG_DESTROY_WITH_PARENT, gtk.MESSAGE_INFO, gtk.BUTTONS_OK, mensagem)
        info.run()
        info.destroy()

    def cp(self, widget, data=None):
        fc = gtk.FileChooserDialog("Escolher arquivo para copiar.", None, gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        fc.set_default_response(gtk.RESPONSE_OK)
        resposta = fc.run()
        if resposta == gtk.RESPONSE_OK:
            origem = fc.get_filename()
            fc.destroy()
                
            origem = '"' + origem + '"'
                
            fc2 = gtk.FileChooserDialog("Selecione pasta para salvar.", None, gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
            fc.set_default_response(gtk.RESPONSE_OK)
            resposta = fc2.run()

            if resposta == gtk.RESPONSE_OK:
                destino = fc2.get_filename()
                fc2.destroy()
                
                destino = "'" + destino + "'"

                #############################
    

                cmd = "cp -v %s %s 2> /dev/null > /dev/null" % (origem, destino)
                resultado = os.system(cmd)


                if (resultado == 0):
                    nome = origem.split('/')[::-1][0].replace('"', "")
                    pasta = origem.split('/')[::-1][1]
                    
                    msg = "Arquivo '%s' copiado para o diretório '%s'." % (nome, pasta)
                    self.label_operacoes.set_text(msg)

                    self.info("Arquivo copiado com sucesso!")

                #############################
            else:
                fc2.destroy()

        else:
            fc.destroy()

    def mv(self, widget, data=None):
            fc = gtk.FileChooserDialog("Selecione arquivo para mover", None, gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
            fc.set_default_response(gtk.RESPONSE_OK)
            resposta = fc.run()
            if resposta == gtk.RESPONSE_OK:
                origem = fc.get_filename()
                fc.destroy()
                    
                origem = '"' + origem + '"'
                    
                fc2 = gtk.FileChooserDialog("Selecione pasta para salvar.", None, gtk.FILE_CHOOSER_ACTION_SAVE, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_SAVE, gtk.RESPONSE_OK))
                fc.set_default_response(gtk.RESPONSE_OK)
                resposta = fc2.run()

                if resposta == gtk.RESPONSE_OK:
                    destino = fc2.get_filename()
                    fc2.destroy()
                    
                    destino = "'" + destino + "'"

                    #############################
                    cmd = "mv %s %s 2> /dev/null > /dev/null" % (origem, destino)
                    resultado = os.system(cmd)


                    if (resultado == 0):
                        nome = origem.split('/')[::-1][0].replace('"', "")
                        pasta = origem.split('/')[::-1][1]
                        
                        msg = "Arquivo '%s' movido para o diretório '%s'." % (nome, pasta)
                        self.label_operacoes.set_text(msg)

                        self.info("Arquivo movido com sucesso!")
                    #############################
                else:
                    fc2.destroy()

            else:
                fc.destroy()

    def rm(self, widget, data=None):
                fc = gtk.FileChooserDialog("Selecione arquivo para remover", None, gtk.FILE_CHOOSER_ACTION_OPEN, (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL, gtk.STOCK_OPEN, gtk.RESPONSE_OK))
                fc.set_default_response(gtk.RESPONSE_OK)
                resposta = fc.run()
                if resposta == gtk.RESPONSE_OK:
                    arquivo = fc.get_filename()
                    fc.destroy()
                        
                    arquivo = '"' + arquivo + '"'


                    dialog = gtk.MessageDialog(self.janela, gtk.DIALOG_MODAL,
                    gtk.MESSAGE_INFO, gtk.BUTTONS_YES_NO, "Tem certeza que deseja excluir o arquivo?")
                    dialog.set_title("Excluir")

                    resposta = dialog.run()
                    dialog.destroy()

                    if resposta == gtk.RESPONSE_YES:
                    ###############################
                        cmd = "rm %s 2> /dev/null > /dev/null" % (arquivo)
                        resultado = os.system(cmd)

                        if (resultado == 0):
                            nome = arquivo.split('/')[::-1][0].replace('"', "")
                            msg = "Arquivo '%s' removido." % (nome)
                            self.label_operacoes.set_text(msg)

                            self.info("Arquivo removido com sucesso!")

                    ##############################

                    #else:

                else:
                    fc.destroy()

