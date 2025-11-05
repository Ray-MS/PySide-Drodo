import json
from collections import defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Iterable

from PySide6.QtCore import QObject, QThread, Signal

from network.steam import SteamPlayerSummariesFetcher


def get_steam_id(account_id: int) -> str:
    return str(0x110000100000000 + account_id)


def get_account_id(steam_id: str) -> int:
    return int(steam_id) - 0x110000100000000


class PlayerManager(QObject):
    updated = Signal()

    def __init__(self) -> None:
        super().__init__()

        self.players = defaultdict(dict)
        self.cache_file = Path('cache', 'players.json')
        self.load_cache()

    def load_cache(self) -> None:
        try:
            with self.cache_file.open('r', encoding='utf-8') as fp:
                data = json.load(fp)
                self.players.update(data['players'])

                cache_time = data['lastUpdated']
                expire_time = datetime.fromisoformat(cache_time) + timedelta(days=1)
                if expire_time > datetime.now():
                    self._update()
        except FileNotFoundError as e:
            print(f"Cache file not exists: {e}")

    def _save_cache(self) -> None:
        with self.cache_file.open('w', encoding='utf-8') as fp:
            data = {
                'lastUpdated': datetime.now().isoformat(),
                'players': self.players,
            }
            json.dump(data, fp, ensure_ascii=False)

    def _update(self) -> None:
        account_ids = self.get_player_account_ids()
        steam_ids = map(get_steam_id, account_ids)

        self.thread = QThread()
        self.worker = SteamPlayerSummariesFetcher(steam_ids=steam_ids)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self._on_fetch_success)
        self.worker.error.connect(self._on_fetch_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def _on_fetch_success(self, data: dict) -> None:
        players = data['response']['players']
        for player in players:
            self.players[str(get_account_id(player['steamid']))].update(player)
        self._save_cache()

    def _on_fetch_error(self, error: str) -> None:
        print(f"Fetch player summaries error: {error}")

    def get_player(self, account_id: int) -> Dict:
        return self.players[str(account_id)]

    def get_player_account_ids(self) -> Iterable[int]:
        return map(int, self.players.keys())

    def get_player_name(self, account_id: int) -> str:
        return self.players[str(account_id)].get('personaname', 'user')

    def add_player(self, account_id: int) -> None:
        self.players[str(account_id)] = {}
        self._save_cache()

    def remove_player(self, account_id: int) -> None:
        self.players.pop(str(account_id))
        self._save_cache()


player_manager = PlayerManager()
