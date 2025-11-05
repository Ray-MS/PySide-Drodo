from typing import Dict

from PySide6.QtCore import QThread
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout

from models.gemtd import GemTDLeaderboardResponse
from network.gemtd import GemTDLeaderboardFetcher

from .column import GemTDLeaderboardColumn

COLUMN_KEYS = ['p1', 'p2', 'p3', 'p4', 'race']


class GemTDLeaderboard(QFrame):
    def __init__(self, account_id: int = 1) -> None:
        super().__init__()

        self.account_id = account_id
        self.columns: Dict[str, GemTDLeaderboardColumn] = dict()

        self._init_ui()
        self._init_layout()
        self._init_connections()

        self._start_fetch_thread()

    def _init_ui(self) -> None:
        self.title_label = QLabel("排行榜")

        for key in COLUMN_KEYS:
            self.columns[key] = GemTDLeaderboardColumn(key)

    def _init_layout(self) -> None:
        column_layout = QHBoxLayout()
        for column in self.columns.values():
            column_layout.addWidget(column)

        main_layout = QVBoxLayout(self)
        main_layout.addWidget(self.title_label)
        main_layout.addLayout(column_layout)

    def _init_connections(self) -> None:
        ...

    def _start_fetch_thread(self) -> None:
        self.thread = QThread(self)
        self.worker = GemTDLeaderboardFetcher(self.account_id)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self._handle_fetch_finished)
        self.worker.error.connect(self._handel_fetch_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def _handle_fetch_finished(self, resp: GemTDLeaderboardResponse) -> None:
        data = resp.data
        for p in data.p1:
            self.columns['p1'].add_coop_entry(p)
        for p in data.p2:
            self.columns['p2'].add_coop_entry(p)
        for p in data.p3:
            self.columns['p3'].add_coop_entry(p)
        for p in data.p4:
            self.columns['p4'].add_coop_entry(p)
        for p in data.race:
            self.columns['race'].add_race_entry(p)

    def _handel_fetch_error(self, msg: str) -> None:
        print(f"[Leaderboard Fetch Error] {msg}")
