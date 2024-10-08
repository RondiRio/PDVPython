# import sys
# from PyQt5.QtWidgets import (
#     QApplication, QMainWindow, QVBoxLayout, QWidget,
#     QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
#     QDialog, QMessageBox, QComboBox
# )
# from PyQt5.QtGui import * 
# from PyQt5.QtCore import *
# import os

# class CadastraProduto(QDialog):
#     def __init__(self, barcode=None):
#         super().__init__()
#         self.setWindowTitle("PDV - Cadastro Produto")
#         self.setGeometry(100, 100, 600, 600)

#         tela = QVBoxLayout()

#         self.NomeProduto = QLineEdit(self)
#         self.NomeProduto.setPlaceholderText("Nome")
#         tela.addWidget(self.NomeProduto)

#         self.PrecoProduto = QLineEdit(self)
#         self.PrecoProduto.setPlaceholderText("Preço")
#         tela.addWidget(self.PrecoProduto)

#         self.UnidadeProduto = QLineEdit(self)
#         self.UnidadeProduto.setPlaceholderText("Unidade")
#         tela.addWidget(self.UnidadeProduto)

#         self.CodigoProduto = QLineEdit(self)
#         self.CodigoProduto.setPlaceholderText("Código")

#         if barcode:
#             self.CodigoProduto.setText(barcode)
#         tela.addWidget(self.CodigoProduto)

#         Salvar = QPushButton("Salvar", self)
#         Salvar.setStyleSheet("background: red; color: white; font-size: 3em;")
#         Salvar.setFont(QFont('Arial', 15))
#         Salvar.clicked.connect(self.RegistraProduto)
#         tela.addWidget(Salvar)

#         self.setLayout(tela)

#     def RegistraProduto(self):
#         nome = self.NomeProduto.text()
#         unidade = self.UnidadeProduto.text()
#         preco = self.PrecoProduto.text()
#         codigo = self.CodigoProduto.text()
#         with open('itensRegistrados.txt', 'a') as file:
#             file.write(f"{codigo},{nome},{unidade},{preco}\n")
#         QMessageBox.information(self, "Sucesso", "Produto registrado.")
#         self.accept()


# class IndexPDV(QMainWindow):
#     def __init__(self):
#         super().__init__()

#         self.setWindowTitle("PDV - Chessman")
#         self.setGeometry(100, 100, 900, 900)

#         central_widget = QWidget()
#         self.setCentralWidget(central_widget)

#         main_layout = QVBoxLayout(central_widget)

#         self.entrarCodigoBarra = QLineEdit()
#         self.entrarCodigoBarra.setPlaceholderText("Digite o código de Barras.")
#         self.entrarCodigoBarra.setFixedSize(150, 30)
#         self.entrarCodigoBarra.returnPressed.connect(self.adiciona_item)
#         main_layout.addWidget(self.entrarCodigoBarra)

#         botaoAdicionar = QPushButton("Adicionar Produto", self)
#         botaoAdicionar.setStyleSheet("background: blue; color: white; font-size: 3em;")
#         botaoAdicionar.setFont(QFont('Arial', 15))
#         botaoAdicionar.clicked.connect(self.adiciona_item)
#         main_layout.addWidget(botaoAdicionar)

#         self.botaoBuscarByNome = QLineEdit(self)
#         self.botaoBuscarByNome.setPlaceholderText("Buscar pelo nome")
#         self.botaoBuscarByNome.returnPressed.connect(self.procurar_produto)
#         main_layout.addWidget(self.botaoBuscarByNome)

#         self.item_tabela = QTableWidget(self)
#         self.item_tabela.setColumnCount(6)
#         self.item_tabela.setHorizontalHeaderLabels(["Código", "Nome", "Unidade", "Quantidade", "Preço", "Total"])
#         main_layout.addWidget(self.item_tabela)

#         self.total_label = QLabel("Total: R$ 0.00", self)
#         font = QFont('Arial', 20)
#         self.total_label.setFont(font)
#         main_layout.addWidget(self.total_label)

