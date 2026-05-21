import sys

from PySide6.QtWidgets import QApplication

from frontend.views.dashboard import Dashboard
from frontend.views.login_dialog import LoginDialog


if __name__ == "__main__":
    app = QApplication(sys.argv)

    login_dialog = LoginDialog()

    if login_dialog.exec() == LoginDialog.Accepted:
        window = Dashboard()
        window.show()
        sys.exit(app.exec())

    sys.exit(0)