from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt

def createCenterBoldTitle(title):
        """
        Create a QLabel with a bold font and center alignment.

        Args:
            title (str): The title text to be displayed.

        Returns:
             QLabel: A QLabel object with the specified title, bold font, and center alignment.
        """

        titleLabel = QLabel(title)
        boldFont = titleLabel.font()
        boldFont.setBold(True)
        boldFont.setPointSize(20)
        titleLabel.setFont(boldFont)
        titleLabel.setAlignment(Qt.AlignCenter)
        return titleLabel