#         botaoCancelarItem = QPushButton("Cancelar item", self)
#         botaoCancelarItem.setStyleSheet("background: red; color: white; font-size: 3em;")
#         botaoCancelarItem.setFont(QFont('Arial', 15))
#         botaoCancelarItem.clicked.connect(self.cancelar_item)
#         main_layout.addWidget(botaoCancelarItem)

#         botaoCancelarVenda = QPushButton("Cancelar venda", self)
#         botaoCancelarVenda.setStyleSheet("background: red; color: white; font-size: 3em;")
#         botaoCancelarVenda.setFont(QFont('Arial', 15))
#         botaoCancelarVenda.clicked.connect(self.cancelar_venda)
#         main_layout.addWidget(botaoCancelarVenda)

#         botaoFinalizarVenda = QPushButton("Finalizar venda", self)
#         botaoFinalizarVenda.setStyleSheet("background: green; color: white; font-size: 3em;")
#         botaoFinalizarVenda.setFont(QFont('Arial', 15))
#         botaoFinalizarVenda.clicked.connect(self.pagamento)
#         main_layout.addWidget(botaoFinalizarVenda)

#         self.itens = []
#         self.total = 0.0

#     def adiciona_item(self):
#         codigoBarras = self.entrarCodigoBarra.text()
#         produtoEncontrado = False

#         if os.path.exists("itensRegistrados.txt"):
#             with open('itensRegistrados.txt', "r") as file:
#                 for line in file:
#                     parts = line.strip().split(',')
#                     if len(parts) != 4:
#                         continue
#                     codigo, nome, unidade, preco = parts
#                     if codigo == codigoBarras:
#                         produtoEncontrado = True
#                         item = {"codigo": codigo, "nome": nome, "unidade": unidade, "quantidade": 1, "preco": float(preco)}
#                         self.itens.append(item)
#                         self.atualiza_tabela()
#                         self.atualiza_total()
#                         break
#         if not produtoEncontrado:
#             self.abrirCadastroProduto(codigoBarras)

#         self.entrarCodigoBarra.clear()

#     def atualiza_tabela(self):
#         self.item_tabela.setRowCount(len(self.itens))
#         for row, item in enumerate(self.itens):
#             self.item_tabela.setItem(row, 0, QTableWidgetItem(item["codigo"]))
#             self.item_tabela.setItem(row, 1, QTableWidgetItem(item["nome"]))
#             self.item_tabela.setItem(row, 2, QTableWidgetItem(item["unidade"]))
#             self.item_tabela.setItem(row, 3, QTableWidgetItem(str(item["quantidade"])))
#             self.item_tabela.setItem(row, 4, QTableWidgetItem(f'R$ {item["preco"]:.2f}'))
#             self.item_tabela.setItem(row, 5, QTableWidgetItem(f'R$ {item["quantidade"] * item["preco"]:.2f}'))

#     def atualiza_total(self):
#         self.total = sum(item["quantidade"] * item["preco"] for item in self.itens)
#         self.total_label.setText(f"Total: R$ {self.total:,.2f}".rjust(20))

#     def procurar_produto(self):
#         nome_produto = self.botaoBuscarByNome.text().strip().lower()
#         produtoEncontrado = False

#         if os.path.exists('itensRegistrados.txt'):
#             with open('itensRegistrados.txt', 'r') as file:
#                 for line in file:
#                     parts = line.strip().split(',')
#                     if len(parts) != 4:
#                         continue
#                     codigo, nome, unidade, preco = parts

#                     if nome.lower() == nome_produto:
#                         produtoEncontrado = True
#                         item = {"codigo": codigo, "nome": nome, "unidade": unidade, "quantidade": 1, "preco": float(preco)}

#                         self.itens.append(item)
#                         self.atualiza_tabela()
#                         self.atualiza_total()
#                         break
#         if not produtoEncontrado:
#             QMessageBox.warning(self, "Produto não encontrado", "Nenhum produto com esse nome.")

#         self.botaoBuscarByNome.clear()

#     def pagamento(self):
#         dialog = Metodo_pagamento(total=self.total)
#         dialog.exec_()

