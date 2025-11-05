import json
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional

import requests
from PySide6.QtCore import QObject, Signal, Slot

from config import url_manager
from models.gemtd import GemTDGoodsResponse


class GemTDGoodsFetcher(QObject):
    finished = Signal(GemTDGoodsResponse)
    error = Signal(str)

    def __init__(self, account_id: Optional[int] = None) -> None:
        super().__init__()

        self.steam_id = str(0x110000100000000 + account_id)
        self.cache_file = Path('cache', f'{self.steam_id}.gemtd.goods')

    @Slot()
    def run(self) -> None:
        if self._check_cache():
            return

        url = url_manager.build_url('gemtd.goods', steam_id=self.steam_id)
        try:
            resp = requests.get(url, timeout=10)
            resp.raise_for_status()
            data = GemTDGoodsResponse(**resp.json())
            self._save_cache(data)
            self.finished.emit(data)
        except requests.RequestException as e:
            self.error.emit(str(e))

    def _check_cache(self) -> bool:
        if self.cache_file.exists():
            with open(self.cache_file, 'r', encoding='utf-8') as fp:
                cache = json.load(fp)
                cache_time = datetime.fromisoformat(cache['lastUpdated'])
                data = GemTDGoodsResponse(**cache['data'])
                expire_time = cache_time + timedelta(seconds=data.expire)
                if datetime.now() < expire_time:
                    self.finished.emit(data)
                    return True
        return False

    def _save_cache(self, data: GemTDGoodsResponse) -> None:
        value = {'lastUpdated': datetime.now().isoformat(), 'data': data.model_dump()}
        with open(self.cache_file, 'w', encoding='utf-8') as fp:
            json.dump(value, fp, ensure_ascii=False)
