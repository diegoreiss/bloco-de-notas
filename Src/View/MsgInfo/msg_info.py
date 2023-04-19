from PySide6.QtWidgets import QMessageBox


class MsgInfo(QMessageBox):
    def __init__(self, icon_type, window_title, text):
        super().__init__()

        if icon_type == 'info':
            super().setIcon(QMessageBox.Information)
        elif icon_type == 'critical':
            super().setIcon(QMessageBox.Critical)

        super().setWindowTitle(window_title)
        super().setText(text)

        super().exec()