#     def cancelar_item(self):
#         if self.itens:
#             self.itens.pop()
#             self.atualiza_tabela()
#             self.atualiza_total()

#     def cancelar_venda(self):
#         self.itens = []
#         self.atualiza_tabela()
#         self.atualiza_total()

#     def fechar_venda(self):
#         pass

#     def abrirCadastroProduto(self, barcode=None):
#         dialog = CadastraProduto(barcode)
#         dialog.exec_()


# class Metodo_pagamento(QDialog):
#     def __init__(self, total):
#         super().__init__()
#         self.setWindowTitle("Formas de Pagamento")
#         self.setGeometry(100, 100, 300, 200)

#         layout = QVBoxLayout()

#         self.total_label = QLabel(f"Total da Compra: R$ {total:.2f}", self)
#         layout.addWidget(self.total_label)

#         instruction_label = QLabel("Escolha a Forma de Pagamento:", self)
#         layout.addWidget(instruction_label)

#         self.payment_combobox = QComboBox(self)
#         self.payment_combobox.addItems(["Cartão de Crédito", "Boleto", "Pix", "Transferência Bancária"])
#         layout.addWidget(self.payment_combobox)

#         self.payment_combobox.currentIndexChanged.connect(self.display_selected_payment)

#         self.message_label = QLabel("", self)
#         layout.addWidget(self.message_label)

#         self.setLayout(layout)

#     def display_selected_payment(self):
#         payment_method = self.payment_combobox.currentText()
#         if payment_method:
#             self.message_label.setText(f"Você selecionou: {payment_method}")
#             botaoFimVenda = QPushButton("Pagar")
#             botaoFimVenda.setStyleSheet("background: blue; color: white; font-size: 3em;")
#             botaoFimVenda.setFont(QFont('Arial', 15))
#             botaoFimVenda.clicked.connect(self.on_payment_button_clicked)
            
            
#             botaoVoltar = QPushButton("Pagar")
#             botaoVoltar.setStyleSheet("background: blue; color: white; font-size: 3em;")
#             botaoVoltar.setFont(QFont('Arial', 15))
#             botaoVoltar.clicked.connect(self.on_back_button_clicked)
            
#             self.layout().addWidget(botaoFimVenda)
#         else:
#             self.message_label.setText("")
#     def on_payment_button_clicked(self):
    
#         print("Pagamento realizado!")
#     def on_back_button_clicked(self):
#         pass

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     window = IndexPDV()
#     window.show()
#     sys.exit(app.exec_())

import sys
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QWidget,
    QLabel, QLineEdit, QPushButton, QTableWidget, QTableWidgetItem,
    QMessageBox, QComboBox, QHBoxLayout, QFormLayout, QDialog
)
from PyQt5.QtGui import QFont
from PyQt5.QtCore import Qt


# Classe representando um Patins
class Patins:
    def __init__(self, numero, disponivel=True):
        self.numero = numero
        self.disponivel = disponivel

    def alugar(self):
        self.disponivel = False

    def devolver(self):
        self.disponivel = True

# Classe representando um Cliente
class Cliente:
    def __init__(self, cpf):
        self.cpf = cpf

# Classe representando um Aluguel
class Aluguel:
    def __init__(self, cliente, patins, preco):
        self.cliente = cliente
        self.patins = patins
        self.preco = preco
        self.hora_inicio = datetime.now()
        self.hora_fim = None
        self.dano = False
        self.valor_dano = 0.0
        self.forma_pagamento = None

    def finalizar_aluguel(self, dano=False, valor_dano=0.0):
        self.hora_fim = datetime.now()
        self.dano = dano
        self.valor_dano = valor_dano

    def registrar_pagamento(self, forma_pagamento):
        self.forma_pagamento = forma_pagamento

    def calcular_total(self):
        return self.preco + self.valor_dano

