import requests
from PySide6.QtCore import QObject, Signal, Slot

from config import url_manager
from models.gemtd import GemTDLeaderboardResponse


class GemTDLeaderboardFetcher(QObject):
    finished = Signal(GemTDLeaderboardResponse)
    error = Signal(str)

    def __init__(self, account_id: int = 1) -> None:
        super().__init__()

        self.account_id = account_id
        self.steam_id = str(0x110000100000000 + account_id)

    @Slot()
    def run(self) -> None:
        url = url_manager.build_url('gemtd.leaderboard', steam_id=self.steam_id)
        try:
            resp = requests.get(url)
            resp.raise_for_status()
            data = GemTDLeaderboardResponse(**resp.json())
            self.finished.emit(data)
        except requests.RequestException as e:
            self.error.emit(str(e))
