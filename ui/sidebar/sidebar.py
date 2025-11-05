import json
from datetime import datetime

from PySide6.QtCore import Qt, QThread
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QHBoxLayout, QLineEdit, QListWidget,
                               QListWidgetItem, QPushButton, QVBoxLayout,
                               QWidget)

from models import player_manager
from network.steam import SteamPlayerSummariesFetcher

from .team import TeamCard


class Sidebar(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.account_cache = dict()
        self.account_ids = set()
        self.items: dict[int, QListWidgetItem] = dict()

        self._init_ui()
        self._init_layout()
        self._init_connections()

        self._init_players()

    def _init_ui(self) -> None:
        self.leaderboard_button = QPushButton("排行榜")

        self.account_list = QListWidget()

        self.team_card = TeamCard()

        self.account_input = QLineEdit()
        self.account_input.setPlaceholderText("请输入 Account ID")
        self.account_input.setFixedHeight(30)

        self.add_account_button = QPushButton("添加账号")
        self.add_account_button.setFixedHeight(30)

        self.setFixedWidth(220)

    def _init_layout(self) -> None:
        bottom_layout = QHBoxLayout()
        bottom_layout.setContentsMargins(5, 5, 5, 5)
        bottom_layout.addWidget(self.account_input)
        bottom_layout.addWidget(self.add_account_button)

        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.addWidget(self.leaderboard_button)
        main_layout.addWidget(self.account_list)
        main_layout.addWidget(self.team_card)
        main_layout.addLayout(bottom_layout)

    def _init_connections(self) -> None:
        self.account_list.itemDoubleClicked.connect(self.team_card.add_player)
        self.add_account_button.clicked.connect(self._on_add_account_clicked)
        player_manager.updated.connect(self._on_player_manager_updated)

    def _init_players(self) -> None:
        for account_id in player_manager.get_player_account_ids():
            self.update_account(account_id, fetch=False)

    def _on_add_account_clicked(self) -> None:
        text = self.account_input.text().strip()
        if text.isdigit():
            account_id = int(text)
            if account_id > 0:
                player_manager.add_player(account_id)
                self.update_account(account_id, fetch=False)

        self.account_input.clear()

    def _on_player_manager_updated(self) -> None:
        for account_id in player_manager.get_player_account_ids():
            self.update_account(account_id, fetch=False)

    def update_account(self, account_id: int, fetch: bool = False):
        if not account_id in self.items:
            item = QListWidgetItem()
            item.setTextAlignment(Qt.AlignLeft)
            item.setFont(QFont('Arial', 11))
            item.setData(Qt.UserRole, account_id)
            self.account_list.addItem(item)
            self.items[account_id] = item

        name = player_manager.get_player_name(account_id)
        self.items[account_id].setText(f'{name} ({account_id})')

        if fetch:
            self._start_fetch(account_id)

    def _save_cache(self):
        self.account_cache['lastUpdated'] = datetime.now().isoformat()
        with open(self.cache_file, 'w', encoding='utf-8') as fp:
            json.dump(self.account_cache, fp, ensure_ascii=False)

    def _start_fetch(self, account_id: int):
        self.thread = QThread()
        self.worker = SteamPlayerSummariesFetcher(account_id)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self._on_fetch_finished)
        self.worker.error.connect(self._on_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def _on_fetch_finished(self, data: dict) -> None:
        print(data)

    def _on_error(self, msg: str) -> None:
        print(msg)
