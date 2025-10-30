import requests
from PySide6.QtCore import QObject, Signal, Slot

from config import url_manager
from models.data_model import GemTDHeroesData, GemTDHeroesResponse


class GemTDHeroesFetcher(QObject):
    finished = Signal(GemTDHeroesData)
    error = Signal(str)

    def __init__(self, account_id: int) -> None:
        super().__init__()
        self.steam_id = str(0x110000100000000 + account_id)

    @Slot()
    def run(self) -> None:
        url = url_manager.build_url('gemtd.heroes', steam_id=self.steam_id)
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = GemTDHeroesResponse(**resp.json()).data[self.steam_id]
            self.finished.emit(data)
        except Exception as e:
            self.error.emit(str(e))
