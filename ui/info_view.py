from PySide6.QtWidgets import QLabel, QStackedWidget, QVBoxLayout, QWidget


class InfoView(QStackedWidget):
    def __init__(self) -> None:
        super().__init__()

        self.pages = {}
        self._init_ui()

    def _init_ui(self) -> None:
        self.add_page("default", _DefaultWidget())

    def add_page(self, key: int, widget: QWidget) -> None:
        if self.pages.get(key):
            print(f"页面 {key} 已存在")
            return

        self.addWidget(widget)
        self.pages[key] = widget

    def show_page(self, key: int) -> None:
        if widget := self.pages.get(key):
            self.setCurrentWidget(widget)
        else:
            self.setCurrentWidget(self.pages["default"])


class _DefaultWidget(QWidget):
    def __init__(self) -> None:
        super().__init__()
        self._init_ui()

    def _init_ui(self) -> None:
        layout = QVBoxLayout(self)

        self.label = QLabel("这里是默认视窗")
        layout.addWidget(self.label)
