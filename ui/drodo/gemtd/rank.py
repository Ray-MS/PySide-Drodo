from typing import Optional

from PySide6.QtCore import QThread
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from models.data_model import GemTDHeroesData, GemTDRankInfo
from network import GemTDHeroesFetcher


class GemTDRankCard(QWidget):
    def __init__(self, account_id: Optional[int] = None, rank: Optional[GemTDRankInfo] = None) -> None:
        super().__init__()

        self._init_ui()

        if rank is not None:
            self._on_rank_updated(rank)
        elif account_id is not None:
            self.account_id = account_id
            self.steam_id = str(0x110000100000000 + account_id)
            self._start_fetch()

    def _init_ui(self):
        self.rank_score_label = QLabel("Rank Score: N/A")
        self.rank_coop_label = QLabel("Rank Coop: N/A")
        self.rank_race_label = QLabel("Rank Race: N/A")
        self.best_kill_p1 = QLabel("Best Kill P1: N/A")
        self.best_kill_p2 = QLabel("Best Kill P2: N/A")
        self.best_kill_p3 = QLabel("Best Kill P3: N/A")
        self.best_kill_p4 = QLabel("Best Kill P4: N/A")

        rank_layout = QHBoxLayout()
        rank_layout.addWidget(self.rank_score_label)
        rank_layout.addWidget(self.rank_coop_label)
        rank_layout.addWidget(self.rank_race_label)

        best_kill_layout = QHBoxLayout()
        best_kill_layout.addWidget(self.best_kill_p1)
        best_kill_layout.addWidget(self.best_kill_p2)
        best_kill_layout.addWidget(self.best_kill_p3)
        best_kill_layout.addWidget(self.best_kill_p4)

        layout = QVBoxLayout(self)
        layout.addLayout(rank_layout)
        layout.addLayout(best_kill_layout)

    def _start_fetch(self):
        self.thread = QThread()
        self.worker = GemTDHeroesFetcher(self.account_id)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.on_fetch_finished)
        self.worker.error.connect(self._on_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def on_fetch_finished(self, data: GemTDHeroesData):
        self.rank_score_label.setText(f"Rank All: {data.rank_info.score}")
        self.rank_coop_label.setText(f"Rank Coop: {data.rank_info.rankcoop}")
        self.rank_race_label.setText(f"Rank Race: {data.rank_info.rankrace}")

        self.best_kill_p1.setText(f"Best Kill P1: {data.rank_info.best_kills.p1}")
        self.best_kill_p2.setText(f"Best Kill P2: {data.rank_info.best_kills.p2}")
        self.best_kill_p3.setText(f"Best Kill P3: {data.rank_info.best_kills.p3}")
        self.best_kill_p4.setText(f"Best Kill P4: {data.rank_info.best_kills.p4}")

    def _on_error(self, msg: str):
        print(f"Error fetching data for account {self.account_id}: {msg}")
