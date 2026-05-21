import logging
import sys

from PySide6.QtCore import Qt
from PySide6.QtGui import QStandardItemModel, QStandardItem
from PySide6.QtWidgets import (
    QApplication, QMainWindow, QMenuBar, QSplitter, QTreeView, QListWidget,
    QLabel, QVBoxLayout, QHBoxLayout, QGroupBox, QFormLayout, QWidget,
    QTableWidget, QStatusBar, QAbstractItemView, QComboBox, QPushButton,
    QTabWidget
)

from frontend.services.backed_service import BackendService


# Import the logging configuration (this will execute the config setup)
# Create a logger for the dashboard module
logger = logging.getLogger(__name__)


class Dashboard(QMainWindow):
    def __init__(self):
        super(Dashboard, self).__init__()
        self.setWindowTitle("Pipeline GUI")

        self.projects = []
        self.current_project_id = None
        self.current_project = None

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

        self.load_projects()

        self.apply_user_permissions()

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
        Create the left panel with project selection and Assets/Shots tabs.
        """
        assets_widget = QWidget()
        layout = QVBoxLayout()

        # Project selector row
        project_row = QHBoxLayout()

        project_label = QLabel("Project:")
        project_row.addWidget(project_label)

        self.project_combo = QComboBox()
        self.project_combo.currentIndexChanged.connect(self.on_project_changed)
        project_row.addWidget(self.project_combo)

        self.manage_projects_button = QPushButton("Manage Projects...")
        self.manage_projects_button.clicked.connect(self.open_project_manager)
        project_row.addWidget(self.manage_projects_button)

        layout.addLayout(project_row)

        # Title
        title = QLabel("<b>Assets / Shots</b>")
        layout.addWidget(title)

        # Tabs for switching between assets and shots
        self.asset_shot_tabs = QTabWidget()
        self.asset_shot_tabs.currentChanged.connect(self.on_asset_shot_tab_changed)

        # Assets tab
        self.assets_tree = QTreeView()
        self.assets_tree.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.assets_tree.setModel(self.populate_assets_tree([]))
        self.assets_tree.selectionModel().selectionChanged.connect(self.show_item_metadata)
        self.asset_shot_tabs.addTab(self.assets_tree, "Assets")

        # Shots tab
        self.shots_tree = QTreeView()
        self.shots_tree.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.shots_tree.setModel(self.populate_shots_tree([]))
        self.shots_tree.selectionModel().selectionChanged.connect(self.show_item_metadata)
        self.asset_shot_tabs.addTab(self.shots_tree, "Shots")

        layout.addWidget(self.asset_shot_tabs)

        # Thumbnail Preview
        self.thumbnail_label = QLabel("Thumbnail Preview")
        self.thumbnail_label.setFixedHeight(100)
        self.thumbnail_label.setStyleSheet("background-color: #333; color: white;")
        layout.addWidget(self.thumbnail_label)

        # Metadata Section
        item_metadata = QGroupBox("Selection Metadata")
        metadata_layout = QFormLayout()

        self.metadata_name = QLabel("N/A")
        self.metadata_type = QLabel("N/A")
        self.metadata_framerange = QLabel("N/A")
        self.metadata_project = QLabel("N/A")

        metadata_layout.addRow("Name:", self.metadata_name)
        metadata_layout.addRow("Type:", self.metadata_type)
        metadata_layout.addRow("Framerange:", self.metadata_framerange)
        metadata_layout.addRow("Project ID:", self.metadata_project)

        item_metadata.setLayout(metadata_layout)
        layout.addWidget(item_metadata)

        assets_widget.setLayout(layout)
        return assets_widget

    def apply_user_permissions(self):
        """
        Update UI based on the logged-in user's role.
        """
        current_user = BackendService.current_user or {}
        username = current_user.get("username", "Unknown user")
        role = current_user.get("role", "unknown")

        self.setWindowTitle(f"Pipeline GUI - {username} ({role})")

        # Only admins can manage projects for now
        is_admin = role == "admin"
        self.manage_projects_button.setEnabled(is_admin)

        if is_admin:
            self.statusBar().showMessage(f"Logged in as {username} ({role})")
        else:
            self.statusBar().showMessage(
                f"Logged in as {username} ({role}) - project management disabled"
            )

    def load_projects(self):
        """
        Load projects into the project dropdown.
        """
        self.projects = BackendService.fetch_projects()

        self.project_combo.blockSignals(True)
        self.project_combo.clear()

        for project in self.projects:
            project_name = project.get("name", "Unnamed Project")
            project_code = project.get("code")

            if project_code:
                label = f"{project_name} ({project_code})"
            else:
                label = project_name

            self.project_combo.addItem(label, project)

        self.project_combo.blockSignals(False)

        if self.project_combo.count() > 0:
            self.project_combo.setCurrentIndex(0)
            self.on_project_changed(0)
        else:
            self.current_project = None
            self.current_project_id = None
            self.refresh_project_data()

    def refresh_assets(self):
        """
        Reload the asset tree for the selected project.
        """
        if self.current_project_id is None:
            assets = []
        else:
            assets = BackendService.fetch_assets(project_id=self.current_project_id)

        asset_model = self.populate_assets_tree(assets)
        self.assets_tree.setModel(asset_model)
        self.assets_tree.selectionModel().selectionChanged.connect(self.show_item_metadata)

    def refresh_shots(self):
        """
        Reload the shot tree for the selected project.
        """
        if self.current_project_id is None:
            shots = []
        else:
            shots = BackendService.list_shots(project_id=self.current_project_id)

        shot_model = self.populate_shots_tree(shots)
        self.shots_tree.setModel(shot_model)
        self.shots_tree.selectionModel().selectionChanged.connect(self.show_item_metadata)

    def on_asset_shot_tab_changed(self, index):
        """
        Clear metadata when switching between Assets and Shots.
        """
        self.clear_metadata()

    def on_project_changed(self, index):
        """
        React when the selected project changes.
        """
        if index < 0:
            self.current_project = None
            self.current_project_id = None
        else:
            self.current_project = self.project_combo.itemData(index)
            self.current_project_id = self.current_project.get("id") if self.current_project else None

        self.refresh_project_data()

    def refresh_project_data(self):
        """
        Refresh all dashboard data for the currently selected project.
        """
        self.refresh_assets()
        self.refresh_shots()

        if self.current_project:
            project_name = self.current_project.get("name", "Unnamed Project")
            self.statusBar().showMessage(f"Current project: {project_name}")
        else:
            self.statusBar().showMessage("No project selected")

    def open_project_manager(self):
        """
        Placeholder for future create/edit/delete project dialog.
        """
        self.statusBar().showMessage("Project manager is not built yet.")

    # def populate_assets_tree(self, assets):
    #     """
    #     Populate the QTreeView with asset data from the backend.
    #
    #     Expects `assets` to be a list of dictionaries, for example:
    #     {
    #         "id": 1,
    #         "project_id": 1,
    #         "project_name": "Big Brain Feature",
    #         "name": "HeroCharacter",
    #         "type": "character"
    #     }
    #     """
    #     model = QStandardItemModel()
    #     model.setHorizontalHeaderLabels(["Assets"])
    #
    #     root = model.invisibleRootItem()
    #
    #     def add_items(parent, items):
    #         for item in items:
    #             name = item.get("name", "Unnamed Asset")
    #             asset_type = item.get("type")
    #
    #             if asset_type:
    #                 label = f"{name} ({asset_type})"
    #             else:
    #                 label = name
    #
    #             tree_item = QStandardItem(label)
    #
    #             # Store useful backend data on the item for later use
    #             tree_item.setData(item.get("id"), Qt.UserRole)
    #             tree_item.setData(item, Qt.UserRole + 1)
    #
    #             parent.appendRow(tree_item)
    #
    #             # Safe for both flat lists and nested tree-style data
    #             children = item.get("children", [])
    #             if children:
    #                 add_items(tree_item, children)
    #
    #     if isinstance(assets, list):
    #         add_items(root, assets)
    #
    #     return model

    def populate_assets_tree(self, assets):
        """
        Populate the asset tree with asset data from the backend.
        """
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Assets"])

        root = model.invisibleRootItem()

        def add_items(parent, items):
            for item in items:
                name = item.get("name", "Unnamed Asset")
                asset_type = item.get("type")

                if asset_type:
                    label = f"{name} ({asset_type})"
                else:
                    label = name

                tree_item = QStandardItem(label)

                tree_item.setData("asset", Qt.UserRole)
                tree_item.setData(item, Qt.UserRole + 1)

                parent.appendRow(tree_item)

                children = item.get("children", [])
                if children:
                    add_items(tree_item, children)

        if isinstance(assets, list):
            add_items(root, assets)

        return model

    def populate_shots_tree(self, shots):
        """
        Populate the shot tree with shot data from the backend.

        Shots are grouped by sequence_id.
        """
        model = QStandardItemModel()
        model.setHorizontalHeaderLabels(["Shots"])

        root = model.invisibleRootItem()
        sequences = {}

        if not isinstance(shots, list):
            return model

        for shot in shots:
            sequence_id = shot.get("sequence_id", "No Sequence")

            if sequence_id not in sequences:
                sequence_item = QStandardItem(f"Sequence {sequence_id}")
                sequence_item.setData("sequence", Qt.UserRole)
                sequence_item.setData({"sequence_id": sequence_id}, Qt.UserRole + 1)
                root.appendRow(sequence_item)
                sequences[sequence_id] = sequence_item

            name = shot.get("name", "Unnamed Shot")
            frame_start = shot.get("frame_start")
            frame_end = shot.get("frame_end")

            if frame_start is not None and frame_end is not None:
                label = f"{name} [{frame_start}-{frame_end}]"
            else:
                label = name

            shot_item = QStandardItem(label)
            shot_item.setData("shot", Qt.UserRole)
            shot_item.setData(shot, Qt.UserRole + 1)

            sequences[sequence_id].appendRow(shot_item)

        return model

    # def show_asset_metadata(self, selected, deselected):
    #     """
    #     Show the metadata for the selected asset.
    #     """
    #     selected_indexes = self.assets_tree.selectionModel().selectedIndexes()
    #     if selected_indexes:
    #         selected_item = selected_indexes[0]
    #         selected_asset = selected_item.data()
    #         # You could fetch more metadata from the backend here if needed.
    #         self.metadata_framerange.setText(f"Framerange: Backend Data for {selected_asset}")
    #     else:
    #         self.metadata_framerange.setText("Framerange: N/A")

    def show_item_metadata(self, selected, deselected):
        """
        Show metadata for the selected asset, shot, or sequence.
        """
        active_tree = self.asset_shot_tabs.currentWidget()
        selected_indexes = active_tree.selectionModel().selectedIndexes()

        if not selected_indexes:
            self.clear_metadata()
            return

        selected_item = selected_indexes[0]
        item_type = selected_item.data(Qt.UserRole)
        item_data = selected_item.data(Qt.UserRole + 1)

        if not isinstance(item_data, dict):
            self.clear_metadata()
            return

        name = item_data.get("name", "N/A")
        project_id = item_data.get("project_id", self.current_project_id)

        self.metadata_name.setText(str(name))
        self.metadata_project.setText(str(project_id) if project_id is not None else "N/A")

        if item_type == "asset":
            asset_type = item_data.get("type", "N/A")
            self.metadata_type.setText(f"Asset / {asset_type}")
            self.metadata_framerange.setText("N/A")

        elif item_type == "shot":
            frame_start = item_data.get("frame_start")
            frame_end = item_data.get("frame_end")

            self.metadata_type.setText("Shot")

            if frame_start is not None and frame_end is not None:
                self.metadata_framerange.setText(f"{frame_start} - {frame_end}")
            else:
                self.metadata_framerange.setText("N/A")

        elif item_type == "sequence":
            sequence_id = item_data.get("sequence_id", "N/A")
            self.metadata_name.setText(f"Sequence {sequence_id}")
            self.metadata_type.setText("Sequence")
            self.metadata_framerange.setText("N/A")

        else:
            self.metadata_type.setText("N/A")
            self.metadata_framerange.setText("N/A")

    def clear_metadata(self):
        """
        Clear the metadata display.
        """
        self.metadata_name.setText("N/A")
        self.metadata_type.setText("N/A")
        self.metadata_framerange.setText("N/A")
        self.metadata_project.setText("N/A")

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


# def add_items(parent, items):
#     for item in items:
#         name = item.get("name", "Unnamed")
#
#         frame_start = item.get("frame_start")
#         frame_end = item.get("frame_end")
#
#         if frame_start is not None and frame_end is not None:
#             label = f"{name} [{frame_start}-{frame_end}]"
#         else:
#             label = name
#
#         tree_item = QStandardItem(label)
#
#         tree_item.setData(item.get("id"), Qt.UserRole)
#         tree_item.setData(item, Qt.UserRole + 1)
#
#         parent.appendRow(tree_item)
#
#         children = item.get("children", [])
#         if children:
#             add_items(tree_item, children)


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
