import json

from PySide6.QtCore import Qt, QUrl, Slot
from PySide6.QtNetwork import (QNetworkAccessManager, QNetworkReply,
                               QNetworkRequest)
from PySide6.QtWidgets import QFrame, QScrollArea, QVBoxLayout, QWidget

from config import url_manager
from models.data_model import GemTDHero, GemTDHeroesData
from utils import get_steam_id

from .hero_card import GemTDHeroCard


class GemTDHeroSea(QFrame):
    def __init__(self, account_id: str) -> None:
        super().__init__()
        self.account_id = account_id
        self.steam_id = get_steam_id(self.account_id)

        self.network_manager = QNetworkAccessManager(self)
        self._data: GemTDHeroesData
        self._onduty_id: str

        self._init_ui()
        self._init_layout()
        self._init_connections()

    def _init_ui(self) -> None:
        self._onduty_card = GemTDHeroCard('h101')

        self._scroll_area = QScrollArea()
        self._scroll_area.setWidgetResizable(True)
        self._scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self._scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self._scroll_content = QWidget()
        self._scroll_area.setWidget(self._scroll_content)
        self._scroll_layout = QVBoxLayout(self._scroll_content)
        self._scroll_layout.setContentsMargins(8, 8, 8, 8)
        self._scroll_layout.setSpacing(8)

    def _init_layout(self) -> None:
        main_layout = QVBoxLayout(self)
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(12)
        main_layout.addWidget(self._onduty_card)
        main_layout.addWidget(self._scroll_area)

    def _init_connections(self) -> None:
        self.network_manager.finished.connect(self._on_request_finished)

    def _add_hero_card(self, hero_id: str, hero: GemTDHero) -> None:
        card = GemTDHeroCard(hero_id, hero)
        card.selected.connect(self._on_hero_selected)
        self._scroll_layout.addWidget(card)

    @Slot(str)
    def _on_hero_selected(self, hero_id: str) -> None:
        self._onduty_id = hero_id
        url = QUrl(url_manager.build_url("gemtd.save", hero_id=hero_id, steam_id=self.steam_id))
        request = QNetworkRequest(url)
        self.network_manager.get(request)

    @Slot(QNetworkReply)
    def _on_request_finished(self, reply: QNetworkReply) -> None:
        try:
            if reply.error() == QNetworkReply.NoError:
                data = reply.readAll().data().decode('utf-8')
                data = json.loads(data)
                if data['err'] == 0 and self._data and self._onduty_id:
                    if hero := self._data.hero_sea.get(self._onduty_id):
                        self._onduty_card.update_hero(self._onduty_id, hero)
        finally:
            reply.deleteLater()

    def on_fetch_finished(self, data: GemTDHeroesData):
        self._data = data
        self._onduty_id = data.onduty_hero.hero_id

        while self._scroll_layout.count():
            item = self._scroll_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()

        for hero_id, hero in data.hero_sea.items():
            self._add_hero_card(hero_id, hero)

        self._onduty_card.update_hero(data.onduty_hero.hero_id, data.onduty_hero)
