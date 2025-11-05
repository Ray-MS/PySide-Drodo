from PySide6.QtWidgets import QFrame, QLabel, QVBoxLayout

from models.gemtd.leaderboard import GemTDCoop, GemTDRace

from .row import GemTDLeaderboardRow


class GemTDLeaderboardColumn(QFrame):
    def __init__(self, name: str) -> None:
        super().__init__()

        self.name = name

        self._init_ui()
        self._init_layout()

    def _init_ui(self) -> None:
        self.name_label = QLabel(self.name)

    def _init_layout(self) -> None:
        layout = QVBoxLayout(self)
        layout.addWidget(self.name_label)

    def add_rank(self, name: str) -> None:
        rank_label = QLabel(str(name))
        rank_label.setFixedWidth(30)
        self.layout().addWidget(rank_label)

    def add_race(self, race: GemTDRace) -> None:
        row = GemTDLeaderboardRow(race=race)
        self.layout().addWidget(row)
