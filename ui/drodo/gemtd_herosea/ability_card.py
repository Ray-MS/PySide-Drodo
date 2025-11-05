from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


class GemTDAbilityCard(QWidget):
    def __init__(self, ability_id: str, ability_level: int) -> None:
        super().__init__()
        self.ability_id = ability_id
        self.ability_level = ability_level
        self.icon_size = 40

        self._init_ui()
        self._init_layout()

    def _init_ui(self):
        self.icon_label = QLabel()
        pixmap = QPixmap(f':/images/lottery/{self.ability_id}.png')
        if not pixmap.isNull():
            size = min(pixmap.width(), pixmap.height())
            cropped = pixmap.copy(
                (pixmap.width() - size) // 2,
                (pixmap.height() - size) // 2,
                size, size
            )
            scaled = cropped.scaled(
                self.icon_size, self.icon_size,
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.icon_label.setPixmap(scaled)
        self.icon_label.setFixedSize(QSize(self.icon_size, self.icon_size))

        self.level_label = QLabel()
        self.level_label.setAlignment(Qt.AlignCenter)
        self._set_level_display(self.ability_level)
        self.level_label.setFixedHeight(self.icon_size // 2)

    def _init_layout(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.level_label, alignment=Qt.AlignCenter)

    def _set_level_display(self, level: int):
        filled = '■' * level
        empty = '□' * (4 - level)
        self.level_label.setText(f'{filled}{empty}')


class GemTDEmptyAbilityCard(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self.icon_size = 40

        self._init_ui()
        self._init_layout()

    def _init_ui(self):
        self.icon_label = QLabel()
        pixmap = QPixmap(f':/images/attribute_bonus.png')
        if not pixmap.isNull():
            size = min(pixmap.width(), pixmap.height())
            cropped = pixmap.copy(
                (pixmap.width() - size) // 2,
                (pixmap.height() - size) // 2,
                size, size
            )
            scaled = cropped.scaled(
                self.icon_size, self.icon_size,
                Qt.KeepAspectRatio, Qt.SmoothTransformation
            )
            self.icon_label.setPixmap(scaled)
        self.icon_label.setFixedSize(QSize(self.icon_size, self.icon_size))

        self.level_label = QLabel()
        self.level_label.setAlignment(Qt.AlignCenter)
        self.level_label.setFixedHeight(self.icon_size // 2)

    def _init_layout(self):
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.addWidget(self.icon_label, alignment=Qt.AlignCenter)
        layout.addWidget(self.level_label, alignment=Qt.AlignCenter)
