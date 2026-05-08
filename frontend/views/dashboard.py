import logging
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QSplitter, QTreeView, QListWidget,
    QLabel, QVBoxLayout, QGroupBox, QFormLayout, QWidget,
    QTableWidget, QStatusBar, QAbstractItemView
)

from frontend.services.backed_service import BackendService



# Import the logging configuration (this will execute the config setup)

# Create a logger for the dashboard module
logger = logging.getLogger(__name__)


# # Mock Backend Function
# def fetch_assets():
#     """
#     Fetch hierarchical assets from the backend (or a mock backend in this case).
#     Each asset can have a name, framerange, and children (sub-assets).
#     """
#     return [
#         {"name": "ap-001", "framerange": "1001.0 - 1073.0", "children": []},
#         {"name": "seq-0010", "framerange": "1050.0 - 1100.0", "children": [
#             {"name": "seq-0010-shot-01", "framerange": "1051.0 - 1060.0", "children": []},
#             {"name": "seq-0010-shot-02", "framerange": "1061.0 - 1070.0", "children": []},
#         ]},
#     ]


class Dashboard(QMainWindow):
    def __init__(self):
        super(Dashboard, self).__init__()
        self.setWindowTitle("Pipeline GUI")

        # --- Main Layout ---
        self.main_splitter = QSplitter(Qt.Horizontal)
        self.setCentralWidget(self.main_splitter)

        # --- Panes ---
        # Left Panel: Assets/Shots
        self.left_panel = self.create_assets_panel()
        self.main_splitter.addWidget(self.left_panel)

        # Middle Panel: Departments/Tasks
        self.middle_panel = self.create_departments_panel()
        self.main_splitter.addWidget(self.middle_panel)

        # Right Panel: Files/Versions
        self.right_panel = self.create_files_panel()
        self.main_splitter.addWidget(self.right_panel)

        # --- Top Bar ---
        self.menu_bar = self.add_menu_bar()

        # --- Bottom Bar ---
        self.status_bar = self.add_status_bar()

        # --- Sizing ---
        self.main_splitter.setStretchFactor(0, 2)  # Left Panel gets 40%
        self.main_splitter.setStretchFactor(1, 1)  # Middle gets 30%
        self.main_splitter.setStretchFactor(2, 1)  # Right Panel gets 30%

    def add_menu_bar(self):
        """
        Add a basic menu bar with options (e.g., File, Edit, Help, etc.)
        """
        menu_bar = QMenuBar()
        self.setMenuBar(menu_bar)

        file_menu = menu_bar.addMenu("File")
        edit_menu = menu_bar.addMenu("Edit")
        view_menu = menu_bar.addMenu("View")
        help_menu = menu_bar.addMenu("Help")

        return menu_bar

    def add_status_bar(self):
        """
        Add a status bar to show metadata about the selected shot/asset.
        """
        status_bar = QStatusBar()
        self.setStatusBar(status_bar)
        status_bar.showMessage("Ready")
        return status_bar

    def create_assets_panel(self):
        """
        Create the left panel (Assets/Shots) with hierarchical lists and metadata.
        """
        assets_widget = QWidget()
        layout = QVBoxLayout()

        # Title: Assets/Shots
        title = QLabel("<b>Assets/Shots</b>")
        layout.addWidget(title)

        # Hierarchical List
        self.assets_tree = QTreeView()
        asset_model = self.populate_assets_tree(BackendService.fetch_assets())
        self.assets_tree.setModel(asset_model)
        self.assets_tree.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.assets_tree.selectionModel().selectionChanged.connect(self.show_asset_metadata)
        layout.addWidget(self.assets_tree)

        # Thumbnail Preview
        self.thumbnail_label = QLabel("Thumbnail Preview")
        self.thumbnail_label.setFixedHeight(100)
        self.thumbnail_label.setStyleSheet("background-color: #333; color: white;")
        layout.addWidget(self.thumbnail_label)

        # Metadata Section
        asset_metadata = QGroupBox("Asset Metadata")
        metadata_layout = QFormLayout()
        self.metadata_framerange = QLabel("Framerange: N/A")
        metadata_layout.addRow("Framerange:", self.metadata_framerange)
        asset_metadata.setLayout(metadata_layout)
        layout.addWidget(asset_metadata)

        assets_widget.setLayout(layout)
        return assets_widget

    def populate_assets_tree(self, assets):
        """
        Populate the QTreeView with data from the backend.
        """
        model = QStandardItemModel()
        root = model.invisibleRootItem()

        def add_items(parent, items):
            for item in items:
                tree_item = QStandardItem(item["name"])
                parent.appendRow(tree_item)
                if item["children"]:
                    add_items(tree_item, item["children"])

        add_items(root, assets)
        model.setHorizontalHeaderLabels(["Assets"])
        return model

    def show_asset_metadata(self, selected, deselected):
        """
        Show the metadata for the selected asset.
        """
        selected_indexes = self.assets_tree.selectionModel().selectedIndexes()
        if selected_indexes:
            selected_item = selected_indexes[0]
            selected_asset = selected_item.data()
            # You could fetch more metadata from the backend here if needed.
            self.metadata_framerange.setText(f"Framerange: Backend Data for {selected_asset}")
        else:
            self.metadata_framerange.setText("Framerange: N/A")

    def create_departments_panel(self):
        """
        Create the middle panel (Departments/Tasks) with hierarchical lists.
        """
        departments_widget = QWidget()
        layout = QVBoxLayout()

        # Title: Departments/Tasks
        title = QLabel("<b>Departments/Tasks</b>")
        layout.addWidget(title)

        # Task List
        list_widget = QListWidget()
        departments = ["Animation", "Blocking", "Compositing", "FX", "Modeling", "Lighting"]
        for department in departments:
            list_widget.addItem(department)
        layout.addWidget(list_widget)

        departments_widget.setLayout(layout)
        return departments_widget

    def create_files_panel(self):
        """
        Create the right panel (Files/Versions) with a table for different versions.
        """
        files_widget = QWidget()
        layout = QVBoxLayout()

        # Title: Files/Versions
        title = QLabel("<b>Files/Versions</b>")
        layout.addWidget(title)

        # File Table
        file_table = QTableWidget(0, 4)  # Rows, Columns
        file_table.setHorizontalHeaderLabels(["Thumbnail", "Version", "User", "Timestamp"])
        file_table.horizontalHeader().setStretchLastSection(True)
        layout.addWidget(file_table)

        files_widget.setLayout(layout)
        return files_widget


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Dashboard()
    window.show()
    sys.exit(app.exec())


# class Dashboard(QWidget):
#     def __init__(self):
#         super().__init__()
#
#         # Example: Simple layout with a label
#         layout = QVBoxLayout()
#
#         label = QLabel("Welcome to the Dashboard!")
#         layout.addWidget(label)
#
#         # Set the layout for this widget
#         self.setLayout(layout)
#
#
#         logger.info("Initializing Dashboard")
#
#     def start(self):
#         try:
#             # Simulating dashboard startup logic
#             logger.info("Starting the Dashboard")
#             # Example of logging different levels:
#             logger.debug("This is a debug message for tracing values.")
#             logger.warning("This is a warning message.")
#             logger.error("This is an error message, something went wrong.")
#         except Exception as e:
#             logger.exception("An exception occurred while starting the Dashboard")
#         finally:
#             logger.info("Dashboard execution finished.")
