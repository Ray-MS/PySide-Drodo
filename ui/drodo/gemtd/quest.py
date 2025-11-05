from PySide6.QtCore import Qt
from PySide6.QtWidgets import QHBoxLayout, QLabel, QVBoxLayout, QWidget

from config import translate_id_to_name
from models.data_model import GemTDHeroesData, GemTDQuest


class GemTDQuestCard(QWidget):
    def __init__(self):
        super().__init__()

        self._init_ui()
        self._init_layout()

    def _init_ui(self) -> None:
        pass

    def _init_layout(self) -> None:
        layout = QVBoxLayout(self)

    def on_fetch_finished(self, data: GemTDHeroesData):
        quest = data.quest

        self.layout().addWidget(_quest_random(quest))
        self.layout().addWidget(_quest_extend(quest))
        self.layout().addWidget(_quest_pass(quest))


def _format_expire(expire: int):
    d = expire // 86400
    h = (expire % 86400) // 3600
    m = (expire % 3600) // 60
    s = expire % 60
    if expire < 0:
        return '已就绪！'
    else:
        return f'刷新时间：{d}天{h}时{m}分{s}秒。'


def _quest_random(quest: GemTDQuest):
    name = f'随机任务：{translate_id_to_name(quest.quest)}'
    reward = f'奖励：随机1~{int(quest.quest[1]) * 5}贝壳。'
    time = _format_expire(quest.quest_expire)
    return _get_label(name, reward, time)


def _quest_extend(quest: GemTDQuest):
    name = f'扩展任务：完成四次随机任务。'
    reward = f'奖励：能盛放技能书的灵纹包。'
    time = f'{quest.quest_finish_count}/4'
    return _get_label(name, reward, time)


def _quest_pass(quest: GemTDQuest):
    name = f'通关任务：完成所有关卡。'
    reward = f'奖励：随机1~10贝壳。'
    time = _format_expire(quest.pass_)
    return _get_label(name, reward, time)


def _get_label(name, reward, time):
    widget = QWidget()
    layout = QHBoxLayout(widget)

    label_quest = QLabel(f'{name}\n{reward}')
    label_quest.setAlignment(Qt.AlignLeft)

    label_time = QLabel(time)
    label_time.setAlignment(Qt.AlignRight)

    layout.addWidget(label_quest)
    layout.addWidget(label_time)
    return widget