# Classe representando o sistema de PDV
class PDV:
    def __init__(self):
        self.patins = []
        self.alugueis = []

    def cadastrar_patins(self, numero):
        patins = Patins(numero)
        self.patins.append(patins)

    def verificar_disponibilidade(self, numero):
        for patins in self.patins:
            if patins.numero == numero and patins.disponivel:
                return patins
        return None

    def registrar_aluguel(self, cpf, numero, preco):
        cliente = Cliente(cpf)
        patins = self.verificar_disponibilidade(numero)
        if patins:
            patins.alugar()
            aluguel = Aluguel(cliente, patins, preco)
            self.alugueis.append(aluguel)
            return aluguel
        else:
            return None

    def finalizar_aluguel(self, cpf, numero, dano=False, valor_dano=0.0, forma_pagamento="Dinheiro"):
        for aluguel in self.alugueis:
            if aluguel.cliente.cpf == cpf and aluguel.patins.numero == numero and not aluguel.hora_fim:
                aluguel.finalizar_aluguel(dano, valor_dano)
                aluguel.registrar_pagamento(forma_pagamento)
                aluguel.patins.devolver()
                return aluguel.calcular_total()
        return None

    def fechamento_caixa(self):
        if any(aluguel.hora_fim is None for aluguel in self.alugueis):
            return None, None, True  # Retorna um sinal de erro se houver aluguel aberto
        total_dinheiro = sum(a.calcular_total() for a in self.alugueis if a.forma_pagamento == "Dinheiro")
        total_cartao = sum(a.calcular_total() for a in self.alugueis if a.forma_pagamento == "Cartão")
        return total_dinheiro, total_cartao, False

    def buscar_aluguel_por_cpf(self, cpf):
        for aluguel in reversed(self.alugueis):
            if aluguel.cliente.cpf == cpf and aluguel.hora_fim is None:
                return aluguel
        return None

