from typing import Dict

from PySide6.QtWidgets import QStackedWidget, QWidget

from .drodo import GemTDMainWidget
from .drodo.gemtd import GemTDLeaderboard


class InfoView(QStackedWidget):
    def __init__(self) -> None:
        super().__init__()

        self.pages: Dict[int, QWidget] = {}
        self._init_ui()

    def _init_ui(self) -> None:
        self.add_page(0, GemTDLeaderboard())

    def add_page(self, key: int, widget: QWidget) -> None:
        if self.pages.get(key):
            print(f"页面 {key} 已存在")
            return

        self.addWidget(widget)
        self.pages[key] = widget

    def show_page(self, account_id: int) -> None:
        if widget := self.pages.get(account_id):
            self.setCurrentWidget(widget)
        else:
            self.setCurrentWidget(self.pages[0])
            widget = GemTDMainWidget(account_id)
            self.add_page(account_id, widget)
            self.setCurrentWidget(widget)
