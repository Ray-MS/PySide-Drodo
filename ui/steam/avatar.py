import requests
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QBrush, QColor, QPainter, QPixmap
from PySide6.QtWidgets import QFrame, QLabel

from models import player_manager


class SteamAvatar(QLabel):
    def __init__(self, account_id: int, size: QSize = QSize(32, 32)) -> None:
        super().__init__()

        self.setFixedSize(size)
        self.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self._set_default_avatar()
        self._load_avatar(account_id)

    def _set_default_avatar(self) -> None:
        default_pixmap = QPixmap(self.size())
        default_pixmap.fill(QColor(200, 200, 200))

        painter = QPainter(default_pixmap)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setBrush(QBrush(QColor(100, 100, 100)))
        painter.setPen(Qt.PenStyle.NoPen)

        rect = default_pixmap.rect().adjusted(8, 8, -8, -8)
        painter.drawEllipse(rect)

        painter.end()
        self.setPixmap(default_pixmap)

    def _load_avatar(self, account_id: int):
        try:
            player = player_manager.get_player(account_id)
            avatar_url = player['avatarfull']
            resp = requests.get(avatar_url, timeout=10)
            resp.raise_for_status()

            pixmap = QPixmap()
            if pixmap.loadFromData(resp.content):
                pixmap = pixmap.scaled(
                    self.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation,
                )
                self.setPixmap(pixmap)
        except requests.RequestException as e:
            print(f"Error loading avatar: {e}")
        except Exception as e:
            print(f"Error loading avatar: {e}")
