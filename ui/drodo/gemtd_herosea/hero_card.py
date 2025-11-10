from typing import List, Optional

from PySide6.QtCore import Qt, Signal, Slot
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QPushButton

from models.data_model import GemTDHero

from .ability_card import GemTDAbilityCard, GemTDEmptyAbilityCard


class GemTDHeroCard(QFrame):
    selected = Signal(str)

    def __init__(self,  hero_id: str, hero: Optional[GemTDHero] = None) -> None:
        super().__init__()
        self.hero_id = hero_id
        self.hero = hero

        self.avatar_label: QLabel
        self.effect_label: QLabel
        self.button: QPushButton
        self.ability_cards: List[GemTDAbilityCard] = []
        self.ability_layout: QHBoxLayout

        self._init_ui()
        self._init_layout()
        self._init_connections()

        if hero is not None:
            self.update_hero(hero_id, hero)

    def _init_ui(self) -> None:
        self.avatar_label = QLabel(alignment=Qt.AlignCenter)
        self.avatar_label.setFixedSize(60, 60)

        self.ability_cards: List[GemTDAbilityCard] = list()

        self.effect_label = QLabel(alignment=Qt.AlignVCenter)
        self.effect_label.setWordWrap(True)
        self.effect_label.setStyleSheet("color: gray; font-size: 11px;")

        self.button = QPushButton("Select")

    def _init_layout(self) -> None:
        main_layout = QHBoxLayout(self)
        main_layout.setContentsMargins(5, 5, 5, 5)
        main_layout.setSpacing(10)

        self.ability_layout = QHBoxLayout()
        self.ability_layout.setSpacing(5)

        main_layout.addWidget(self.avatar_label)
        main_layout.addLayout(self.ability_layout)
        main_layout.addWidget(self.effect_label)
        main_layout.addWidget(self.button)

    def _init_connections(self) -> None:
        self.button.clicked.connect(self._on_select_clicked)

    @Slot()
    def _on_select_clicked(self) -> None:
        self.selected.emit(self.hero_id)

    def update_hero(self, hero_id: str, hero: GemTDHero) -> None:
        self.hero_id = hero_id
        self.hero = hero

        self._clear_ability_cards()
        self._update_avatar()
        self._update_abilities()
        self._update_effect_label()

    def _update_avatar(self) -> None:
        pixmap = QPixmap(f":/images/lottery/{self.hero_id}.png")
        if not pixmap.isNull():
            self.avatar_label.setPixmap(pixmap.scaled(60, 60, Qt.KeepAspectRatio, Qt.SmoothTransformation))
        else:
            self.avatar_label.setText(self.hero_id)

    def _update_abilities(self) -> None:
        if not self.hero:
            return

        for ability_id, ability_level in self.hero.ability.items():
            card = GemTDAbilityCard(ability_id, ability_level)
            self.ability_cards.append(card)
            self.ability_layout.addWidget(card)

        max_abilities = int(self.hero_id[1]) + (self.hero.extend or 0)
        for _ in range(max_abilities - len(self.ability_cards)):
            card = GemTDEmptyAbilityCard()
            self.ability_cards.append(card)
            self.ability_layout.addWidget(card)

    def _update_effect_label(self) -> None:
        self.effect_label.setText(self.hero.effect)

    def _clear_ability_cards(self) -> None:
        while self.ability_layout.count():
            item = self.ability_layout.takeAt(0)
            widget = item.widget()
            if widget is not None:
                widget.setParent(None)
                widget.deleteLater()
        self.ability_cards.clear()
