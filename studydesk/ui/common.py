from PyQt5.QtWidgets import QFrame, QVBoxLayout, QLabel


def stat_card(title, value="0"):
    card = QFrame()
    card.setObjectName("card")
    layout = QVBoxLayout(card)
    title_label = QLabel(title)
    title_label.setObjectName("muted")
    value_label = QLabel(value)
    value_label.setObjectName("statValue")
    layout.addWidget(title_label)
    layout.addWidget(value_label)
    card.value_label = value_label
    return card
