import json
from datetime import datetime
from pathlib import Path

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
        self.cache_file = Path('cache', f'{self.steam_id}.gemtd.heroes')

    @Slot()
    def run(self) -> None:
        if self._check_cache():
            return

        url = url_manager.build_url('gemtd.heroes', steam_id=self.steam_id)
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = GemTDHeroesResponse(**resp.json()).data[self.steam_id]
            self._save_cache(data)
            self.finished.emit(data)
        except Exception as e:
            self.error.emit(str(e))

    def _check_cache(self) -> bool:
        try:
            if self.cache_file.exists():
                with open(self.cache_file, 'r', encoding='utf-8') as fp:
                    cache = json.load(fp)
                    cache_time = datetime.fromisoformat(cache['lastUpdated'])
                    if (datetime.now() - cache_time).days == 0:
                        data = GemTDHeroesData(**cache['data'])
                        self.finished.emit(data)
                        return True
        except Exception as e:
            self.error.emit(str(e))
            return False
        return False

    def _save_cache(self, data: GemTDHeroesData) -> None:
        value = {'lastUpdated': datetime.now().isoformat(), 'data': data.model_dump(by_alias=True)}
        with open(self.cache_file, 'w', encoding='utf-8') as fp:
            json.dump(value, fp, ensure_ascii=False)
