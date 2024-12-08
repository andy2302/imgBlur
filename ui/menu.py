from PySide6.QtWidgets import QFrame, QVBoxLayout, QPushButton
from PySide6.QtCore import QPropertyAnimation


def create_menu_widget(parent):
    menu_widget = QFrame()
    menu_widget.setFixedWidth(0)  # Initially collapsed
    menu_widget.setStyleSheet("background-color: #333; color: white;")

    menu_layout = QVBoxLayout()
    menu_widget.setLayout(menu_layout)

    # Add menu buttons
    load_image_button = QPushButton("Load Image")
    load_image_button.clicked.connect(parent.load_image)
    menu_layout.addWidget(load_image_button)

    undo_button = QPushButton("Undo")
    undo_button.clicked.connect(parent.undo_last)
    menu_layout.addWidget(undo_button)

    blurs_button = QPushButton("Blurs")
    blurs_button.clicked.connect(parent.toggle_blurs_menu)
    menu_layout.addWidget(blurs_button)

    adjustments_button = QPushButton("Adjustments")
    adjustments_button.clicked.connect(parent.toggle_adjustments_menu)
    menu_layout.addWidget(adjustments_button)

    # Animation
    animation = QPropertyAnimation(menu_widget, b"minimumWidth")
    animation.setDuration(300)
    menu_open = False

    return menu_widget, animation, menu_open