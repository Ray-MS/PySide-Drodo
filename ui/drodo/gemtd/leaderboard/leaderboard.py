from typing import Dict

from PySide6.QtCore import QThread
from PySide6.QtWidgets import QFrame, QHBoxLayout, QLabel, QVBoxLayout

from models.gemtd import GemTDLeaderboardResponse
from network.gemtd import GemTDLeaderboardFetcher

from .column import GemTDLeaderboardColumn

keys = ['p1', 'p2', 'p3', 'p4', 'race']


class GemTDLeaderboard(QFrame):
    def __init__(self, account_id: int = 1) -> None:
        super().__init__()

        self.account_id = account_id

        self._init_ui()
        self._init_layout()
        self._init_connections()

        self._start_fetch()

    def _init_ui(self) -> None:
        self.leaderboard_label = QLabel("排行榜")

        self.ranks: dict[str, GemTDLeaderboardColumn] = dict()
        for key in keys:
            widget = GemTDLeaderboardColumn(key)
            self.ranks[key] = widget

    def _init_layout(self) -> None:
        rank_layout = QHBoxLayout()
        for key, widget in self.ranks.items():
            rank_layout.addWidget(widget)

        layout = QVBoxLayout(self)
        layout.addWidget(self.leaderboard_label)
        layout.addLayout(rank_layout)

    def _init_connections(self) -> None:
        ...

    def _start_fetch(self) -> None:
        self.thread = QThread()
        self.worker = GemTDLeaderboardFetcher(self.account_id)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self._on_fetch_finished)
        self.worker.error.connect(self._on_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def _on_fetch_finished(self, resp: GemTDLeaderboardResponse) -> None:
        data = resp.data
        for p in data.p1:
            self.ranks['p1'].add_rank(p.kill)
        for p in data.p2:
            self.ranks['p2'].add_rank(p.kill)
        for p in data.p3:
            self.ranks['p3'].add_rank(p.kill)
        for p in data.p4:
            self.ranks['p4'].add_rank(p.kill)
        for p in data.race:
            self.ranks['race'].add_race(p)

    def _on_error(self, msg: str) -> None:
        print(msg)
