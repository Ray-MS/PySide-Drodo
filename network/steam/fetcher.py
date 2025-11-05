import os
from typing import Iterable

import requests
from PySide6.QtCore import QObject, Signal, Slot

from config import url_manager


class SteamPlayerSummariesFetcher(QObject):
    finished = Signal(dict)
    error = Signal(str)

    def __init__(self, steam_ids: Iterable[str]) -> None:
        super().__init__()

        self.steam_ids = ','.join(steam_ids)

    @Slot()
    def run(self) -> None:
        KEY = os.getenv('STEAM_API_KEY')
        url = url_manager.build_url('player_summaries', source='steam', key=KEY, steam_ids=self.steam_ids)
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = resp.json()
            self.finished.emit(data)
        except requests.RequestException as e:
            self.error.emit(str(e))
