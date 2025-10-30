import re

from PySide6.QtCore import QThread
from PySide6.QtWidgets import (QLabel, QLineEdit, QMainWindow, QPushButton,
                               QTextEdit, QVBoxLayout, QWidget)

from models.data_model import GemTDHeroesData
from network.fetcher import GemTDHeroesFetcher
from ui.sidebar import Sidebar
from ui.widgets import QuestCard


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.request_ids = set()

        self.setWindowTitle("Drodo App")
        self.setGeometry(100, 100, 800, 600)

        label = QLabel("欢迎使用 Drodo", self)
        label.move(50, 50)

        self.sidebar = Sidebar()

        self.input_id = QLineEdit()
        self.input_id.setPlaceholderText("请输入 Account ID")

        self.btn_fetch = QPushButton("获取数据")
        self.btn_fetch.clicked.connect(self.on_fetch_clicked)

        self.main_layout = QVBoxLayout()
        self.main_layout.addWidget(self.sidebar)
        self.main_layout.addWidget(self.input_id)
        self.main_layout.addWidget(self.btn_fetch)

        container = QWidget()
        container.setLayout(self.main_layout)
        self.setCentralWidget(container)

    def on_fetch_clicked(self):
        pattern = re.compile(r'^\d+$')
        text = self.input_id.text().strip()
        if not pattern.match(text):
            return

        account_id = int(text)
        if account_id in self.request_ids:
            return

        self.request_ids.add(account_id)
        self.start_fetch(account_id)

    def start_fetch(self, account_id: int):
        self.thread = QThread()
        self.worker = GemTDHeroesFetcher(account_id)
        self.worker.moveToThread(self.thread)

        self.thread.started.connect(self.worker.run)
        self.worker.finished.connect(self.handle_result)
        self.worker.error.connect(self.handle_error)

        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)

        self.thread.start()

    def handle_result(self, data: GemTDHeroesData):
        card = QuestCard(data)
        self.main_layout.addWidget(card)

    def handle_error(self, err_msg: str):
        print(f"请求出错：{err_msg}")
