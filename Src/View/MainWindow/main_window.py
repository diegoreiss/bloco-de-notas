from PySide6.QtWidgets import \
    QMainWindow, QLabel, QLineEdit, \
    QTextEdit, QPushButton, QVBoxLayout, \
    QWidget, QSizePolicy, QTableWidget, \
    QAbstractItemView, QTableWidgetItem, QComboBox
from PySide6.QtGui import QColor

from Src.Model.nota import Nota
from Src.Controller.nota_DAO import NotaDAO
from Src.View.MsgInfo.msg_info import MsgInfo


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(450, 500)
        self.setWindowTitle('Notas')

        self.lbl_id = QLabel('Id')
        self.txt_id = QLineEdit()
        self.txt_id.setFixedWidth(50)
        self.lbl_id.setVisible(False)
        self.txt_id.setVisible(False)

        self.lbl_titulo_nota = QLabel('Titulo da nota:')
        self.txt_titulo_nota = QLineEdit()

        self.lbl_nota = QLabel('Nota:')
        self.txt_nota = QTextEdit()

        self.lbl_categoria = QLabel('Categoria:')
        self.cb_categoria = QComboBox()
        self.cb_categoria.addItems(self.pegar_categorias())

        self.lbl_tabela_nota = QLabel('Notas Cadastradas:')
        self.tabela_nota = QTableWidget()
        self.tabela_nota.setColumnCount(5)
        self.tabela_nota.setHorizontalHeaderLabels([
            'Id', 'Nome', 'Data', 'Texto', 'Last Update'
        ])
        self.tabela_nota.setSelectionMode(QAbstractItemView.NoSelection)
        self.tabela_nota.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.btn_salvar = QPushButton('Salvar')

        self.btn_atualizar = QPushButton('Atualizar')
        self.btn_atualizar.setVisible(False)

        self.btn_remover = QPushButton('Remover')
        self.btn_remover.setVisible(False)

        self.btn_voltar = QPushButton('Voltar')
        self.btn_voltar.setVisible(False)

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_id)
        layout.addWidget(self.txt_id)
        layout.addWidget(self.lbl_titulo_nota)
        layout.addWidget(self.txt_titulo_nota)
        layout.addWidget(self.lbl_nota)
        layout.addWidget(self.txt_nota)
        layout.addWidget(self.lbl_categoria)
        layout.addWidget(self.cb_categoria)
        layout.addWidget(self.lbl_tabela_nota)
        layout.addWidget(self.tabela_nota)
        layout.addWidget(self.btn_salvar)
        layout.addWidget(self.btn_atualizar)
        layout.addWidget(self.btn_remover)
        layout.addWidget(self.btn_voltar)

        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.container)
        self.container.setLayout(layout)

        self.popular_table_nota()

        self.txt_titulo_nota.textChanged.connect(self.on_change)
        self.txt_nota.textChanged.connect(self.on_change)

        self.btn_salvar.clicked.connect(self.salvar_nota)
        self.btn_atualizar.clicked.connect(self.atualizar_nota)
        self.btn_remover.clicked.connect(self.remover_nota)
        self.tabela_nota.cellDoubleClicked.connect(self.carrega_dados)
        self.btn_voltar.clicked.connect(self.voltar)

        self.nota = Nota()

    def on_change(self):
        self.nota.id = self.txt_id.text()
        self.nota.nome = self.txt_titulo_nota.text()
        self.nota.texto = self.txt_nota.toPlainText()

        print(self.nota.__dict__)

    def limpar_campos(self):
        for widget in self.container.children():
            if isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QTextEdit):
                widget.clear()

    def carrega_dados(self, row, column):
        self.txt_id.setText(self.tabela_nota.item(row, 0).text())
        self.txt_titulo_nota.setText(self.tabela_nota.item(row, 1).text())
        self.txt_nota.setText(self.tabela_nota.item(row, 3).text())

        self.btn_atualizar.setVisible(True)
        self.btn_remover.setVisible(True)
        self.btn_salvar.setVisible(False)
        self.btn_voltar.setVisible(True)

    def voltar(self):
        self.limpar_campos()
        self.btn_salvar.setVisible(True)
        self.btn_remover.setVisible(False)
        self.btn_atualizar.setVisible(False)
        self.btn_voltar.setVisible(False)

    def salvar_nota(self):
        nota_dao = NotaDAO()

        retorno = nota_dao.registrar_nota(self.nota)

        if retorno == 'inserted':
            MsgInfo('info', 'Cadastro Realizado', 'Cadastro realizado com sucesso!')
            self.popular_table_nota()
            self.limpar_campos()
        else:
            print(retorno)

    def atualizar_nota(self):
        self.nota.id = int(self.nota.id)
        nota_dao = NotaDAO()

        retorno = nota_dao.atualizar_nota(self.nota)

        if retorno == 'updated':
            MsgInfo('info', 'Atualizar', 'A nota foi atualizada com sucesso!')
            self.popular_table_nota()
            self.limpar_campos()
            self.voltar()
        else:
            print(retorno)

    def remover_nota(self):
        self.nota.id = int(self.nota.id)

        nota_dao = NotaDAO()

        retorno = nota_dao.remover_nota(self.nota)

        if retorno == 'deleted':
            MsgInfo('info', 'Nota Deletada', 'Nota removida com sucesso!')
            self.popular_table_nota()
            self.voltar()
        else:
            print(retorno)

    def pegar_categorias(self):
        nota_dao = NotaDAO()

        categorias = ['Não Informado']

        categorias += [j for i in nota_dao.consultar_todas_categorias() for j in i]

        return categorias

    def popular_table_nota(self):
        self.tabela_nota.setRowCount(0)

        nota_dao = NotaDAO()
        lista_notas = nota_dao.consultar_todas_notas()

        self.tabela_nota.setRowCount(len(lista_notas))

        for linha, nota in enumerate(lista_notas):
            for coluna, valor in enumerate(nota):
                self.tabela_nota.setItem(linha, coluna, QTableWidgetItem(str(valor)))

