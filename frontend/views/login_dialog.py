from PySide6.QtWidgets import (
    QDialog, QVBoxLayout, QFormLayout, QLineEdit,
    QPushButton, QLabel, QHBoxLayout
)

from frontend.services.backed_service import BackendService


class LoginDialog(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Login")
        self.setModal(True)

        layout = QVBoxLayout()

        form_layout = QFormLayout()

        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Username")

        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)

        form_layout.addRow("Username:", self.username_input)
        form_layout.addRow("Password:", self.password_input)

        layout.addLayout(form_layout)

        self.error_label = QLabel("")
        self.error_label.setStyleSheet("color: red;")
        layout.addWidget(self.error_label)

        button_row = QHBoxLayout()

        self.login_button = QPushButton("Login")
        self.login_button.clicked.connect(self.try_login)

        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)

        button_row.addWidget(self.login_button)
        button_row.addWidget(self.cancel_button)

        layout.addLayout(button_row)

        self.setLayout(layout)

    def try_login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text()

        if not username or not password:
            self.error_label.setText("Please enter username and password.")
            return

        try:
            BackendService.login(username, password)
        except Exception as e:
            self.error_label.setText("Login failed. Check username/password.")
            print(f"Login error: {e}")
            return

        self.accept()