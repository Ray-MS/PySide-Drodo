from PySide6.QtWidgets import (QGroupBox, QListWidget, QListWidgetItem,
                               QVBoxLayout)


class TeamCard(QGroupBox):
    def __init__(self) -> None:
        super().__init__()

        self.players = set()

        self._init_ui()
        self._init_layout()
        self._init_connections()

    def _init_ui(self) -> None:
        self.setTitle('Team')

        self.account_list = QListWidget()

    def _init_layout(self) -> None:
        layout = QVBoxLayout(self)
        layout.addWidget(self.account_list)

    def _init_connections(self) -> None:
        self.account_list.itemDoubleClicked.connect(self._remove_player)

    def add_player(self, item: QListWidgetItem) -> None:
        if len(self.players) < 4 and item.text() not in self.players:
            self.account_list.addItem(item.clone())
            self.players.add(item.text())

    def _remove_player(self, item: QListWidgetItem) -> None:
        self.account_list.takeItem(self.account_list.row(item))
        self.players.remove(item.text())
