from datetime import date
from PySide6.QtWidgets import \
    QMainWindow, QLabel, QLineEdit, \
    QTextEdit, QPushButton, QVBoxLayout, \
    QWidget, QSizePolicy, QTableWidget, \
    QAbstractItemView, QTableWidgetItem, QComboBox
from PySide6.QtGui import \
    QIcon
from ..MsgInfo.msg_info import MsgInfo
from ...Infra.Repository.nota_repository import NotaRepository


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(450, 500)
        app_icon = QIcon('img/notas.png')
        self.setWindowIcon(app_icon)
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

        self.lbl_tabela_nota = QLabel('Notas Cadastradas:')
        self.tabela_nota = QTableWidget()
        self.tabela_nota.setColumnCount(4)
        self.tabela_nota.setHorizontalHeaderLabels([
            'Id', 'Nome', 'Texto', 'Data',
        ])
        self.tabela_nota.verticalHeader().setVisible(False)
        self.tabela_nota.setSelectionMode(QAbstractItemView.NoSelection)
        self.tabela_nota.setEditTriggers(QAbstractItemView.NoEditTriggers)

        self.btn_salvar = QPushButton('Salvar')

        self.btn_limpar = QPushButton('Limpar')
        self.btn_limpar.setEnabled(False)

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
        layout.addWidget(self.lbl_tabela_nota)
        layout.addWidget(self.tabela_nota)
        layout.addWidget(self.btn_salvar)
        layout.addWidget(self.btn_limpar)
        layout.addWidget(self.btn_atualizar)
        layout.addWidget(self.btn_remover)
        layout.addWidget(self.btn_voltar)

        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.container)
        self.container.setLayout(layout)

        self.txt_titulo_nota.textChanged.connect(self.on_change)
        self.txt_nota.textChanged.connect(self.on_change)

        self.btn_salvar.clicked.connect(self.salvar_nota)
        self.btn_limpar.clicked.connect(self.limpar_campos)
        self.btn_atualizar.clicked.connect(self.atualizar_nota)
        self.btn_remover.clicked.connect(self.remover_nota)
        self.tabela_nota.cellDoubleClicked.connect(self.carrega_dados)
        self.btn_voltar.clicked.connect(self.voltar)

        self.popular_table_nota()

    def on_change(self):
        if self.is_campos_vazios():
            self.btn_limpar.setEnabled(False)
        else:
            self.btn_limpar.setEnabled(True)

    def limpar_campos(self):
        for widget in self.container.children():
            if isinstance(widget, QLineEdit):
                widget.clear()
            elif isinstance(widget, QTextEdit):
                widget.clear()

    def carrega_dados(self, row):
        self.txt_id.setText(self.tabela_nota.item(row, 0).text())
        self.txt_titulo_nota.setText(self.tabela_nota.item(row, 1).text())
        self.txt_nota.setText(self.tabela_nota.item(row, 2).text())

        self.btn_atualizar.setVisible(True)
        self.btn_remover.setVisible(True)
        self.btn_salvar.setVisible(False)
        self.btn_voltar.setVisible(True)
        self.btn_limpar.setVisible(False)

    def voltar(self):
        self.limpar_campos()
        self.btn_salvar.setVisible(True)
        self.btn_remover.setVisible(False)
        self.btn_atualizar.setVisible(False)
        self.btn_voltar.setVisible(False)
        self.btn_limpar.setVisible(True)

    def get_nota(self):
        nota = {
            'nome': self.txt_titulo_nota.text(),
            'texto': self.txt_nota.toPlainText()
        }

        return nota

    def salvar_nota(self):
        if not self.is_campos_vazios():
            try:
                nota = self.get_nota()
                NotaRepository.insert(**nota)
                MsgInfo('info', 'Cadastro Realizado', 'Cadastro realizado com sucesso!')
                self.popular_table_nota()
                self.limpar_campos()
            except BaseException as e:
                print(e)
        else:
            MsgInfo('critical', 'Salvar Cliente', 'Não é aceito campos vazios!\nPreencha Novamente')

    def atualizar_nota(self):
        if not self.is_campos_vazios():
            try:
                nota_id = int(self.txt_id.text())
                nota = self.get_nota()
                NotaRepository.update(nota_id, **nota)
                MsgInfo('Info', 'Atualizar Nota', 'Nota atualizada com sucesso!')
                self.popular_table_nota()
                self.voltar()
            except BaseException as e:
                MsgInfo('critical', 'Atualizar Nota', 'Erro ao atualizar nota')
        else:
            MsgInfo('critical', 'Atualizar Nota', 'Não é aceito campos vazios!\nPreencha Novamente')

    def remover_nota(self):
        try:
            nota_id = int(self.txt_id.text())
            NotaRepository.delete(nota_id)
            MsgInfo('Info', 'Deletar Nota', 'Nota deletada com sucesso!')
            self.popular_table_nota()
            self.voltar()
        except BaseException as e:
            print(e)
            MsgInfo('critical', 'Deletar Nota', 'Erro ao deletar a nota')

    def popular_table_nota(self):
        self.tabela_nota.setRowCount(0)

        data = NotaRepository.select()
        print(data)

        self.tabela_nota.setRowCount(len(data))

        for linha, nota in enumerate(data):
            obj = [nota.id, nota.nome, nota.texto, date.strftime(nota.data_criacao, '%d/%m/%Y')]

            for coluna, valor in enumerate(obj):
                item = QTableWidgetItem(str(valor))
                self.tabela_nota.setItem(linha, coluna, item)

    def is_campos_vazios(self):
        return self.txt_titulo_nota.text() == '' \
            or self.txt_nota.toPlainText() == ''
