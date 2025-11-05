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

        if bool(coop) == bool(race):
            raise ValueError("GemTDLeaderboardRow must have exactly one of coop or race.")
        self.avatars = []
        self.score_label = QLabel()

        self._init_layout()

        self._set_coop(coop)
        self._set_race(race)

    def _init_layout(self) -> None:
        self.avatar_layout = QHBoxLayout()
        layout = QHBoxLayout(self)
        layout.addLayout(self.avatar_layout)
        layout.addWidget(self.score_label)

    def _update_avatar_layout(self) -> None:
        for avatar in self.avatars:
            self.avatar_layout.addWidget(avatar)

    def _set_coop(self, coop: Optional[GemTDCoop]) -> None:
        if coop is None:
            return
        player_ids = coop.player_ids.split(',')
        self.avatars = [SteamAvatar(get_account_id(pid)) for pid in player_ids]
        self.score_label.setText(str(coop.kill))
        self._update_avatar_layout()

    def _set_race(self, race: Optional[GemTDRace]) -> None:
        if race is None:
            return
        self.avatars = [SteamAvatar(get_account_id(race.player_id))]
        self.score_label.setText(str(race.race_level))
        self._update_avatar_layout()
