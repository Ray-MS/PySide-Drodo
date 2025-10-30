import json
import re
from datetime import datetime
from pathlib import Path

from PySide6.QtCore import Qt, QThread
from PySide6.QtWidgets import (QHBoxLayout, QLineEdit, QMainWindow,
                               QPushButton, QVBoxLayout, QWidget)

from models.data_model import GemTDHeroesData
from network.fetcher import GemTDHeroesFetcher
from ui.gemtd_widget import GemTDWidget
from ui.info_view import InfoView
from ui.quest_card import QuestCard
from ui.sidebar import Sidebar

CACHE_FILE = 'account_cache.json'
CACHE_TTL = 24 * 60 * 60


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self._init_ui()
        self._load_cache()
        self.request_ids = set()

    def _init_ui(self):
        self.setWindowTitle("Drodo App")
        self.setGeometry(100, 100, 800, 600)

        self.sidebar = Sidebar()
        self.info_view = InfoView()
        self.sidebar.list_widget.itemClicked.connect(self._on_sidebar_item_clicked)

        main_view_layout = QVBoxLayout()
        main_view_layout.addWidget(self.info_view)

        central_layout = QHBoxLayout()
        central_layout.addWidget(self.sidebar)
        central_layout.addLayout(main_view_layout)

        container = QWidget()
        container.setLayout(central_layout)
        self.setCentralWidget(container)

    def _load_cache(self):
        if Path(CACHE_FILE).exists():
            with open(CACHE_FILE, 'r', encoding='utf-8') as fp:
                self.cache = json.load(fp)
                for player in self.cache.get('players', {}).keys():
                    self._add_account(int(player))
        else:
            self.cache = {
                'lastUpdated': datetime.now().isoformat(),
                'players': {},
            }

    def _add_account(self, account_id: int):
        self.sidebar._add_item(account_id)
        self.info_view.add_page(account_id, GemTDWidget(account_id))

    def start_fetch(self, account_id: int):
        self.thread = QThread()
        self.worker = GemTDHeroesFetcher(account_id)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.handle_result)
        self.worker.error.connect(self.handle_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def handle_result(self, data: GemTDHeroesData):
        card = QuestCard(data)
        self.main_layout.addWidget(card)

    def handle_error(self, err_msg: str):
        print(f"请求出错：{err_msg}")

    def _on_sidebar_item_clicked(self, item):
        account_id = item.data(Qt.UserRole)
        self.info_view.show_page(account_id)
