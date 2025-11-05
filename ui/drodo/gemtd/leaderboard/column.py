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
        self.header_label = QLabel(self.name)

    def _init_layout(self) -> None:
        layout = QVBoxLayout(self)
        layout.addWidget(self.header_label)
        layout.addStretch()

    def add_coop_entry(self, coop: GemTDCoop) -> None:
        row = GemTDLeaderboardRow(coop=coop)
        self.layout().insertWidget(self.layout().count() - 1, row)

    def add_race_entry(self, race: GemTDRace) -> None:
        row = GemTDLeaderboardRow(race=race)
        self.layout().insertWidget(self.layout().count() - 1, row)