# Classe principal da janela do sistema
class JanelaPrincipal(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("LocaPatins - Aluguel de Patins")
        self.setGeometry(100, 100, 1080, 1080)
        self.pdv = PDV()
        self.initUI()

    def salvar_registro_patins(self):
        try:
            with open("registro_de_patins.txt", "w") as arquivo:
                arquivo.write("Registro de Patins\n")
                arquivo.write("===================\n")
                for aluguel in self.pdv.alugueis:
                    status = "Ativo" if aluguel.hora_fim is None else "Finalizado"
                    arquivo.write(f"Patins {aluguel.patins.numero} - Cliente {aluguel.cliente.cpf} - Status: {status}\n")
                QMessageBox.information(self, "Sucesso", "Dados exportados para registro_de_patins.txt com sucesso.")
        except Exception as e:
            QMessageBox.warning(self, "Erro", f"Erro ao salvar arquivo: {str(e)}")

    def mostrar_registro_patins(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Registro de Patins")
        dialog.setGeometry(100, 100, 600, 400)

        tabela = QTableWidget()
        tabela.setRowCount(len(self.pdv.alugueis))
        tabela.setColumnCount(4)  # Adicionei uma coluna extra para a hora de início/fechamento
        tabela.setHorizontalHeaderLabels(["Número do Patins", "CPF do Cliente", "Status do Aluguel", "Horário"])

        # Preenche a tabela com os dados dos aluguéis
        for row, aluguel in enumerate(self.pdv.alugueis):
            tabela.setItem(row, 0, QTableWidgetItem(str(aluguel.patins.numero)))
            tabela.setItem(row, 1, QTableWidgetItem(aluguel.cliente.cpf))
            
            status = "Ativo" if aluguel.hora_fim is None else "Finalizado"
            tabela.setItem(row, 2, QTableWidgetItem(status))

            if aluguel.hora_fim is None:  # Se o aluguel ainda está ativo
                tabela.setItem(row, 3, QTableWidgetItem(f"Início: {aluguel.hora_inicio.strftime('%H:%M:%S')}"))
            else:  # Se o aluguel foi finalizado
                tabela.setItem(row, 3, QTableWidgetItem(f"Início: {aluguel.hora_inicio.strftime('%H:%M:%S')}\nFim: {aluguel.hora_fim.strftime('%H:%M:%S')}"))

        # Layout para o botão de salvar registro
        botoes_layout = QHBoxLayout()

        # Botão para voltar
        self.botaoVoltar = QPushButton("Voltar")
        self.botaoVoltar.setStyleSheet("font-weight: bold; background: #ADD8E6;")
        self.botaoVoltar.clicked.connect(dialog.accept)  # Função de fechar o diálogo
        botoes_layout.addWidget(self.botaoVoltar)

        # Layout principal da janela de diálogo
        layout = QVBoxLayout()
        layout.addWidget(tabela)
        layout.addLayout(botoes_layout)  # Adicione os botões ao layout principal
        dialog.setLayout(layout)

        dialog.exec_()


    def initUI(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # Sessão para cadastrar Patins
        secao_patins = self.criar_secao_patins()
        main_layout.addWidget(secao_patins)

        # Sessão de registro de aluguel
        secao_aluguel = self.criar_secao_aluguel()
        main_layout.addWidget(secao_aluguel)

        # Sessão de devolução de aluguel
        secao_devolucao = self.criar_secao_devolucao()
        main_layout.addWidget(secao_devolucao)

        # Botões na parte inferior
        self.botao_cadastrar_patins = QPushButton("Cadastrar Patins")
        self.botao_registrar_aluguel = QPushButton("Registrar Aluguel")
        self.botao_finalizar_aluguel = QPushButton("Finalizar Aluguel")
        self.botao_registro_patins = QPushButton("Ver Registro de Patins")
        self.botao_fechamento_caixa = QPushButton("Fechamento de Caixa")

        # Aplicação de estilização dos botões
        estilo_botao = """
            QPushButton {
                background-color: #4CAF50;
                color: white;
                font-weight: bold;
                padding: 10px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """
        self.botao_cadastrar_patins.setStyleSheet(estilo_botao)
        self.botao_registrar_aluguel.setStyleSheet(estilo_botao)
        self.botao_finalizar_aluguel.setStyleSheet(estilo_botao)
        self.botao_registro_patins.setStyleSheet(estilo_botao)
        self.botao_fechamento_caixa.setStyleSheet(estilo_botao)

        # Conexão dos botões com suas funções
        self.botao_cadastrar_patins.clicked.connect(self.cadastrar_patins)
        self.botao_registrar_aluguel.clicked.connect(self.registrar_aluguel)
        self.botao_finalizar_aluguel.clicked.connect(self.finalizar_aluguel)
        self.botao_registro_patins.clicked.connect(self.mostrar_registro_patins)
        self.botao_fechamento_caixa.clicked.connect(self.fechamento_caixa)

        main_layout.addWidget(self.botao_cadastrar_patins)
        main_layout.addWidget(self.botao_registrar_aluguel)
        main_layout.addWidget(self.botao_finalizar_aluguel)
        main_layout.addWidget(self.botao_registro_patins)
        main_layout.addWidget(self.botao_fechamento_caixa)

    # Método para criar a seção de cadastro de patins
    def criar_secao_patins(self):
        secao_patins = QWidget()
        layout = QFormLayout(secao_patins)

        self.input_numero_patins = QLineEdit()
        layout.addRow("Número do Patins:", self.input_numero_patins)

        return secao_patins

    # Método para criar a seção de registro de aluguel
    def criar_secao_aluguel(self):
        secao_aluguel = QWidget()
        layout = QFormLayout(secao_aluguel)

        self.input_cpf = QLineEdit()
        self.input_numero_patins_alugar = QLineEdit()
        self.input_preco = QLineEdit()

        layout.addRow("CPF do Cliente:", self.input_cpf)
        layout.addRow("Número do Patins para Alugar:", self.input_numero_patins_alugar)
        layout.addRow("Preço do Aluguel:", self.input_preco)

        return secao_aluguel

    # Método para criar a seção de devolução de aluguel
    def criar_secao_devolucao(self):
        secao_devolucao = QWidget()
        layout = QFormLayout(secao_devolucao)

        self.input_cpf_devolucao = QLineEdit()
        self.input_numero_patins_devolver = QLineEdit()
        self.input_valor_dano = QLineEdit()

        self.combo_dano = QComboBox()
        self.combo_dano.addItems(["Não", "Sim"])

        self.combo_forma_pagamento = QComboBox()
        self.combo_forma_pagamento.addItems(["Dinheiro", "Cartão"])

        layout.addRow("CPF do Cliente (Devolução):", self.input_cpf_devolucao)
        layout.addRow("Número do Patins para Devolver:", self.input_numero_patins_devolver)
        layout.addRow("Houve Dano?", self.combo_dano)
        layout.addRow("Valor do Dano:", self.input_valor_dano)
        layout.addRow("Forma de Pagamento:", self.combo_forma_pagamento)

        # Conectar evento de mudança de texto para preencher automaticamente o aluguel
        self.input_cpf_devolucao.textChanged.connect(self.on_cpf_devolucao_changed)

        return secao_devolucao

    def cadastrar_patins(self):
        numero = self.input_numero_patins.text()
        if numero:
            self.pdv.cadastrar_patins(numero)
            QMessageBox.information(self, "Sucesso", f"Patins número {numero} cadastrado com sucesso!")
            self.input_numero_patins.clear()
        else:
            QMessageBox.warning(self, "Erro", "Número do patins não pode ser vazio.")

    def registrar_aluguel(self):
        cpf = self.input_cpf.text()
        numero = self.input_numero_patins_alugar.text()
        preco = self.input_preco.text()

        if cpf and numero and preco:
            try:
                preco = float(preco)
                aluguel = self.pdv.registrar_aluguel(cpf, numero, preco)
                if aluguel:
                    QMessageBox.information(self, "Sucesso", f"Aluguel do patins número {numero} registrado com sucesso!")
                    self.input_cpf.clear()
                    self.input_numero_patins_alugar.clear()
                    self.input_preco.clear()
                else:
                    QMessageBox.warning(self, "Erro", f"Patins número {numero} não está disponível.")
            except ValueError:
                QMessageBox.warning(self, "Erro", "Preço inválido.")
        else:
            QMessageBox.warning(self, "Erro", "Todos os campos devem ser preenchidos.")

    def on_cpf_devolucao_changed(self):
        cpf = self.input_cpf_devolucao.text()
        aluguel = self.pdv.buscar_aluguel_por_cpf(cpf)
        if aluguel:
            self.input_numero_patins_devolver.setText(str(aluguel.patins.numero))
            self.input_valor_dano.setText(str(aluguel.valor_dano))

    def finalizar_aluguel(self):
        cpf = self.input_cpf_devolucao.text()
        numero = self.input_numero_patins_devolver.text()
        dano = self.combo_dano.currentText() == "Sim"
        valor_dano = self.input_valor_dano.text()

        # Corrigir para tratar o valor do dano vazio
        valor_dano_float = 0.0 if not valor_dano or not dano else float(valor_dano)
        forma_pagamento = self.combo_forma_pagamento.currentText()

        if cpf and numero:
            total = self.pdv.finalizar_aluguel(cpf, numero, dano, valor_dano_float, forma_pagamento)
            if total is not None:
                QMessageBox.information(self, "Sucesso", f"Aluguel do patins número {numero} finalizado.\nTotal: R${total:.2f}")
                self.input_cpf_devolucao.clear()
                self.input_numero_patins_devolver.clear()
                self.input_valor_dano.clear()
            else:
                QMessageBox.warning(self, "Erro", "Aluguel não encontrado ou já finalizado.")
        else:
            QMessageBox.warning(self, "Erro", "CPF e Número do Patins devem ser preenchidos.")

    def fechamento_caixa(self):
        total_dinheiro, total_cartao, erro = self.pdv.fechamento_caixa()
        if erro:
            QMessageBox.warning(self, "Erro", "Existem aluguéis em aberto, finalize-os antes de fechar o caixa.")
        else:
            QMessageBox.information(self, "Fechamento de Caixa", f"Total em Dinheiro: R${total_dinheiro:.2f}\nTotal em Cartão: R${total_cartao:.2f}")

# Código principal para iniciar a aplicação
if __name__ == '__main__':
    app = QApplication(sys.argv)
    janela = JanelaPrincipal()
    janela.show()
    sys.exit(app.exec_())
