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
        secao_patins.setStyleSheet("color: black;")
        main_layout.addWidget(secao_patins)

        # Sessão de registro de aluguel
        secao_aluguel = self.criar_secao_aluguel()
        secao_aluguel.setStyleSheet("color: BLACK;")
        main_layout.addWidget(secao_aluguel)

        # Sessão de devolução de aluguel
        secao_devolucao = self.criar_secao_devolucao()
        secao_devolucao.setStyleSheet("color: black;")
        main_layout.addWidget(secao_devolucao)

       # Layout para os botões na parte inferior
        botoes_layout = QHBoxLayout()
        botoes_layout.setAlignment(Qt.AlignRight)  # Alinha o layout horizontal à direita

        # Cria layouts verticais para os pares de botões
        vertical_layout1 = QVBoxLayout()
        vertical_layout2 = QVBoxLayout()

        # Botão para cadastrar patins
        self.botao_cadastrar_patins = QPushButton("Cadastrar Patins")
        self.botao_cadastrar_patins.setStyleSheet("font-weight: bold; background: #90EE90;")
        self.botao_cadastrar_patins.setFixedSize(200, 50)
        self.botao_cadastrar_patins.clicked.connect(self.cadastrar_patins)
        vertical_layout1.addWidget(self.botao_cadastrar_patins)

        # Botão para registrar aluguel
        self.botao_registrar_aluguel = QPushButton("Registrar Aluguel")
        self.botao_registrar_aluguel.setStyleSheet("font-weight: bold; background: #90EE90;")
        self.botao_registrar_aluguel.setFixedSize(200, 50)
        self.botao_registrar_aluguel.clicked.connect(self.registrar_aluguel)
        vertical_layout1.addWidget(self.botao_registrar_aluguel)
        
        # Botão para visualizar registro de patins
        self.botao_ver_registro = QPushButton("Ver Registro de Patins")
        self.botao_ver_registro.setStyleSheet("font-weight: bold; background: #ADD8E6;")
        self.botao_ver_registro.setFixedSize(200, 50)
        self.botao_ver_registro.clicked.connect(self.mostrar_registro_patins)
        vertical_layout1.addWidget(self.botao_ver_registro)

        # Botão para finalizar aluguel
        self.botao_finalizar_aluguel = QPushButton("Finalizar Aluguel")
        self.botao_finalizar_aluguel.setStyleSheet("font-weight: bold; background: #FF6347;")
        self.botao_finalizar_aluguel.setFixedSize(200, 50)
        self.botao_finalizar_aluguel.clicked.connect(self.finalizar_aluguel)
        vertical_layout2.addWidget(self.botao_finalizar_aluguel)

        # Botão para fechar caixa
        self.botao_fechar_caixa = QPushButton("Fechar Caixa")
        self.botao_fechar_caixa.setStyleSheet("font-weight: bold; background: #FF6347;")
        self.botao_fechar_caixa.setFixedSize(200, 50)
        self.botao_fechar_caixa.clicked.connect(self.fechar_caixa)
        vertical_layout2.addWidget(self.botao_fechar_caixa)

        # Botão para salvar registro
        self.botao_salvar_registro = QPushButton("Salvar Registro")
        self.botao_salvar_registro.setStyleSheet("font-weight: bold; background: #ADD8E6;")
        self.botao_salvar_registro.setFixedSize(200, 50)
        self.botao_salvar_registro.clicked.connect(self.salvar_registro_patins)
        vertical_layout2.addWidget(self.botao_salvar_registro)

        # Adiciona os layouts verticais ao layout horizontal
        botoes_layout.addLayout(vertical_layout1)
        botoes_layout.addLayout(vertical_layout2)

        # Adiciona o layout horizontal ao layout principal
        main_layout.addLayout(botoes_layout)


    def criar_secao_patins(self):
        patins_group = QWidget()
        layout = QVBoxLayout(patins_group)

        titulo = QLabel("Cadastrar Patins:")
        layout.addWidget(titulo)

        form_layout = QFormLayout()
        self.input_numero_patins = QLineEdit()
        form_layout.addRow("Número do Patins:", self.input_numero_patins)

        layout.addLayout(form_layout)

        return patins_group

    def criar_secao_aluguel(self):
        aluguel_group = QWidget()
        layout = QVBoxLayout(aluguel_group)

        titulo = QLabel("Registro de Aluguel:")
        layout.addWidget(titulo)

        form_layout = QFormLayout()
        self.input_cpf = QLineEdit()
        self.input_numero_patins_alugar = QLineEdit()
        self.input_preco = QLineEdit()

        form_layout.addRow("CPF do Cliente:", self.input_cpf)
        form_layout.addRow("Número do Patins:", self.input_numero_patins_alugar)
        form_layout.addRow("Preço (R$):", self.input_preco)
        

        layout.addLayout(form_layout)

        return aluguel_group

    def criar_secao_devolucao(self):
        devolucao_group = QWidget()
        layout = QVBoxLayout(devolucao_group)

        titulo = QLabel("Devolução de Aluguel:")
        layout.addWidget(titulo)

        form_layout = QFormLayout()
        self.input_cpf_devolucao = QLineEdit()
        self.input_numero_patins_devolver = QLineEdit()
        self.input_dano = QComboBox()
        self.input_dano.addItems(["Sim", "Não"])
        self.input_valor_dano = QLineEdit()
        self.input_forma_pagamento = QComboBox()
        self.input_forma_pagamento.addItems(["Dinheiro", "Cartão"])

        form_layout.addRow("CPF do Cliente:", self.input_cpf_devolucao)
        form_layout.addRow("Número do Patins:", self.input_numero_patins_devolver)
        form_layout.addRow("Houve Dano?", self.input_dano)
        form_layout.addRow("Valor do Dano (R$):", self.input_valor_dano)
        form_layout.addRow("Forma de Pagamento:", self.input_forma_pagamento)

        layout.addLayout(form_layout)

        return devolucao_group

    def cadastrar_patins(self):
        numero = self.input_numero_patins.text()
        if numero:
            self.pdv.cadastrar_patins(numero)
            QMessageBox.information(self, "Sucesso", f"Patins {numero} cadastrado com sucesso.")
            self.input_numero_patins.clear()
        else:
            QMessageBox.warning(self, "Erro", "Por favor, insira o número do patins.")
    def Botao_voltarTabela():
        exit()
        
        
    def registrar_aluguel(self):
        cpf = self.input_cpf.text()
        numero = self.input_numero_patins_alugar.text()
        preco = self.input_preco.text()

        if not cpf or not numero or not preco:
            QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos.")
            return

        try:
            preco_float = float(preco)
            aluguel = self.pdv.registrar_aluguel(cpf, numero, preco_float)
            if aluguel:
                QMessageBox.information(self, "Sucesso", "Aluguel registrado com sucesso!")
                self.input_cpf.clear()
                self.input_numero_patins_alugar.clear()
                self.input_preco.clear()
            else:
                QMessageBox.warning(self, "Erro", "Patins não disponível para aluguel.")
        except ValueError:
            QMessageBox.warning(self, "Erro", "Preço inválido. Por favor, insira um número válido.")

    def finalizar_aluguel(self):
        cpf = self.input_cpf_devolucao.text()
        numero = self.input_numero_patins_devolver.text()
        dano = self.input_dano.currentText() == "Sim"
        valor_dano = self.input_valor_dano.text()
        forma_pagamento = self.input_forma_pagamento.currentText()

        if not cpf or not numero:
            QMessageBox.warning(self, "Erro", "Por favor, preencha todos os campos.")
            return

        try:
            valor_dano_float = float(valor_dano) if valor_dano else 0.0
            total = self.pdv.finalizar_aluguel(cpf, numero, dano, valor_dano_float, forma_pagamento)
            if total is not None:
                QMessageBox.information(self, "Sucesso", f"Aluguel finalizado. Total a pagar: R$ {total:.2f}")
                self.input_cpf_devolucao.clear()
                self.input_numero_patins_devolver.clear()
                self.input_valor_dano.clear()
            else:
                QMessageBox.warning(self, "Erro", "Aluguel não encontrado ou já finalizado.")
        except ValueError:
            QMessageBox.warning(self, "Erro", "Valor de dano inválido. Por favor, insira um número válido.")

    def fechar_caixa(self):
        total_dinheiro, total_cartao, erro = self.pdv.fechamento_caixa()
        if erro:
            QMessageBox.warning(self, "Erro", "Existem aluguéis não finalizados.")
        else:
            QMessageBox.information(self, "Fechamento de Caixa", f"Total em Dinheiro: R$ {total_dinheiro:.2f}\nTotal em Cartão: R$ {total_cartao:.2f}")
        
        exit()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    
    janela = JanelaPrincipal()
    janela.showMaximized()
    janela.show()
    sys.exit(app.exec_())
