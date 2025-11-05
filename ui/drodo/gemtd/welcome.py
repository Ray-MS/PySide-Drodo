from PySide6.QtWidgets import QFrame, QVBoxLayout

from .quest import GemTDQuestCard
from .rank import GemTDRankCard


class GemTDWelcomeWidget(QFrame):
    def __init__(self) -> None:
        super().__init__()

        self._init_ui()
        self._init_layout()
        self._init_connections()

    def _init_ui(self) -> None:
        self.rank = GemTDRankCard()
        self.quest = GemTDQuestCard()

    def _init_layout(self) -> None:
        layout = QVBoxLayout(self)
        layout.addWidget(self.rank)
        layout.addWidget(self.quest)

    def _init_connections(self) -> None:
        pass
