from PySide6.QtWidgets import \
    QMainWindow, QLabel, QLineEdit, \
    QTextEdit, QPushButton, QVBoxLayout, \
    QWidget, QSizePolicy

from src.model.nota import Nota


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setMinimumSize(500, 900)
        self.setWindowTitle('Notas')

        self.lbl_id = QLabel('Id')
        self.txt_id = QLineEdit()

        self.lbl_titulo_nota = QLabel('Titulo da nota')
        self.txt_titulo_nota = QLineEdit()

        self.lbl_nota = QLabel('Nota')
        self.txt_nota = QTextEdit()

        self.btn_salvar = QPushButton('Salvar')

        layout = QVBoxLayout()
        layout.addWidget(self.lbl_id)
        layout.addWidget(self.txt_id)
        layout.addWidget(self.lbl_titulo_nota)
        layout.addWidget(self.txt_titulo_nota)
        layout.addWidget(self.lbl_nota)
        layout.addWidget(self.txt_nota)
        layout.addWidget(self.btn_salvar)

        self.container = QWidget()
        self.container.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.setCentralWidget(self.container)
        self.container.setLayout(layout)


