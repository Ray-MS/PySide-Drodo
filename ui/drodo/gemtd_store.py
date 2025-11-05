from collections import defaultdict
from typing import Optional, Tuple

from PySide6.QtCore import QSize, Qt, QThread
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QGridLayout, QLabel, QVBoxLayout, QWidget

from config import translate_id_to_name
from models.gemtd import GemTDGood, GemTDGoodsResponse
from network.gemtd import GemTDGoodsFetcher

COLUMNS = 4

mapping = defaultdict(lambda: 0, {'b': 0, 'h': 1, 't': 2, 'a': 3, 'e': 4})


def _custom_sort(item: Tuple[str, GemTDGood]) -> int:
    key, good = item
    return mapping[good.id[0]], -int(good.id[1]), int(good.id[1:])


class GemTDStoreWidget(QWidget):
    def __init__(self, account_id: int = 1) -> None:
        super().__init__()

        self.account_id = account_id
        self.steam_id = str(0x110000100000000 + account_id)

        self._init_ui()
        self._start_fetch()

    def _init_ui(self) -> None:
        widgets = []

        for _ in range(12):
            widget = _GoodWidget()
            widgets.append(widget)

        self.grid_layout = QGridLayout(self)
        self.grid_layout.setSpacing(5)
        for idx, widget in enumerate(widgets):
            self.grid_layout.addWidget(widget, idx // COLUMNS, idx % COLUMNS)

    def _start_fetch(self) -> None:
        self.thread = QThread()
        self.worker = GemTDGoodsFetcher(self.account_id)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self._on_fetch_finished)
        self.worker.error.connect(self._on_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def _on_fetch_finished(self, data: GemTDGoodsResponse) -> None:
        goods = data.list
        onsale = data.onsale
        for idx, (key, good) in enumerate(sorted(goods.items(), key=_custom_sort)):
            row, col = idx // COLUMNS, idx % COLUMNS
            widget: _GoodWidget = self.grid_layout.itemAtPosition(
                row, col).widget()
            name = translate_id_to_name(good.id)
            widget.set_name(name)
            widget.set_pixmap(good.id)
            widget.set_price(good.price)
            if key == onsale:
                widget.set_onsale()

    def _on_error(self, msg: str) -> None:
        print(f"Error fetching goods for account {self.account_id}: {msg}")


class _GoodWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()

        self.price = None

        self._init_ui()
        self._init_layout()
        self._init_connections()

    def _init_ui(self) -> None:
        self.good_image = QLabel()
        image_pixmap = QPixmap(':/images/lottery/box201803.png')
        if image_pixmap.isNull():
            image_pixmap = QPixmap(QSize(50, 50))
            image_pixmap.fill(Qt.lightGray)
        else:
            image_pixmap = image_pixmap.scaledToWidth(50, Qt.SmoothTransformation)
        self.good_image.setPixmap(image_pixmap)
        self.good_image.setAlignment(Qt.AlignCenter)

        self.good_id_label = QLabel('b201711')
        self.good_price_label = QLabel('0')

        layout = QVBoxLayout(self)
        layout.addWidget(self.good_image)
        layout.addWidget(self.good_id_label)
        layout.addWidget(self.good_price_label)

    def _init_layout(self) -> None:
        ...

    def _init_connections(self) -> None:
        ...

    def set_name(self, good_id: str) -> None:
        self.good_id_label.setText(good_id)

    def set_pixmap(self, good_id: str):
        image_pixmap = QPixmap(f':/images/lottery/{good_id}.png')
        if image_pixmap.isNull():
            print(f"{good_id} not found")
            return
        image_pixmap = image_pixmap.scaledToWidth(50, Qt.SmoothTransformation)
        self.good_image.setPixmap(image_pixmap)

    def set_price(self, price: Optional[int]) -> None:
        self.price = price
        self.good_price_label.setText(f'{price}' if price else '已满级')

    def set_onsale(self) -> None:
        if self.price is None:
            return
        self.good_price_label.setText(f'<s>{self.price}</s> {self.price // 2}')
