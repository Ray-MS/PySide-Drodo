from PySide6.QtCore import QThread, Signal
from PySide6.QtWidgets import QLabel, QTabWidget, QVBoxLayout, QWidget

from models.data_model import GemTDHeroesData
from network import GemTDHeroesFetcher

from .gemtd import GemTDWelcomeWidget
from .gemtd_herosea import GemTDHeroSea
from .gemtd_store import GemTDStoreWidget


class GemTDMainWidget(QWidget):
    fetch_finished = Signal(GemTDHeroesData)

    def __init__(self, account_id: int) -> None:
        super().__init__()
        self.account_id = account_id

        self._init_ui()
        self._init_layout()
        self._init_connections()
        self._load()

    def _init_ui(self) -> None:
        self.tab_widget = QTabWidget()

        self.welcome = GemTDWelcomeWidget()
        self.herosea = GemTDHeroSea(account_id=self.account_id)
        self.store = GemTDStoreWidget(account_id=self.account_id)
        self.page4 = self.create_page("页面4内容", "yellow")

        self.tab_widget.addTab(self.welcome, "欢迎")
        self.tab_widget.addTab(self.herosea, "英雄池")
        self.tab_widget.addTab(self.store, "商店")
        self.tab_widget.addTab(self.page4, "标签4")

    def _init_layout(self) -> None:
        layout = QVBoxLayout(self)
        layout.addWidget(self.tab_widget)

    def _init_connections(self) -> None:
        self.fetch_finished.connect(self.welcome.rank.on_fetch_finished)
        self.fetch_finished.connect(self.welcome.quest.on_fetch_finished)
        self.fetch_finished.connect(self.herosea.on_fetch_finished)

    def _load(self) -> None:
        self.thread = QThread()
        self.worker = GemTDHeroesFetcher(self.account_id)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self._on_fetch_finished)
        self.worker.error.connect(self._on_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def create_page(self, content, color):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        label = QLabel(content)
        label.setStyleSheet(f"background-color: {color}; padding: 20px;")
        layout.addWidget(label)
        return widget

    def _on_fetch_finished(self, data: GemTDHeroesData):
        self.fetch_finished.emit(data)

    def _on_error(self, msg: str) -> None:
        print(f"Error fetching data for account {self.account_id}: {msg}")
