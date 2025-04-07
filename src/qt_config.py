from PyQt5.QtWidgets import (QLabel)
from PyQt5.QtCore import Qt

def createCenterBoldTitle(title):
        titleLabel = QLabel(title)
        boldFont = titleLabel.font()
        boldFont.setBold(True)
        boldFont.setPointSize(20)
        titleLabel.setFont(boldFont)
        titleLabel.setAlignment(Qt.AlignCenter)
        return titleLabel