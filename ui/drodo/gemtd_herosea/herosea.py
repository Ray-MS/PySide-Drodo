from PySide6.QtCore import Qt
from PySide6.QtWidgets import (QFrame, QScrollArea, QSizePolicy, QVBoxLayout,
                               QWidget)

from models.data_model import GemTDHero, GemTDHeroesData

from .hero_card import GemTDHeroCard


class GemTDHeroseaWidget(QFrame):
    def __init__(self) -> None:
        super().__init__()

        self._init_ui()
        self._init_layout()
        self._init_connections()

    def _init_ui(self) -> None:
        self.onduty_hero = GemTDHeroCard('h101')

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.scroll_content = QWidget()
        self.scroll_area.setWidget(self.scroll_content)

    def _init_layout(self) -> None:
        layout = QVBoxLayout(self)
        layout.addWidget(self.onduty_hero)
        layout.addWidget(self.scroll_area)
        self.scroll_content_layout = QVBoxLayout(self.scroll_content)

    def _init_connections(self) -> None:
        pass

    def add_widget(self, hero_id: str, hero: GemTDHero) -> None:
        widget = GemTDHeroCard(hero_id, hero)
        self.scroll_content_layout.addWidget(widget)

    def on_fetch_finished(self, data: GemTDHeroesData):
        for key, hero in data.hero_sea.items():
            self.add_widget(key, hero)
        self.onduty_hero.update(data.onduty_hero.hero_id, data.onduty_hero)
