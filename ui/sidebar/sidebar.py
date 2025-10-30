import json
import os
from datetime import datetime
from pathlib import Path

import requests
from PySide6.QtCore import Qt
from PySide6.QtGui import QFont
from PySide6.QtWidgets import (QHBoxLayout, QLineEdit, QListWidget,
                               QListWidgetItem, QPushButton, QVBoxLayout,
                               QWidget)

from config.url_manager import url_manager

CACHE_FILE = 'account_cache.json'
CACHE_TTL = 24 * 60 * 60


class Sidebar(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.account_ids = set()

        self._init_ui()
        self._load_cache()

    def _init_ui(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)

        self.list_widget = QListWidget()
        layout.addWidget(self.list_widget)
        layout.addStretch()

        bottom_widget = QWidget()
        bottom_layout = QHBoxLayout(bottom_widget)
        bottom_layout.setContentsMargins(5, 5, 5, 5)

        self.input_field = QLineEdit()
        self.input_field.setFixedHeight(30)
        self.input_field.setPlaceholderText("请输入 Account ID")
        bottom_layout.addWidget(self.input_field)

        self.add_button = QPushButton('添加账号')
        self.add_button.setFixedHeight(30)
        self.add_button.clicked.connect(self._on_add_clicked)
        bottom_layout.addWidget(self.add_button)

        layout.addWidget(bottom_widget)

        self.setFixedWidth(220)

    def _add_account(self, account_id: int):
        if account_id in self.account_ids:
            return

        self.account_ids.add(account_id)

        cached = self.cache['players'].get(str(account_id), {})
        name = cached.get('personaname', 'account')

        item = QListWidgetItem(f'{name} ({account_id})')
        item.setTextAlignment(Qt.AlignLeft)
        item.setFont(QFont('Arial', 11))
        item.setData(Qt.UserRole, account_id)
        self.list_widget.addItem(item)

        self._fetch_account_info(account_id)

    def _on_add_clicked(self):
        text = self.input_field.text()
        if not text.isdigit():
            self.input_field.clear()
            return

        account_id = int(text)
        self._add_account(account_id)
        self.input_field.clear()

        cached = self.cache['players'].get(str(account_id))
        if cached:
            self._add_account(account_id)

    def _load_cache(self):
        if Path(CACHE_FILE).exists():
            with open(CACHE_FILE, 'r', encoding='utf-8') as fp:
                self.cache = json.load(fp)
        else:
            self.cache = {
                'lastUpdated': datetime.now().isoformat(),
                'players': {},
            }

    def _save_cache(self):
        self.cache['lastUpdated'] = datetime.now().isoformat()
        with open(CACHE_FILE, 'w', encoding='utf-8') as fp:
            json.dump(self.cache, fp, ensure_ascii=False)

    def _fetch_account_info(self, account_id: int):
        KEY = os.getenv('STEAM_API_KEY')
        steam_id = str(0x110000100000000 + account_id)
        url = url_manager.build_url('player_summaries', source='steam', key=KEY, steam_ids=steam_id)

        try:
            resp = requests.get(url, timeout=5)
            resp.raise_for_status()
            data = resp.json()
            for player in data['response']['players']:
                if steam_id := player.get('steam_id'):
                    self.cache['players'][account_id] = player
            self._save_cache()
        except requests.RequestException as e:
            print(f'请求失败: {e}')
