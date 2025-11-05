from pathlib import Path

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QMainWindow, QVBoxLayout, QWidget

from models import player_manager
from ui.drodo import DrodoWidget
from ui.info_view import InfoView
from ui.sidebar import Sidebar


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        player_manager.load_cache()

        self._init_ui()
        self._init_layout()
        self._init_connections()

    def _init_ui(self):
        self.setWindowTitle("Drodo App")
        self.setGeometry(100, 100, 800, 600)

        self.sidebar = Sidebar()
        self.info_view = InfoView()

        main_view_layout = QVBoxLayout()
        main_view_layout.addWidget(self.info_view)

        central_layout = QHBoxLayout()
        central_layout.addWidget(self.sidebar)
        central_layout.addLayout(main_view_layout)

        container = QWidget()
        container.setLayout(central_layout)
        self.setCentralWidget(container)

    def _init_layout(self) -> None:
        ...

    def _init_connections(self) -> None:
        self.sidebar.leaderboard_button.clicked.connect(lambda: self.info_view.show_page(0))
        self.sidebar.account_list.itemClicked.connect(self._on_sidebar_item_clicked)
        self.sidebar.team_card.account_list.itemClicked.connect(self._on_sidebar_item_clicked)

    def _add_account(self, account_id: int):
        self.sidebar.update_account(account_id)
        self.info_view.add_page(account_id, DrodoWidget(account_id))

    def _on_sidebar_item_clicked(self, item):
        account_id = item.data(Qt.UserRole)
        self.info_view.show_page(account_id)
