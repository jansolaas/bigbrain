from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class Dashboard(QWidget):
    def __init__(self):
        super().__init__()

        # Example: Simple layout with a label
        layout = QVBoxLayout()

        label = QLabel("Welcome to the Dashboard!")
        layout.addWidget(label)

        # Set the layout for this widget
        self.setLayout(layout)
