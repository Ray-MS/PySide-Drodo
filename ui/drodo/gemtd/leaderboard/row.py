from typing import Optional

from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout

from models.gemtd.leaderboard import GemTDCoop, GemTDRace
from ui.steam import SteamAvatar
from utils import get_account_id


class GemTDLeaderboardRow(QFrame):
    def __init__(
        self,
        *,
        coop: Optional[GemTDCoop] = None,
        race: Optional[GemTDRace] = None,
    ) -> None:
        super().__init__()

        if coop is None and race is None:
            raise
        if coop is not None and race is not None:
            raise

        self._init_ui()
        self._init_layout()

        self._set_coop(coop)
        self._set_race(race)

    def _init_ui(self) -> None:
        self.avatars = []
        self.score = QLabel()

    def _init_layout(self) -> None:
        self.avatar_layout = QHBoxLayout()

        layout = QHBoxLayout(self)
        layout.addLayout(self.avatar_layout)
        layout.addWidget(self.score)

    def _update_layout(self) -> None:
        for avatar in self.avatars:
            self.avatar_layout.addWidget(avatar)

    def _set_coop(self, coop: Optional[GemTDCoop]) -> None:
        if coop is None:
            return

    def _set_race(self, race: Optional[GemTDRace]) -> None:
        if race is None:
            return
        avatar = SteamAvatar(get_account_id(race.player_id))
        self.avatars.append(avatar)
        self.score.setText(str(race.race_level))
        self._update_layout()
