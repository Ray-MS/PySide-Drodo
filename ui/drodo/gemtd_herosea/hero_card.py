from typing import List, Optional

from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel, QWidget

from models.data_model import GemTDHero

from .ability_card import GemTDAbilityCard, GemTDEmptyAbilityCard


class GemTDHeroCard(QWidget):
    def __init__(self, hero_id: str, hero: Optional[GemTDHero] = None) -> None:
        super().__init__()
        self.hero_id = hero_id
        self.hero = hero

        self._init_ui()
        self._init_layout()

        if self.hero is not None:
            self.update(hero_id, hero)

    def _init_ui(self) -> None:
        self.avatar_label = QLabel()
        self.avatar_label.setAlignment(Qt.AlignCenter)
        self.avatar_label.setFixedSize(60, 60)

        self.ability_cards: List[GemTDAbilityCard] = list()

        self.effect_label = QLabel()
        self.effect_label.setAlignment(Qt.AlignVCenter)
        self.effect_label.setWordWrap(True)
        self.effect_label.setStyleSheet("color: gray; font-size: 11px;")

    def _init_layout(self) -> None:
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(10)

        self.ability_layout = QHBoxLayout()
        self.ability_layout.setSpacing(5)
        for card in self.ability_cards:
            self.ability_layout.addWidget(card)

        main_layout.addWidget(self.avatar_label)
        main_layout.addLayout(self.ability_layout)
        main_layout.addWidget(self.effect_label)

    def update(self, hero_id: str, hero: GemTDHero) -> None:
        self.hero = hero
        self.hero_id = hero_id

        for card in self.ability_cards:
            card.destroy()

        pix = QPixmap(f":/images/lottery/{hero_id}.png")
        if not pix.isNull():
            self.avatar_label.setPixmap(pix.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.avatar_label.setText(hero_id)
        for ability_id, ability_level in hero.ability.items():
            card = GemTDAbilityCard(ability_id, ability_level)
            self.ability_cards.append(card)
            self.ability_layout.addWidget(card)
        max_abilities = int(hero_id[1]) + (hero.extend or 0)
        for _ in range(max_abilities - len(self.ability_cards)):
            card = GemTDEmptyAbilityCard()
            self.ability_cards.append(card)

        self.effect_label.setText(hero.effect)
