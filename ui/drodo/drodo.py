from PySide6.QtCore import QSize, Qt, QThread
from PySide6.QtGui import QFont, QPixmap
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from models.data_model import GemTDHeroesData
from network.fetcher import GemTDHeroesFetcher


class DrodoWidget(QWidget):
    def __init__(self, account_id: int) -> None:
        super().__init__()

        self.account_id = account_id
        self.steam_id = str(0x110000100000000 + account_id)
        self._init_ui()
        self._start_fetch()

    def _init_ui(self) -> None:
        account_id_label = QLabel(f"Account ID: {self.account_id}")
        self.wallet = _WalletWidget()

        layout = QVBoxLayout(self)
        layout.addWidget(account_id_label)
        layout.addWidget(self.wallet)

    def _start_fetch(self) -> None:
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

    def _on_fetch_finished(self, data: GemTDHeroesData) -> None:
        self.wallet.set_shell(data.shell)
        self.wallet.set_ice(data.ice)
        self.wallet.set_candy(data.candy)

    def _on_error(self, msg: str) -> None:
        print(f"Error fetching data for account {self.account_id}: {msg}")


class _WalletWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self._init_ui()

    def _init_ui(self) -> None:
        self.shell = _WalletItemWidget(':/images/resources/award_shell.png')
        self.ice = _WalletItemWidget(':/images/resources/award_ice.png')
        self.candy = _WalletItemWidget(':/images/resources/award_candy.png')

        layout = QHBoxLayout(self)
        layout.addWidget(self.shell)
        layout.addWidget(self.ice)
        layout.addWidget(self.candy)

    def set_shell(self, value: int) -> None:
        self.shell.set_value(value)

    def set_ice(self, value: int) -> None:
        self.ice.set_value(value)

    def set_candy(self, value: int) -> None:
        self.candy.set_value(value)


class _WalletItemWidget(QWidget):
    def __init__(self, image_path: str) -> None:
        super().__init__()

        self.image_path = image_path
        self._init_ui()
        self.set_value(0)

    def _init_ui(self) -> None:
        icon = QLabel()
        icon_pixmap = QPixmap(self.image_path)
        if icon_pixmap.isNull():
            icon_pixmap = QPixmap(QSize(32, 32))
            icon_pixmap.fill(Qt.lightGray)
        else:
            icon_pixmap = icon_pixmap.scaled(32, 32, Qt.KeepAspectRatio, Qt.SmoothTransformation)
        icon.setPixmap(icon_pixmap)
        icon.setAlignment(Qt.AlignCenter)

        self.value = QLabel()
        self.value.setAlignment(Qt.AlignCenter)
        self.value.setFont(QFont('Arial', 12))

        layout = QHBoxLayout(self)
        layout.setAlignment(Qt.AlignCenter)
        layout.setSpacing(10)
        layout.addWidget(icon)
        layout.addWidget(self.value)

    def set_value(self, value: int) -> None:
        self.value.setText(f'x {value}')
